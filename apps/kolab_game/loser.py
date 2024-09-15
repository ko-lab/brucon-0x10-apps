import random
import time
import rgb

# Constants
WIDTH, HEIGHT = 32, 19
TEXT_COLOR = (255, 0, 0)  # Red color for "LOSER"
FADE_COLOR = (50, 50, 50)  # Darker color for fading background
FALLING_PIXEL_COLOR = (255, 255, 0)  # Yellow falling pixels
FALL_SPEED = 1  # Speed at which letters fall

# LOSER Text
loser_message = [
    " L     OOO  SSS   EEEE RRR  ",
    " L    O   O S     E    R  R ",
    " L    O   O  SS   EEEE RRR  ",
    " L    O   O    S  E    R R  ",
    " LLLL  OOO  SSS   EEEE R  R "
]

def set_pixel(x, y, color):
    """Set a single pixel on the display if it's within bounds."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        rgb.pixel(color, (x, y))

def draw_loser(offsets):
    """Draw the 'LOSER' text in the center of the screen with Y-offsets."""
    y_start = (HEIGHT - len(loser_message)) // 2
    x_start = (WIDTH - len(loser_message[0])) // 2

    for y, line in enumerate(loser_message):
        for x, char in enumerate(line):
            if char != ' ':
                new_y = y_start + y + offsets[y][x]
                if 0 <= new_y < HEIGHT:  # Draw only within screen bounds
                    set_pixel(x_start + x, new_y, TEXT_COLOR)

def fade_background(brightness):
    """Create a fading background effect with adjustable brightness."""
    rgb.background((100,100,100))

def falling_pixels():
    """Create random falling pixels across the screen."""
    for _ in range(5):  # Number of falling pixels
        x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
        set_pixel(x, y, FALLING_PIXEL_COLOR)

def letter_fall_down(offsets):
    """Move letters down one by one, simulating a fall."""
    for y in range(len(loser_message)):
        for x in range(len(loser_message[0])):
            if loser_message[y][x] != ' ':
                offsets[y][x] += FALL_SPEED  # Move letters down
    return offsets

def loser_animation():
    """Run the optimized loser animation loop."""
    brightness = 1.0
    fading_out = True
    initial_phase_duration = 10  # Duration for the initial fade and falling pixel phase
    fall_duration = 3  # Duration for the fall-down effect

    # Initialize fall offsets for each letter in the message
    offsets = [[0 for _ in line] for line in loser_message]

    # Initial animation phase (fading and falling pixels)
    start_time = time.time()
    while time.time() - start_time < initial_phase_duration:
        rgb.clear()

        # Fade the background and draw random falling pixels
        fade_background(brightness)
        falling_pixels()

        # Draw the "LOSER" text
        draw_loser(offsets)

        # Adjust the brightness for the fading effect
        brightness += -0.05 if fading_out else 0.05
        fading_out = brightness <= 0.2 or brightness >= 1.0  # Switch fading direction
        brightness = max(0.2, min(brightness, 1.0))  # Clamp brightness

        time.sleep(0.05)  # Control animation speed

    # Letter fall-down phase
    fall_start_time = time.time()
    while time.time() - fall_start_time < fall_duration:
        rgb.clear()

        # Continue fading the background during the fall-down effect
        fade_background(brightness)

        # Move letters down and draw them falling
        offsets = letter_fall_down(offsets)
        draw_loser(offsets)

        time.sleep(0.1)  # Control fall-down speed

# Run the optimized loser animation
if __name__ == "__main__":
    loser_animation()
