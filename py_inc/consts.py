epd_res_x, epd_res_y = 250, 122
pixel_size = 5 # Size of the EPD pixels in simulation pixels
num_lines_x = epd_res_x + 2
num_lines_y = epd_res_y + 2
char_width = 7       # Width of a character in font12 of the EPD driver
char_height = 12     # Height of a character in font12 of the EPD driver
char_start = (7, 12) # Topleft-most character position in EPD pixels
nlines = 9

# Number of characters allowed per buffer
# as determined empirically using char_start = (7, 12)
buffer_nchars = [8, 9, 9, 8]
buffer_start_pos = [0, 8, 17, 26] # Buffer character positions (not pixels!)

# Pixel delta in vertical direction between top of characters
# in one row and top of characters in the row below
line_spacing = 12

# Minimum values of x and y that will actually draw pixels
# The LAFVIN ePaper display appears to have a border of pixels that aren't actually visible
# E.g., drawing text at x=0 actually cuts off one pixel, drawing text at y=5 cuts off one pixel
unusable_pixels_x = 1
unusable_pixels_y = 6

colours = {
    "BLUE"     : (0, 100, 200),
    "LIGHTBLUE": "#b4c2cf",
    "RED"      : (225, 25, 25),
    "GREEN"    : (0, 255, 0),
    "BLACK"    : (60, 60, 60),
    "WHITE"    : (255, 255, 255),
    "GREY1"    : "#cccccc",
    "GREY2"    : "#777777",
    "GREY3"    : "#d9d9d9"
}