#!/bin/bash
DEFAULT_PORT=/dev/cu.usbmodem313371
# Default directory
DEFAULT_DIR="kolab_game"

# Use the first argument if provided, otherwise use the default
APP_DIR="${1:-$DEFAULT_DIR}"
PORT="${2:-$DEFAULT_PORT}"
echo "uploading app [$APP_DIR] to $PORT"

python3 -m mpremote connect port:$PORT fs mkdir :apps 1>/dev/null 2>/dev/null
python3 -m mpremote connect port:$PORT fs mkdir :apps/$APP_DIR 1>/dev/null 2>/dev/null
for file in apps/$APP_DIR/*; do
  python3 -m mpremote connect port:$PORT fs cp $file :$file || exit 1
done

python3 -m mpremote connect port:$PORT fs mkdir :None 1>/dev/null 2>/dev/null
python3 -m mpremote connect port:$PORT fs mkdir :None/$APP_DIR 1>/dev/null 2>/dev/null
python3 -m mpremote connect port:$PORT fs cp apps/$APP_DIR/icon.py :None/$APP_DIR/icon.py
python3 -m mpremote connect port:$PORT fs cp apps/$APP_DIR/metadata.json :None/$APP_DIR/metadata.json
