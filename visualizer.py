import pygame
from scipy.ndimage import zoom


DISPLAY_SIZE = 576
DISPLAY_POSITION = 40, 120
WHITE = 255, 255, 255


class Pixel:
    def __init__(self, x, y, color, pixel_size):
        self.rect = pygame.Rect(x, y, pixel_size, pixel_size)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class PixelMap:
    def __init__(self, pixel_map):
        self.pixels = []
        modified_pixel_map = self.modification(pixel_map)
        self.size = len(modified_pixel_map)
        self.pixel_size = DISPLAY_SIZE / self.size

        for row in range(self.size):
            for col in range(self.size):
                x = col * self.pixel_size + DISPLAY_POSITION[0]
                y = row * self.pixel_size + DISPLAY_POSITION[1]
                color = tuple([modified_pixel_map[row][col] * x for x in WHITE])
                self.pixels.append(Pixel(x, y, color, self.pixel_size))

    def modification(self, og_pixel_map):
        return og_pixel_map

    def draw(self, surface):
        for pixel in self.pixels:
            pixel.draw(surface)


class SmoothPixelMap(PixelMap):
    def __init__(self, pixel_map):
        super().__init__(pixel_map)

    def modification(self, og_pixel_map):
        return zoom(og_pixel_map, zoom=2, order=1)
