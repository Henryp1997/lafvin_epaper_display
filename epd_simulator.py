import sys
from pathlib import Path
import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from py_inc.drawing import (
    Cell, draw_usuable_region_border,
    draw_grid_lines, draw_unusable_pixels_on_top
)
from py_inc.text_engine import draw_string, draw_buffer_chars, output_cpp_code_to_file
from py_inc.messages_ import messages, func_names
from py_inc.consts import *
HERE = Path(__file__).parent

pg.init()

screen_x = epd_res_x * pixel_size
screen_y = epd_res_y * pixel_size

squares = []
all_vertices = []
surf = pg.display.set_mode((screen_x, screen_y))
surf.fill(colours["GREY1"])
pg.display.set_caption("LAFVIN 2.13inch ePaper display simulator")

# Draw grid lines and a boundary indicating the usuable region of the display
draw_grid_lines(surf, num_lines_x, num_lines_y, pixel_size)
draw_usuable_region_border(
    surf,
    unusable_pixels_x, unusable_pixels_y,
    epd_res_x, epd_res_y,
    pixel_size
)


def get_new_message_idx(current_idx):
    import random
    next_idx = current_idx
    while next_idx == current_idx:
        next_idx = random.randint(1, len(messages) - 1)

    return next_idx


### Simulation loop
j = 0
advance_in_order = False
output_message = True
draw_watermark = True
message_idx = 0      # Index of message in `messages` list
message_page_idx = 0 # Index of page within message
cpp_write_mode = "w"
cpp_filename = "messages"

# Clear cpp files before starting
open(HERE / f"{cpp_filename}.h", "w").close()
open(HERE / f"{cpp_filename}.cpp", "w").close()

while True:
    clock = pg.time.Clock()
    clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN:
            # Allow turning pixels on with clicks
            click_pos = event.pos
            if click_pos[1] <= (num_lines_y - 1) * pixel_size: # clicked in grid region
                x = int(click_pos[0] / pixel_size)
                y = int(click_pos[1] / pixel_size)
                square = Cell(surf, position=(x, y), pixel_size=pixel_size)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # Pressed space. Advance message to next page if in a multi-page message or a random next message
                if isinstance(current_message, (list, tuple)):
                    # Message is a multi-page message, only change message_idx if advanced past the last page
                    message_page_idx += 1
                    if message_page_idx > len(current_message) - 1:
                        message_page_idx = 0
                        if advance_in_order:
                            message_idx += 1
                        else:
                            message_idx = get_new_message_idx(current_idx=message_idx)
                else:
                    if advance_in_order:
                        message_idx += 1
                    else:
                        message_idx = get_new_message_idx(current_idx=message_idx)
                output_message = True
            elif event.key == pg.K_ESCAPE:
                print("Clearing cpp files...")
                open(HERE / f"{cpp_filename}.h", "w").close()
                open(HERE / f"{cpp_filename}.cpp", "w").close()
    
    # Draw string
    if isinstance((current_message := messages[message_idx]), (tuple, list)):
        string_to_write = current_message[message_page_idx]
    else:
        string_to_write = current_message
    
    buffer_data = draw_string(surf, string_to_write)

    if message_idx != 0 and draw_watermark:
        # Draw a "Press the button..." watermark
        buffer_data[-1][1] = [i for i in f"{' ' * (buffer_nchars[1] - 2)}Pr"]
        buffer_data[-1][2] = [i for i in "ess the b"]
        buffer_data[-1][3] = [i for i in "utton..."]

        for buffer in (1, 2, 3):
            draw_buffer_chars(
                surf, buffer, -1, buffer_data,
                x=char_start[0] + (sum(buffer_nchars[:buffer])) * char_width,
                y=char_start[1] + (nlines - 1) * (char_height + line_separation)
            )

    if isinstance(current_message, (tuple, list)):
        # Draw a page number
        buffer_data[-1][0] = [i for i in f"Page {message_page_idx + 1} of {len(messages[message_idx])}"]
        for buffer in (0,):
            draw_buffer_chars(
                surf, buffer, -1, buffer_data,
                x=char_start[0],
                y=char_start[1] + (nlines - 1) * (char_height + line_separation)
            )

    if output_message:
        func_name = func_names[message_idx]
        if isinstance(current_message, (tuple, list)):
            func_name = f"{func_name}{message_page_idx}"
        output_cpp_code_to_file(
            buffer_data,
            func_name=func_name,
            file=cpp_filename,
            write_mode=cpp_write_mode
        )
        if cpp_write_mode == "w":
            # Toggle to append mode after one write
            cpp_write_mode = "a"
        output_message = False

    # Mask out any pixels that overstepped the allowed region
    draw_unusable_pixels_on_top(
        surf, unusable_pixels_x, unusable_pixels_y, epd_res_x, epd_res_y, pixel_size
    )

    pg.display.update()
    j += 1
