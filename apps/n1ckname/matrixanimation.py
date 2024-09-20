import random
import time

import accel
import rgb
from .display_helper import reset_buffer, prepare_pixel_global, render_image_buffer, WIDTH, HEIGHT, image_buffer
from .debug import log
from .messages import brucon_message
CUSTOM_MESSAGE_RATE = 20
import nvs
nickname = nvs.get_str("system", 'nickname')

# Setup RGB
# Matrix Animation Variables
matrix_columns = [random.randint(0, HEIGHT - 1) for _ in range(WIDTH)]  # Y positions of the head of each column

def do_sleep():
    [time.sleep(0.01) for i in range(0,5)]

# KOLAB Text and Protected Area

def calc_cyan_columns(min_cyan=0, max_cyan=3):
    """Randomly select columns to be cyan, between min_cyan and max_cyan."""
    num_cyan = random.randint(min_cyan, max_cyan)
    selected = set()
    while len(selected) < num_cyan:
        col = random.randint(0, WIDTH - 1)
        selected.add(col)
    cyan_columns = list(selected)
    return cyan_columns


def buffer_matrix_frame(cyan_columns):
    """Draw one frame of the Matrix effect."""
    for x in range(WIDTH):
        # Determine the color for the current column
        if x in cyan_columns:
            color = (0, 255, 255)  # Cyan color for special columns
        else:
            color = (255, 0, 0)  # Default green color

        # Move the column's head down by one row
        matrix_columns[x] = (matrix_columns[x] + 1) % HEIGHT

        # Draw the "head" of the column
        prepare_pixel_global((x, matrix_columns[x]), color)
        # Draw the trailing characters with dimmer colors
        for i in range(1, 6):
            char_y = (matrix_columns[x] - i) % HEIGHT
            prepare_pixel_global((x, char_y), (color[0] // (i +1), color[1] // (i + 1), color[2] // (i + 1)))
    return image_buffer

class MatrixAnimation:
    def __init__(self, custom_message):
        # Initial position of KOLAB text (centered)
        self.custom_message = custom_message
        self.message_x = 5
        self.message_y = 2


    def buffer_custom_message(self):
        self._buffer_message(brucon_message)

    def buffer_custom_message(self):
        self._buffer_message(brucon_message)

    def buffer_brucon(self):
        self._buffer_message(brucon_message)

    def buffer_nickname(self):
        rgb.text(nickname, color=(0 ,255 ,0))

    def _buffer_message(self, msg):
        """Draw the 'KOLAB' text at its current position."""
        for y, line in enumerate(msg):
            for x, char in enumerate(line):
                if char != ' ':
                    prepare_pixel_global((self.message_x+ x, self.message_y+y), (0,255 , 0))  # RGB color for KOLAB text

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
        rgb.setbrightness(7)
        cyan_columns = calc_cyan_columns()  # Initialize cyan columns for the Matrix effect
        loop_count = 0
        while keep_showing():
            reset_buffer()
            buffer_matrix_frame(cyan_columns)  # Draw the Matrix background without touching the KOLAB text
            # self.update_message_position()  # Update KOLAB text position based on accelerometer input
            ax, ay, az = accel.get_xyz()
            # if az > 0:
            #     self.buffer_custom_message()
            # else:
            #     self.buffer_brucon()  # Redraw KOLAB at the new position
            rgb.clear()
            render_image_buffer()
            self.buffer_nickname()
            loop_count += 1
            do_sleep()
            if loop_count % 100 == 0:
                log(f"Main loop iteration: {loop_count}")


if __name__ == "__main__":
    log("endgame.py started")
    MatrixAnimation("").show_loop()
