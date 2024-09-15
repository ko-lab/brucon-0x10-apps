from time import sleep

import rgb
count =0
WIDTH =32
HEIGHT=19
rgb.setbrightness(100)
while True:
     # print(count,': x' ,count % WIDTH, 'y', (count//WIDTH) % HEIGHT)
     rgb.pixel((100,0,0), (count % WIDTH, (count//WIDTH) % HEIGHT))
     count = count + 1
     if (count % (32*19)) == 0:
          rgb.clear()
          [sleep(0.01) for i in range(0,10)]

