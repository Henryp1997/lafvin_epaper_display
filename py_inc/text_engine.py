import pygame as pg
from py_inc.drawing import Cell
from py_inc.consts import *
from py_inc.font12 import font12


def draw_string(surface: pg.Surface, string: str):
    buffer_data = [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
    ]
    j = 0
    line = 0
    for _, char in enumerate(string):
        if j > sum(buffer_nchars) - 1:
            j = 0
            line += 1

        if j < buffer_start_pos[1]:
            buffer = 0
        elif buffer_start_pos[1] <= j < buffer_start_pos[2]:
            buffer = 1
        elif buffer_start_pos[2] <= j < buffer_start_pos[3]:
            buffer = 2
        elif buffer_start_pos[3] <= j:
            buffer = 3

        buffer_data[line][buffer].append(char)
        j += 1

    # Draw strings in buffer data
    for line in range(nlines):
        draw_buffer_chars(surface, 0, line, buffer_data, colour="RED")
        draw_buffer_chars(surface, 1, line, buffer_data)
        draw_buffer_chars(surface, 2, line, buffer_data, colour="BLUE")
        draw_buffer_chars(surface, 3, line, buffer_data)


def draw_buffer_chars(
    surface: pg.Surface,
    buffer: int,
    line: int,
    buffer_data: str,
    colour: str = "BLACK",
):
    x, y = char_start
    for i in range(buffer):
        # Offset by previous buffers
        x += buffer_nchars[i] * char_width

    chars = buffer_data[line][buffer]
    if len(chars) < buffer_nchars[buffer]:
        chars += [" "] * (buffer_nchars[buffer] - len(chars))

    y += line * line_spacing
    for char in buffer_data[line][buffer]:
        letter = font12[char]
        for i, row in enumerate(letter):
            for j, state in enumerate(row):
                c = colour if state else "WHITE"
                xpos, ypos = x + j, y + i
                Cell(
                    surface, position=(xpos, ypos), pixel_size=pixel_size, colour=c
                )
        x += char_width
