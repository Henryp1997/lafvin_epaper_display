import pygame as pg
from pygame.locals import *
import sys
from py_inc.drawing import Cell, draw_usuable_region_border, draw_grid_lines, draw_unusable_pixels_on_top
from py_inc.consts import colours

pg.init()

epd_res_x, epd_res_y = 250, 122
pixel_size = 5 # Size of the EPD pixels in simulation pixels
num_lines_x = epd_res_x + 2
num_lines_y = epd_res_y + 2

# Minimum values of x and y that will actually draw pixels
# The LAFVIN ePaper display appears to have a border of pixels that aren't actually visible
# E.g., drawing text at x=0 actually cuts off one pixel, drawing text at y=5 cuts off one pixel
unusable_pixels_x = 1
unusable_pixels_y = 6

char_width = 7 # Width of a pixel in font12 of the EPD driver

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

def create_cell_upon_click(click_pos, pixel_size: int):
    x = int(click_pos[0] / pixel_size)
    y = int(click_pos[1] / pixel_size)
    square = Cell(surf, position=(x, y), pixel_size=pixel_size)
    squares.append(square)


LETTER_L = [
    (0, 1, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 0, 0),
]

j = 0
print(screen_x, screen_y)
while True:
    clock = pg.time.Clock()
    clock.tick(60)

    # dynamic cell creation
    reset = False
    
    # static cell creation
    # while j < 3:
    #     vertex, vertex_coords = glider(j)
    #     all_vertices.append(vertex)
    #     print(vertex_coords)
    #     square = Cell(surf, position=vertex_coords, pixel_size=pixel_size)
    #     squares.append(square)
    #     j += 1

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN:
            click_pos = event.pos
            if click_pos[1] <= (num_lines_y - 1) * pixel_size: # clicked in grid region
                create_cell_upon_click(click_pos, pixel_size)
    
    coords = []
    x, y = 0, 5
    for _ in range(35):
        for i, row in enumerate(LETTER_L):
            for j, state in enumerate(row):
                colour = "BLACK" if state else "WHITE"
                xpos, ypos = x + j, y + i
                Cell(surf, position=(xpos, ypos), pixel_size=pixel_size, colour=colour)
        x += char_width
   

    # Mask out any pixels that overstepped the allowed region
    draw_unusable_pixels_on_top(
        surf, unusable_pixels_x, unusable_pixels_y, epd_res_x, epd_res_y, pixel_size
    )

    pg.display.update()
