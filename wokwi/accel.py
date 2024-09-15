from wokwi_check import is_wokwi

if is_wokwi:
    import wokwi_accel as accel
else:
    import fri3d2020_accel as accel

def init():
    accel.init()

def get_xyz():
    return accel.get_xyz()
