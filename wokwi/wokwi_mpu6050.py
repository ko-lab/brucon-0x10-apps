from machine import I2C, Pin
import ustruct
import time

class MPU6050:
    # MPU6050 Registers and their Addresses
    MPU6050_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B

    def __init__(self, i2c):
        self.i2c = i2c
        self.address = self.MPU6050_ADDR
        time.sleep(1)  # Add delay after initializing I2C
        self.i2c.writeto_mem(self.address, self.PWR_MGMT_1, b'\x00')  # Wake up MPU6050

    def read_raw_data(self, register):
        # Read 2 bytes of data from the given register
        high = self.i2c.readfrom_mem(self.address, register, 1)
        low = self.i2c.readfrom_mem(self.address, register + 1, 1)
        value = ustruct.unpack('>h', high + low)[0]
        return value

    def acceleration(self):
        ax = self.read_raw_data(self.ACCEL_XOUT_H)
        ay = self.read_raw_data(self.ACCEL_XOUT_H + 2)
        az = self.read_raw_data(self.ACCEL_XOUT_H + 4)

        # Convert to 'g' units (1g = 9.81m/s^2)
        accel_scale_modifier = 16384.0  # Assumes the accelerometer is set to +/- 2g
        ax = ax / accel_scale_modifier
        ay = ay / accel_scale_modifier
        az = az / accel_scale_modifier

        return (ax, ay, az)