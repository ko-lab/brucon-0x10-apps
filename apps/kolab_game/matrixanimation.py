import random
import time

import accel
import rgb
from .display_helper import rgb_to_hex
from .debug import log

# Setup RGB
WIDTH, HEIGHT = 32, 19
image_buffer = [0]*(WIDTH*HEIGHT)
# Matrix Animation Variables
matrix_columns = [random.randint(0, HEIGHT - 1) for _ in range(WIDTH)]  # Y positions of the head of each column
cyan_columns = []  # List to store the indices of cyan columns

# Characters for the Matrix effect (not needed but here to resemble the idea)
matrix_chars = [chr(i) for i in range(33, 127)]  # Printable ASCII characters

# KOLAB Text and Protected Area
def prepare_pixel_global(pos, color):
    global image_buffer
    (posx, posy)= pos
    hex_color = rgb_to_hex(color)
    i = posy*WIDTH+ posx
    image_buffer[i] = hex_color

def render_image_buffer():
        rgb.image(image_buffer, pos=(0,0), size=(WIDTH, HEIGHT))

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
        prepare_pixel_global((x, matrix_columns[x]), color)

        # Draw the trailing characters with dimmer colors
        for i in range(1, 4):
            char_y = (matrix_columns[x] - i) % HEIGHT
            prepare_pixel_global((x, char_y), (color[0], color[1] // (i + 1), color[2] // (i + 1)))

class MatrixAnimation:
    def __init__(self, custom_message):
        # Initial position of KOLAB text (centered)
        self.custom_message = custom_message
        self.message_x = (WIDTH - len(self.custom_message[0])) // 2
        self.message_y = (HEIGHT - len(self.custom_message)) // 2


    def buffer_message(self):
        """Draw the 'KOLAB' text at its current position."""
        for y, line in enumerate(self.custom_message):
            for x, char in enumerate(line):
                if char != ' ':
                    prepare_pixel_global((self.message_x+ x, self.message_y+y), (11, 118, 187))  # RGB color for KOLAB text

    def update_message_position(self):
        """Update the KOLAB text position based on accelerometer input."""
        ax, ay, az = accel.get_xyz()

        # Adjust the sensitivity as needed
        threshold = 5
        if az < -threshold:  # Device held upright (neutral position)
            self.message_x = (WIDTH - len(self.custom_message[0])) // 2
            self.message_y = (HEIGHT - len(self.custom_message)) // 2
        else:
            if ax > threshold:  # Tilted right
                self.message_x = max(0, self.message_x - 1)
            elif ax < -threshold:  # Tilted left
                self.message_x = min(WIDTH - len(self.custom_message[0]), self.message_x + 1)

            if ay > threshold:  # Tilted forward
                self.message_y = max(0, self.message_y - 1)
            elif ay < -threshold:  # Tilted backward
                self.message_y = min(HEIGHT - len(self.custom_message), self.message_y + 1)


    def show_loop(self, keep_showing = lambda: True):
        # Setup accel
        accel.init()
        log("Entering ko_lab_matrix_animation")
        rgb.clear()
        if self.custom_message != '':
            self.buffer_message()  # Draw the KOLAB text once at the start
        render_image_buffer()
        initialize_cyan_columns()  # Initialize cyan columns for the Matrix effect
        loop_count = 0
        while keep_showing():
            buffer_matrix_frame()  # Draw the Matrix background without touching the KOLAB text
            if self.custom_message != '':
                self.update_message_position()  # Update KOLAB text position based on accelerometer input
                self.buffer_message()  # Redraw KOLAB at the new position
            rgb.clear()
            render_image_buffer()
            loop_count += 1
            time.sleep(0.05)  # Add a small delay to control the animation speed
            if loop_count % 100 == 0:
                log(f"Main loop iteration: {loop_count}")


if __name__ == "__main__":
    log("endgame.py started")
    MatrixAnimation("").show_loop()
