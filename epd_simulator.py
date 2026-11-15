import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import sys
from py_inc.drawing import (
    Cell, draw_usuable_region_border,
    draw_grid_lines, draw_unusable_pixels_on_top
)
from py_inc.text_engine import draw_string, output_cpp_code_to_file
from py_inc.consts import *

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


### Simulation loop
j = 0
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
    
    # Draw string
    if j == 0:
        string = "hello, world!" * 8
        buffer_data = draw_string(surf, string)
        output_cpp_code_to_file(buffer_data, string, func_name="helloWorld")

    # Mask out any pixels that overstepped the allowed region
    draw_unusable_pixels_on_top(
        surf, unusable_pixels_x, unusable_pixels_y, epd_res_x, epd_res_y, pixel_size
    )

    pg.display.update()
    j += 1
