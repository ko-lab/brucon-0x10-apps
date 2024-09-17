import random
import random
import time

import accel
import rgb
from .display_helper import rgb_to_hex
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
def prepare_pixel_global(pos, color):
    global image_buffer
    (posx, posy)= pos
    hex_color = rgb_to_hex(color)
    i = posy*WIDTH+ posx
    image_buffer[i] = hex_color

kolab_protected_pixels = []

def is_protected_pixel(x, y):
    """Check if the given pixel is part of the KOLAB text."""
    return (x, y) in kolab_protected_pixels

def render_image_buffer():
        rgb.image(image_buffer, pos=(0,0), size=(WIDTH, HEIGHT))


class MatrixAnimation:
    def __init__(self, kolab_message):
        # Initial position of KOLAB text (centered)
        self.kolab_message = kolab_message
        self.kolab_x = (WIDTH - len(self.kolab_message[0])) // 2
        self.kolab_y = (HEIGHT - len(self.kolab_message)) // 2

    def initialize_protected_pixels(self):
        """Determine the pixels where the KOLAB text is located to protect them from the Matrix animation."""
        kolab_protected_pixels.clear()
        for y, line in enumerate(self.kolab_message):
            for x, char in enumerate(line):
                if char != ' ':
                    kolab_protected_pixels.append((self.kolab_x + x, self.kolab_y + y))



    def initialize_cyan_columns(min_cyan=0, max_cyan=3):
        """Randomly select columns to be cyan, between min_cyan and max_cyan."""
        global cyan_columns
        num_cyan = random.randint(min_cyan, max_cyan)
        selected = set()
        while len(selected) < num_cyan:
            col = random.randint(0, WIDTH - 1)
            selected.add(col)
        cyan_columns = list(selected)

    def buffer_matrix_frame(self):
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


    def buffer_kolab(self):
        """Draw the 'KOLAB' text at its current position."""
        for y, line in enumerate(self.kolab_message):
            for x, char in enumerate(line):
                if char != ' ':
                    prepare_pixel_global((self.kolab_x+ x, self.kolab_y+y), (11, 118, 187))  # RGB color for KOLAB text

    def update_kolab_position(self):
        """Update the KOLAB text position based on accelerometer input."""
        ax, ay, az = accel.get_xyz()

        # Adjust the sensitivity as needed
        threshold = 5
        if az < -threshold:  # Device held upright (neutral position)
            self.kolab_x = (WIDTH - len(self.kolab_message[0])) // 2
            self.kolab_y = (HEIGHT - len(self.kolab_message)) // 2
        else:
            if ax > threshold:  # Tilted right
                self.kolab_x = max(0, self.kolab_x - 1)
            elif ax < -threshold:  # Tilted left
                self.kolab_x = min(WIDTH - len(self.kolab_message[0]), self.kolab_x + 1)

            if ay > threshold:  # Tilted forward
                self.kolab_y = max(0, self.kolab_y - 1)
            elif ay < -threshold:  # Tilted backward
                self.kolab_y = min(HEIGHT - len(self.kolab_message), self.kolab_y + 1)

        self.initialize_protected_pixels()  # Update protected pixels


    def show_loop(self):
        # Setup accel
        accel.init()
        log("Entering ko_lab_matrix_animation")
        rgb.clear()
        # print('ko_lab_matrix_animation: clear done')
        render_image_buffer()
        #     print('ko_lab_matrix_animation: initial render done')
        self.buffer_kolab()  # Draw the KOLAB text once at the start
        render_image_buffer()
        #     print('ko_lab_matrix_animation: buffer+render kolab done')
        self.initialize_protected_pixels()  # Initialize the protected pixels for the KOLAB text
        #     print('ko_lab_matrix_animation: initialize_protected_pixels done')
        self.initialize_cyan_columns()  # Initialize cyan columns for the Matrix effect
        #     print('ko_lab_matrix_animation: init_cyan done')
        loop_count = 0
        while True:
            self.update_kolab_position()  # Update KOLAB text position based on accelerometer input
            #         print('ko_lab_matrix_animation: loop update_kolab_pos done')
            self.buffer_matrix_frame()  # Draw the Matrix background without touching the KOLAB text
            #         print('ko_lab_matrix_animation: loop buffer_matrix_frame done')
            self.buffer_kolab()  # Redraw KOLAB at the new position
            #         print('ko_lab_matrix_animation: loop buffer_kolab done')
            time.sleep(0.05)  # Add a small delay to control the animation speed
            rgb.clear()
            #         print('ko_lab_matrix_animation: loop clear done')
            render_image_buffer()
            #         print('ko_lab_matrix_animation: loop render done')
            loop_count += 1
            if loop_count % 100 == 0:
                log(f"Main loop iteration: {loop_count}")


if __name__ == "__main__":
    log("endgame.py started")

    endGame = MatrixAnimation("").show_loop()
