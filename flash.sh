#DEFAULT_PORT=/dev/tty.usbmodem313371
DEFAULT_PORT=/dev/tty.usbmodem01
PORT="${1:-$DEFAULT_PORT}"
esptool.py -p $PORT write_flash 0x10000 brucon_2024_gold_release.bin


esptool.py -p /dev/cu.usbmodem01 --chip esp32s2 --before=no_reset --after=no_reset erase_flash
esptool.py -p /dev/cu.usbmodem01 --chip esp32s2 --before=no_reset --after=no_reset write_flash --flash_mode dio --flash_freq 80m --flash_size 4MB 0x1000 bootloader/bootloader.bin 0x10000 badge_firmware.bin 0x8000 partition_table/partition-table.bin

