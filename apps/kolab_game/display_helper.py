def rgb_to_hex(color):
    (r, g, b) = color
    return rgba_to_hex((r,g,b,0))

def rgba_to_hex(color):
    (r, g, b, alpha) = color
    color_value = (r << 24) | (g << 16) | (b << 8) | alpha
    return color_value

