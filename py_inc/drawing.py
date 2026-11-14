import pygame as pg
import numpy as np
from py_inc.consts import colours


class Cell():
    def __init__(
        self,
        surface: pg.Surface,
        position: tuple,
        pixel_size: int,
        colour: str = "BLACK"
    ):
        self.position = position # Position in grid coordinates (not pixels)
        self.x = self.position[0] * pixel_size
        self.y = self.position[1] * pixel_size
        vertex = (self.x + 1, self.y + 1) # Account for grid linewidth
        pg.draw.rect(
            surface,
            colours[colour],
            pg.Rect(vertex, (pixel_size - 1, pixel_size - 1))
        )


def draw_usuable_region_border(
    surface: pg.Surface,
    unusable_pixels_x: int,
    unusable_pixels_y: int,
    epd_res_x: int,
    epd_res_y: int,
    pixel_size: int,
    colour: str = "red"
):
    pg.draw.rect(
        surface,
        colour,
        tuple(np.array([
            unusable_pixels_x,
            unusable_pixels_y,
            (epd_res_x - unusable_pixels_x),
            (epd_res_y - unusable_pixels_y),
        ]) * pixel_size),
        width=1
    )


def draw_grid_lines(
    surface: pg.Surface,
    num_lines_x: int,
    num_lines_y: int,
    pixel_size: int,
    colour: str = "GREY2"
):
    x, y = 0, 0
    for _ in range(int(num_lines_x)):
        pg.draw.line(
            surface,
            colours[colour],
            (x, 0), (x, (num_lines_y - 1) * pixel_size)
        )
        x += pixel_size
    for _ in range(int(num_lines_y)):
        pg.draw.line(
            surface,
            colours[colour],
            (0, y), ((num_lines_x - 1) * pixel_size, y)
        )
        y += pixel_size
    return


def draw_unusable_pixels_on_top(
    surface: pg.Surface,
    unusable_pixels_x: int,
    unusable_pixels_y: int,
    epd_res_x: int,
    epd_res_y: int,
    pixel_size: int,
    colour: str = "GREY1"
):
    # Mask out the top unusable_pixels_y rows of pixels (won't use these)
    for y in range(unusable_pixels_y):
        for x in range(epd_res_x):
            Cell(
                surface, position=(x, y), pixel_size=pixel_size, colour=colour
            )

    # Mask out a 1 pixel column on the left
    for y in range(epd_res_y):
        for x in range(unusable_pixels_x):
            Cell(
                surface, position=(x, y), pixel_size=pixel_size, colour=colour
            )