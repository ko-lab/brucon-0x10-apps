import rgb

WIDTH, HEIGHT = 32, 19
image_buffer = [0]*(WIDTH*HEIGHT)

def rgb_to_hex(color):
    (r, g, b) = color
    return rgba_to_hex((r,g,b,0))

def rgba_to_hex(color):
    (r, g, b, alpha) = color
    color_value = (r << 24) | (g << 16) | (b << 8) | alpha
    return color_value


def reset_buffer():
    global image_buffer
    image_buffer = [0]*(WIDTH*HEIGHT)


def prepare_pixel_global(pos, color):
    global image_buffer
    (posx, posy)= pos
    hex_color = rgb_to_hex(color)
    i = posy*WIDTH+ posx
    image_buffer[i] = hex_color


def render_image_buffer():
        rgb.image(image_buffer, pos=(0,0), size=(WIDTH, HEIGHT))
