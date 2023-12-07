import pygame
import sys
import pygame_gui
from tkinter import filedialog
from data_structure import Butlr32_Data, Esoil_Data
from visualizer import PixelMap, SmoothPixelMap


SCREEN_SIZE = 650, 750
OPENFILE_BUTTON = (40, 40), (120, 40)
PLAY_BUTTON = (210, 40), (100, 40)
PAUSE_BUTTON = (350, 40), (100, 40)
SMOOTH_BUTTON = (490, 40), (120, 40)
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 53, 53, 53
FPS = 5


def main():
    pygame.init()
    pygame.display.set_caption("Data Visualization")

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
