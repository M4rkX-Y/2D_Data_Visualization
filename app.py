import pygame
import sys
import pygame_gui
from tkinter import filedialog
from scipy.ndimage import zoom
from data import Butlr32_Data, Esoil_Data


SCREEN_SIZE = 650, 750
DISPLAY_SIZE = 576
DISPLAY_POSITION = 40, 120
OPENFILE_BUTTON = (40, 40), (120, 40)
PLAY_BUTTON = (210, 40), (100, 40)
PAUSE_BUTTON = (350, 40), (100, 40)
SMOOTH_BUTTON = (490, 40), (120, 40)
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 53, 53, 53
FPS = 5


class Pixel:
    def __init__(self, x, y, color, pixel_size):
        self.rect = pygame.Rect(x, y, pixel_size, pixel_size)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class PixelMap:
    def __init__(self, pixel_map):
        self.pixels = []
        self.size = len(pixel_map)
        self.pixel_size = DISPLAY_SIZE / self.size

        for row in range(self.size):
            for col in range(self.size):
                x = col * self.pixel_size + DISPLAY_POSITION[0]
                y = row * self.pixel_size + DISPLAY_POSITION[1]
                color = tuple([pixel_map[row][col] * x for x in WHITE])
                self.pixels.append(Pixel(x, y, color, self.pixel_size))

    def draw(self, surface):
        for pixel in self.pixels:
            pixel.draw(surface)


class SmoothPixelMap(PixelMap):
    def __init__(self, pixel_map):
        super().__init__(pixel_map)
        self.pixels = []
        self.size *= 2
        self.pixel_size = DISPLAY_SIZE / self.size
        smooth_pixel_map = zoom(pixel_map, zoom=2, order=1)
        for row in range(self.size):
            for col in range(self.size):
                x = col * self.pixel_size + DISPLAY_POSITION[0]
                y = row * self.pixel_size + DISPLAY_POSITION[1]
                color = tuple([smooth_pixel_map[row][col] * x for x in WHITE])
                self.pixels.append(Pixel(x, y, color, self.pixel_size))


def main():
    pygame.init()
    pygame.display.set_caption("Data Visualization")

    # TODO: Adding the implementation of reading the file and select how we want to visualize the data.
    screen = pygame.display.set_mode(SCREEN_SIZE)
    manager = pygame_gui.UIManager(SCREEN_SIZE)
    play = False
    smooth = False

    frame = [[1]]
    pixel_map = PixelMap(frame)
    clock = pygame.time.Clock()
    last_toggle_time = pygame.time.get_ticks()

    file_explore = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(OPENFILE_BUTTON),
        text="Open File",
        manager=manager,
    )
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(PLAY_BUTTON),
        text="Play",
        manager=manager,
    )

    pause_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(PAUSE_BUTTON),
        text="Pause",
        manager=manager,
    )
    smooth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(SMOOTH_BUTTON),
        text="Smooth: Off",
        manager=manager,
    )

    play_button.disable()
    pause_button.disable()

    while True:
        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == file_explore:
                    filename = filedialog.askopenfilename(
                        filetypes=[
                            ("TXT Files", "*.txt"),
                            ("NPY Files", "*.npy"),
                        ]
                    )
                    if filename.split(".")[-1] == "npy":
                        data = Esoil_Data(filename)
                    if filename.split(".")[-1] == "txt":
                        data = Butlr32_Data(filename)
                    frame = data.pop_frame()
                    pixel_map = PixelMap(frame)
                    play_button.enable()
                    pause_button.enable()
                if event.ui_element == play_button:
                    play = True
                if event.ui_element == pause_button:
                    play = False
                if event.ui_element == smooth_button:
                    smooth_button.set_text("Smooth: Off" if smooth else "Smooth: On")
                    smooth = not smooth
            manager.process_events(event)

        current_time = pygame.time.get_ticks()
        if current_time - last_toggle_time > 1000 / FPS:
            if play:
                frame = data.pop_frame()
                if smooth:
                    pixel_map = SmoothPixelMap(frame)
                else:
                    pixel_map = PixelMap(frame)

            if smooth:
                pixel_map = SmoothPixelMap(frame)
            else:
                pixel_map = PixelMap(frame)
            last_toggle_time = current_time

        screen.fill(GRAY)
        pixel_map.draw(screen)
        manager.update(delta_time / 1000.0)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
