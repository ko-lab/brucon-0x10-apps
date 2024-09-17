PORT=/dev/cu.usbmodem313371

#python3 -m mpremote connect port:$PORT run __init__.py
DEFAULT_DIR="apps/kolab_game"

# Use the first argument if provided, otherwise use the default
APP_DIR="${1:-$DEFAULT_DIR}"
python3 -m mpremote connect port:$PORT mount $APP_DIR run $APP_DIR/__init__.py

