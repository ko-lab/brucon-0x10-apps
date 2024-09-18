import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Get the list of device files in /dev/
def list_dev_devices():
    try:
        # List all device files in /dev/
        dev_files = [f for f in os.listdir('/dev/') if f.startswith('tty')]
        return dev_files
    except Exception as e:
        print(f"Error listing /dev/ devices: {e}")
        return []

# Run the external script to install the app for the detected device
def run_install_script(device_path, retries=3):
    script_path = './install-app.sh'
    success = False
    for attempt in range(1, retries + 1):
        print(f"Attempt {attempt}: Running install script for {device_path}...")
        try:
            subprocess.run([script_path, device_path], check=True)
            success = True
            break
        except subprocess.CalledProcessError:
            print(f"Install script failed on attempt {attempt}. Retrying...")
            time.sleep(1)
        except OSError as e:
            print(f"Error executing script: {e}")
            break  # Stop retrying if there is a format error

    if success:
        print(f"Installation successful for {device_path}")
    else:
        print(f"Installation failed for {device_path} after 3 attempts")
    
    return success

# Handle the installation process for a new device
def handle_new_device(device):
    device_path = f"/dev/{device}"
    print(f"New device detected: {device_path}")
    # Attempt to run the install script with the device path
    run_install_script(device_path)

blocklist = set(list_dev_devices())
busy_list = set()

# Main logic
def main():
    # Initial blocklist of current devices in /dev/
    global busy_list
    print("Monitoring /dev/ for new devices...")
    
    with ThreadPoolExecutor() as executor:
        futures = {}
        while True:
            time.sleep(1)

            # Get the current list of devices in /dev/
            current_devices = set(list_dev_devices())

            # Detect new devices (those not in the blocklist)
            new_devices = current_devices - blocklist - busy_list
            busy_list = busy_list & current_devices
            for device_path in new_devices:
                busy_list.add(device_path) 
                # Submit each new device to the thread pool
                future = executor.submit(handle_new_device, device_path)
                futures[future] = device_path

            # Check for completed futures (optional, for logging or error handling)
            for future in as_completed(futures):
                device = futures[future]
                try:
                    future.result()  # Fetch result to check for exceptions
                except Exception as e:
                    print(f"Error handling device {device}: {e}")

if __name__ == "__main__":
    main()

