import random
import time

import accel
import rgb
from display_helper import rgb_to_hex

def log(message):
    print(message)

# Setup RGB
WIDTH, HEIGHT = 32, 19
image_buffer = [0]*(WIDTH*HEIGHT)
# Matrix Animation Variables
matrix_columns = [random.randint(0, HEIGHT - 1) for _ in range(WIDTH)]  # Y positions of the head of each column
cyan_columns = []  # List to store the indices of cyan columns

# Characters for the Matrix effect (not needed but here to resemble the idea)
matrix_chars = [chr(i) for i in range(33, 127)]  # Printable ASCII characters

# KOLAB Text and Protected Area
kolab_message = [
    " K   K  OOO     L    AA  BBB  ",
    " K  K  O   O    L   A  A B  B ",
    " KKK   O   O -- L   AAAA BBB  ",
    " K  K  O   O    L   A  A B  B ",
    " K   K  OOO     LLL A  A BBB  "
]
kolab_protected_pixels = []

# Initial position of KOLAB text (centered)
kolab_x = (WIDTH - len(kolab_message[0])) // 2
kolab_y = (HEIGHT - len(kolab_message)) // 2

def initialize_protected_pixels():
    """Determine the pixels where the KOLAB text is located to protect them from the Matrix animation."""
    kolab_protected_pixels.clear()
    for y, line in enumerate(kolab_message):
        for x, char in enumerate(line):
            if char != ' ':
                kolab_protected_pixels.append((kolab_x + x, kolab_y + y))

def is_protected_pixel(x, y):
    """Check if the given pixel is part of the KOLAB text."""
    return (x, y) in kolab_protected_pixels

def initialize_cyan_columns(min_cyan=0, max_cyan=3):
    """Randomly select columns to be cyan, between min_cyan and max_cyan."""
    global cyan_columns
    num_cyan = random.randint(min_cyan, max_cyan)
    selected = set()
    while len(selected) < num_cyan:
        col = random.randint(0, WIDTH - 1)
        selected.add(col)
    cyan_columns = list(selected)

def buffer_matrix_frame():
    """Draw one frame of the Matrix effect."""
    for x in range(WIDTH):
        # Determine the color for the current column
        if x in cyan_columns:
            color = (0, 255, 255)  # Cyan color for special columns
        else:
            color = (0, 255, 0)  # Default green color

        # Move the column's head down by one row
        matrix_columns[x] = (matrix_columns[x] + 1) % HEIGHT

        # Draw the "head" of the column
        if not is_protected_pixel(x, matrix_columns[x]):
            prepare_pixel_global((x, matrix_columns[x]), color)

        # Draw the trailing characters with dimmer colors
        for i in range(1, 4):
            char_y = (matrix_columns[x] - i) % HEIGHT
            if not is_protected_pixel(x, char_y):
                prepare_pixel_global((x, char_y), (color[0], color[1] // (i + 1), color[2] // (i + 1)))

def prepare_pixel_global(pos, color):
    (posx, posy)= pos
    hex_color = rgb_to_hex(color)
    i = posy*WIDTH+ posx
    image_buffer[i] = hex_color

def buffer_kolab():
    """Draw the 'KOLAB' text at its current position."""
    for y, line in enumerate(kolab_message):
        for x, char in enumerate(line):
            if char != ' ':
                prepare_pixel_global((kolab_x+ x, kolab_y+y), (11, 118, 187))  # RGB color for KOLAB text

def update_kolab_position():
    """Update the KOLAB text position based on accelerometer input."""
    global kolab_x, kolab_y
    ax, ay, az = accel.get_xyz()

    # Adjust the sensitivity as needed
    threshold = 5
    if az < -threshold:  # Device held upright (neutral position)
        kolab_x = (WIDTH - len(kolab_message[0])) // 2
        kolab_y = (HEIGHT - len(kolab_message)) // 2
    else:
        if ax > threshold:  # Tilted right
            kolab_x = max(0, kolab_x - 1)
        elif ax < -threshold:  # Tilted left
            kolab_x = min(WIDTH - len(kolab_message[0]), kolab_x + 1)

        if ay > threshold:  # Tilted forward
            kolab_y = max(0, kolab_y - 1)
        elif ay < -threshold:  # Tilted backward
            kolab_y = min(HEIGHT - len(kolab_message), kolab_y + 1)

    initialize_protected_pixels()  # Update protected pixels


def render_image_buffer():
    rgb.image(image_buffer, size=(WIDTH, HEIGHT))

def ko_lab_matrix_animation():
    # Setup accel
    accel.init()
    log("Entering ko_lab_matrix_animation")
    rgb.clear()
    buffer_kolab()  # Draw the KOLAB text once at the start
    initialize_protected_pixels()  # Initialize the protected pixels for the KOLAB text
    initialize_cyan_columns()  # Initialize cyan columns for the Matrix effect
    loop_count = 0
    while True:
        update_kolab_position()  # Update KOLAB text position based on accelerometer input
        buffer_matrix_frame()  # Draw the Matrix background without touching the KOLAB text
        buffer_kolab()  # Redraw KOLAB at the new position
        time.sleep(0.1)  # Add a small delay to control the animation speed
        rgb.clear()
        render_image_buffer()
        loop_count += 1
        if loop_count % 100 == 0:
            log(f"Main loop iteration: {loop_count}")

if __name__ == "__main__":
    log("ko_lab_matrix.py started")
    ko_lab_matrix_animation()
