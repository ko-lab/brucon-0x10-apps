PORT=/dev/cu.usbmodem313371


PORT=${1:-$PORT}

python3 -m mpremote connect port:$PORT $2

