import buttons
import time
import rgb
import accel

def clear_display(button_is_down, button_name):
    print('BUTTON '+button_name+' Callback! down: '+ str(button_is_down))
    if button_is_down:
        rgb.background((200, 200, 200))
        time.sleep(0.2)
        rgb.clear()
        pass

def setup_button_callback():
    buttons.register(buttons.BTN_A, lambda down: clear_display(down, 'A'))
    buttons.register(buttons.BTN_B, lambda down: clear_display(down, 'B'))
    buttons.register(buttons.BTN_UP, lambda down: clear_display(down, 'UP'))
    buttons.register(buttons.BTN_DOWN, lambda down: clear_display(down, 'DOWN'))
    buttons.register(buttons.BTN_LEFT, lambda down: clear_display(down, 'LEFT'))
    buttons.register(buttons.BTN_RIGHT, lambda down: clear_display(down, 'RIGHT'))


def test_image():
    data = [0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff]
    rgb.clear()
    rgb.image(data, pos=(12, 0), size=(8, 8))

def print_accel():
    print("accel"+str(accel.get_xyz()))

def main():
    print("Entering main function")
    # accel.init()
    # setup_button_callback()
    rgb.setbrightness(1)
    rgb.background((0,50,0))
    time.sleep(1)
    count = 0
    while True:
        # print_accel()
        # test_image()
        # time.sleep(0.1)
        rgb.pixel((1, 0, 0), (0, 0))
        if (count % 100) == 0:
            rgb.clear()
            time.sleep(0.01)
        print('count: '+str(count))
        count = count + 1




if __name__ == "__main__":
    print("Script started")
    main()
