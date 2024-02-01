import pygame
from scipy.ndimage import zoom
import matplotlib

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab


WHITE = 255, 255, 255


class Pixel:
    def __init__(self, x, y, color, pixel_size):
        self.rect = pygame.Rect(x, y, pixel_size, pixel_size)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class PixelMap:
    def __init__(self, pixel_map, display_position, pixel_size):
        self.pixels = []
        modified_pixel_map = self.modification(pixel_map)
        self.size = len(modified_pixel_map)
        self.pixel_size = pixel_size / self.size

        for row in range(self.size):
            for col in range(self.size):
                x = col * self.pixel_size + display_position[0]
                y = row * self.pixel_size + display_position[1]
                color = tuple([modified_pixel_map[row][col] * x for x in WHITE])
                self.pixels.append(Pixel(x, y, color, self.pixel_size))

    def modification(self, og_pixel_map):
        return og_pixel_map

    def draw(self, surface):
        for pixel in self.pixels:
            pixel.draw(surface)


class SmoothPixelMap(PixelMap):
    def __init__(self, pixel_map, display_position, pixel_size):
        super().__init__(pixel_map, display_position, pixel_size)

    def modification(self, og_pixel_map):
        return zoom(og_pixel_map, zoom=2, order=1)


class ResultMap:
    def __init__(self, display_position, size):
        self.result = []
        self.position = display_position
        self.size = size
        matplotlib.pyplot.rcParams.update(
            {
                "lines.marker": ".",  # available ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
                "lines.linewidth": "0.5",
                "axes.prop_cycle": matplotlib.pyplot.cycler(
                    "color", ["white"]
                ),  # line color
                "text.color": "white",  # no text in this example
                "axes.facecolor": "black",  # background of the figure
                "axes.edgecolor": "lightgray",
                "axes.labelcolor": "white",  # no labels in this example
                "axes.grid": "True",
                "grid.linestyle": "--",  # {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
                "xtick.color": "white",
                "ytick.color": "white",
                "grid.color": "lightgray",
                "figure.facecolor": "black",  # color surrounding the plot
                "figure.edgecolor": "black",
            }
        )
        self.fig = pylab.figure(
            figsize=[3, 2],
            dpi=100,
        )
        self.fig.patch.set_alpha(1)
        self.ax = self.fig.gca()
        self.ax.plot(self.result)

        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        self.raw_data = renderer.tostring_rgb()

    def add(self, result):
        self.result.append(result)
        self.ax.plot(self.result)

        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        self.raw_data = renderer.tostring_rgb()

    def draw(self, screen):
        surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
        screen.blit(surf, self.position)
        matplotlib.pyplot.close()
