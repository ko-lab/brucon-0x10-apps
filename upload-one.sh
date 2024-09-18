#!/bin/bash
DEFAULT_PORT=/dev/cu.usbmodem313371
# Default directory
DEFAULT_DIR="apps/kolab_game"

# Use the first argument if provided, otherwise use the default
APP_DIR="${1:-$DEFAULT_DIR}"
PORT="${2:-$DEFAULT_PORT}"
echo "uploading app [$APP_DIR] to $PORT"
python3 -m mpremote connect port:$PORT fs mkdir :$APP_DIR 1>/dev/null 2>/dev/null
for file in $APP_DIR/*.py; do
  python3 -m mpremote connect port:$PORT fs cp $file :$file
done
