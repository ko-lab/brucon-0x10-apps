from neopixel import NeoPixel
from machine import Pin

print('init rgb')
PIN_NUM = 5  # GPIO 5 for NeoPixel data
WIDTH, HEIGHT = 32, 19
NUM_LEDS = WIDTH * HEIGHT

strip = NeoPixel(Pin(PIN_NUM),NUM_LEDS)

print('done init rgb')
def xy_to_i(x, y):
    return y * WIDTH + x

def framerate(frame):
    raise NotImplementedError('TODO implement')

def text(text, color=(255, 255, 255), pos=None):
    raise NotImplementedError('TODO implement')


def scrolltext(text, color=(255, 255, 255), pos=None, width=None):
    raise NotImplementedError('TODO implement')

def background(color=(0, 0, 0)):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            strip[xy_to_i(x, y)] = color
    strip.write()

def pixel(color=(255, 255, 255), pos=(0,0)):
    (r, g, b) = color
    (x, y) = pos
    strip[xy_to_i(x, y)] = (r, g, b)
    strip.write()

def gif(data, pos=(0,0), size=(8,8), frames=1):
    raise NotImplementedError('TODO implement')

def image(data, pos=(0,0), size=(8,8)):
    width, height = size
    start_x, start_y = pos
    num_leds = len(strip)  # Total number of LEDs in the strip

    # Calculate linear position in data for strip LEDs
    for y in range(height):
        for x in range(width):
            index_in_data = y * width + x  # Convert 2D position to linear index
            led_index = (start_y + y) * WIDTH + start_x + x  # Map to strip index

            if led_index < num_leds:
                color = data[index_in_data]

                # Convert ARGB to RGB for WS2812 (ignore the alpha)
                alpha = color & 0xff
                if alpha == 0:
                    continue
                b = (color >> 8) & 0xff
                g = (color >> 16) & 0xff
                r = color >> 24

                # Set color to the LED at calculated index
                strip[led_index] = (r, g, b)

    # Write out all the colors to the strip in one go
    strip.write()

def getbrightness():
    return 100 # 'TODO implement'

def setbrightness(brightness):
    pass # 'TODO implement'

def setfont(font_index):
    raise NotImplementedError('TODO implement')

def clear():
    background()
# Restore previously set brightness
setbrightness(getbrightness() or (MAX_BRIGHTNESS - 2))
