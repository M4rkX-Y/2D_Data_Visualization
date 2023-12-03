import pygame
import sys
import pygame_gui
from tkinter import filedialog
from Data import Butlr32_Data, Esoil_Data


SCREEN_SIZE = 840, 640
DISPLAY_SIZE = 480
DISPLAY_POSITION = 40, 80
OPENFILE_BUTTON = (10, 10), (100, 40)
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 93, 93, 93
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


def main():
    pygame.init()

    # TODO: Adding the implementation of reading the file and select how we want to visualize the data.
    # data = Esoil_Data("./data/11_15_3x3_5.npy")
    data = Butlr32_Data("./data/standing_9_32x32_sensor.txt")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    manager = pygame_gui.UIManager(SCREEN_SIZE)
    pygame.display.set_caption("Data Visualization")

    # TODO: The button is not showing up
    file_explore = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(OPENFILE_BUTTON),
        text="Click Me",
        manager=manager,
    )

    frame = data.pop_frame()
    pixel_map = PixelMap(frame)
    clock = pygame.time.Clock()
    last_toggle_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.ui_element == file_explore:
                    filename = filedialog.askopenfilename(
                        filetypes=[
                            ("TXT Files", "*.txt"),
                            ("NPY Files", "*.npy"),
                        ]
                    )
                    print(filename)
                    manager.process_events(event)

        manager.update(clock.tick(60) / 1000.0)

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

        screen.fill(GRAY)
        pixel_map.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
