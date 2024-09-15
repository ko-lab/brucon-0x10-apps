DEBUG = True
from winner import ko_lab_matrix_animation
from loser import loser_animation
from display_helper import rgba_to_hex
def log(message):
    print(message)


log("Starting up main.py...")

import random
import time
import accel
import rgb
import buttons

# Setup RGB
WIDTH, HEIGHT = 32, 19

# Game variables
block_size = 2
block_x, block_y = WIDTH // 2 - block_size // 2 - 1, HEIGHT // 2 - block_size // 2
block_locations = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
game_won = False
game_lost = False


def reset():
    global game_won
    global game_lost
    game_won = False
    game_lost = False
    global block_size
    block_size = 1
    global block_x
    global block_y
    block_x, block_y = WIDTH // 2 - block_size // 2 - 1, HEIGHT // 2 - block_size // 2
    global block_locations
    block_locations = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    startup_sequence()


def set_pixel(x, y, r, g, b):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        rgb.pixel((r, g, b), (x, y))


def fill(r, g, b):
    rgb.background((r, g, b))


def random_color(max=255):
    if random.randint(0, 5) != 0:
        return (0, 0, 0, 0)

    return (random.randint(0, max), random.randint(0, max), random.randint(0, max), 0xff)


def write_kolab(text_color=(255, 000, 000, 0xff), random_background=False):
    global game_won
    global game_lost

    message = """
|IIIIIIIIIIIIIIIIIIIIIIIIIIIIII|
|                              |
| K   K  OOO     L    AA  BBB  |
| K  K  O   O    L   A  A B  B |
| KKK   O   O -- L   AAAA BBB  |
| K  K  O   O    L   A  A B  B |
| K   K  OOO     LLL A  A BBB  |
|                              |
|IIIIIIIIIIIIIIIIIIIIIIIIIIIIII|"""

    letter_height = 8

    x_start = 0
    y_start = (HEIGHT - letter_height) // 2
    img_width = len(message.split('\n')[1:][0])
    img_height = len(message.split('\n')[1:])
    # Initialize the data array to store color values for each pixel
    data = [0] * (img_width * img_height)  # Initialize all pixels to black
    found_unmasked_kolab_pixel = False
    found_unmasked_sparkle_pixel = False
    # Update the data array based on the message
    for y, row in enumerate(message.split('\n')[1:]):  # Skip the first newline character
        for x, char in enumerate(row):
            index_in_img = (y) * img_width + (x)
            global_y = y + y_start
            global_x = x + x_start
            if char == ' ':
                if block_locations[global_y][global_x]:
                    color = (0, 0, 0, 255)  # Turn off places where the block as been
                else:
                    found_unmasked_sparkle_pixel = True
                    color = random_color(150) if random_background else (0, 100, 0, 0xff)
            else:
                if block_locations[global_y][global_x]:
                    color = (0, 255, 0, 255)
                else:
                    found_unmasked_kolab_pixel = True
                    color = text_color  # Assign text color

            color_value = rgba_to_hex(color)
            data[index_in_img] = color_value
    if not found_unmasked_kolab_pixel:
        game_won = True
    if not found_unmasked_sparkle_pixel:
        game_lost = True

    return lambda: rgb.image(data, pos=(x_start, y_start), size=(img_width, img_height))


def draw_sparkles():
    write_kolab((255, 0, 0, 0xff), True)()


def draw_block():
    for y in range(block_size):
        for x in range(block_size):
            set_pixel(block_x + x, block_y + y, 255, 255, 255)  # Red color

def to_1or2(val50k, tresh):
    sign = val50k>0
    absval = abs(val50k)
    result = 1 if absval > tresh else 0
    return result if sign else -result

def update_block_position():
    global block_x, block_y

    if accel:
        ax, ay, _ = accel.get_xyz()
        # Adjust sensitivity as needed
        # print('ay', ay)

        dx = to_1or2(ax, 10000)
        dy = to_1or2(ay, 5000)
        # print('dx', dx)

        new_x = max(0, min(WIDTH - block_size, block_x - dx))
        new_y = max(0, min(HEIGHT - block_size, block_y - dy))

        # Update sparkles
        for y in range(block_size):
            for x in range(block_size):
                if not block_locations[new_y + y][new_x + x]:
                    # print('marking block location: ' + str(new_y + y) + ', ' + str(new_x + x))
                    block_locations[new_y + y][new_x + x] = True

        block_x, block_y = new_x, new_y


def main():
    log("[START] main()")
    startup_sequence()
    accel.init()
    loop_count = 0
    while True:
        game_loop()
        loop_count += 1
        if loop_count % 100 == 0:
            log(f"Main loop iteration: {loop_count}")


def game_loop():
    if game_won:
        game_won_loop()
        return
    if game_lost:
        game_lost_loop()
        return
    do_write= write_kolab()
    rgb.clear()
    do_write()
    # draw_sparkles()
    update_block_position()
    draw_block()
    time.sleep(0.1)  # Add a small delay to prevent the loop from running too fast


def game_lost_loop():
    loser_animation()


def game_won_loop():
    ko_lab_matrix_animation()


def startup_sequence():
    # fill(0, 0, 0)
    write_kolab()()
    time.sleep(0.5)
    draw_block()


def handle_button_press(down: bool, button: str):
    if down:
        print('button [' + button + '] pressed, resetting game!')
        reset()


def force_game_won(down):
    global game_won
    if DEBUG and down:
        print('force won!')
        game_won = True

def force_game_lost(down):
    global game_lost
    if DEBUG and down:
        print('force lost!')
        game_lost = True

def setup_button_callback():
    buttons.register(buttons.BTN_A, lambda down: handle_button_press(down, 'A'))
    buttons.register(buttons.BTN_UP, lambda down: handle_button_press(down, 'UP'))
    buttons.register(buttons.BTN_DOWN, lambda down: handle_button_press(down, 'DOWN'))
    buttons.register(buttons.BTN_LEFT, force_game_lost)
    buttons.register(buttons.BTN_RIGHT, force_game_won)


# if __name__ == "__main__":
log("Script started")
setup_button_callback()
main()
