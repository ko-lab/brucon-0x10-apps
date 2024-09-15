import wokwi_mpu6050
from machine import Pin, I2C

class Accel:
  def __init__(self):
    # Setup accelerometer
    print("Setting up I2C and Accelerometer")
    self.i2c = I2C(0, sda=Pin(18), scl=Pin(19))  # Use I2C0 with GPIO 8 (SDA) and GPIO 9 (SCL)
    try:
        self.mpu = mpu6050.MPU6050(self.i2c)
        print("MPU6050 initialized successfully")
    except Exception as e:
        print(f"Error initializing MPU6050: {e}")
        self.mpu = None
  def get_xyz(self):
    return self.mpu.acceleration()

_accel = None

def init():
  global _accel  # Declare _accel as global to modify the global variable
  _accel = Accel()

def get_xyz():
  return _accel.get_xyz()
