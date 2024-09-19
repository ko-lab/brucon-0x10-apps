import nvs
import rgb


def main():
    nickname = nvs.get_str("system", 'nickname')
    rgb.scrolltext(nickname)
