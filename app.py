import pygame
import sys
import pygame_gui
from tkinter import filedialog
from data_structure import Butlr32_Data, Esoil_Data, Hadamard
from visualizer import PixelMap, SmoothPixelMap, ResultMap


SCREEN_SIZE = 975, 750
OPENFILE_BUTTON = (40, 40), (120, 40)
PLAY_BUTTON = (210, 40), (100, 40)
PAUSE_BUTTON = (350, 40), (100, 40)
SMOOTH_BUTTON = (490, 40), (120, 40)
MASK_BUTTON = (650, 40), (120, 40)
CLEAR_BUTTON = (800, 40), (120, 40)
DISPLAY_SIZE = 576
DISPLAY_POSITION = 40, 120
MASK_POSITION = 650, 120
MASK_SIZE = 288
RESULT_POSITION = 650, 480
RESULT_SIZE = 300, 200
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
    mask = False

    frame = [[1]]
    pixel_map = PixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
    mask_map = PixelMap(frame, MASK_POSITION, MASK_SIZE)
    result_map = ResultMap(RESULT_POSITION, RESULT_SIZE)
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
    load_mask = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(MASK_BUTTON),
        text="Load Mask",
        manager=manager,
    )

    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(CLEAR_BUTTON),
        text="Clear",
        manager=manager,
    )

    play_button.disable()
    pause_button.disable()
    load_mask.disable()

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
                            ("NPY Files", "*.npy"),
                            ("TXT Files", "*.txt"),
                        ]
                    )
                    if filename != "":
                        if filename.split(".")[-1] == "npy":
                            data = Esoil_Data(filename)
                        if filename.split(".")[-1] == "txt":
                            data = Butlr32_Data(filename)
                        frame = data.pop_frame()
                        pixel_map = PixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
                        play_button.enable()
                        pause_button.enable()
                        load_mask.enable()
                if event.ui_element == play_button:
                    play = True
                if event.ui_element == pause_button:
                    play = False
                if event.ui_element == smooth_button:
                    smooth_button.set_text("Smooth: Off" if smooth else "Smooth: On")
                    smooth = not smooth
                if event.ui_element == load_mask:
                    filename = filedialog.askopenfilename(
                        filetypes=[
                            ("NPY Files", "*.npy"),
                        ]
                    )
                    if filename != "":
                        mask_data = Esoil_Data(filename)
                        mask_frame = mask_data.pop_frame()
                        mask_map = PixelMap(mask_frame, MASK_POSITION, MASK_SIZE)
                        mask = True
                if event.ui_element == clear_button:
                    frame = [[1]]
                    pixel_map = PixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
                    mask_map = PixelMap(frame, MASK_POSITION, MASK_SIZE)
                    result_map.clear()
                    play = False
                    smooth = False
                    mask = False
                    play_button.disable()
                    pause_button.disable()
                    load_mask.disable()
            manager.process_events(event)
        current_time = pygame.time.get_ticks()
        if current_time - last_toggle_time > 1000 / FPS:
            if play:
                if data.get_length() != 0:
                    frame = data.pop_frame()
                    if smooth:
                        pixel_map = SmoothPixelMap(
                            frame, DISPLAY_POSITION, DISPLAY_SIZE
                        )
                    else:
                        pixel_map = PixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
                    if mask:
                        result_sum = Hadamard(frame, mask_frame)
                        result_map.add(result_sum)

            if smooth:
                pixel_map = SmoothPixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
            else:
                pixel_map = PixelMap(frame, DISPLAY_POSITION, DISPLAY_SIZE)
            last_toggle_time = current_time

        screen.fill(GRAY)
        pixel_map.draw(screen)
        mask_map.draw(screen)
        result_map.draw(screen)
        manager.update(delta_time / 1000.0)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
