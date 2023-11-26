import pygame
import sys
import pygame_gui
from Data import Butlr32_Data


PIXEL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 5


class Pixel:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PIXEL_SIZE, PIXEL_SIZE)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class PixelMap:
    def __init__(self, pixel_map):
        self.pixels = []

        self.size = len(pixel_map)

        for row in range(self.size):
            for col in range(self.size):
                x = col * PIXEL_SIZE
                y = row * PIXEL_SIZE
                color = tuple([pixel_map[row][col] * x for x in WHITE])
                self.pixels.append(Pixel(x, y, color))

    def draw(self, surface):
        for pixel in self.pixels:
            pixel.draw(surface)


def main():
    pygame.init()
    data = Butlr32_Data("data\\standing_9_32x32_sensor.txt")
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Pixel Map")

    frame = data.pop_frame()
    pixel_map = PixelMap(frame)
    clock = pygame.time.Clock()
    last_toggle_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()

        if current_time - last_toggle_time > 1000 / FPS:
            new_frame = data.pop_frame()
            i = 0
            for row in range(pixel_map.size):
                for col in range(pixel_map.size):
                    pixel_map.pixels[i].color = tuple(
                        [new_frame[row][col] * x for x in WHITE]
                    )
                    i += 1

            last_toggle_time = current_time

        screen.fill(BLACK)
        pixel_map.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
