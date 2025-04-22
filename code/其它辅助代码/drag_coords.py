# drag_coords.py
# Demo：drag teaching （ real-time coordinates ）

# import toolkits
from pymycobot.mycobot280 import MyCobot280
from pymycobot import PI_PORT, PI_BAUD
import time

# connect to the arm
mc = MyCobot280(PI_PORT, PI_BAUD)

# reset the arm to original position
mc.send_angles([0, 0, 0, 0, 0, 0], 60)
time.sleep(3)

# move the robot arm to the table surface
mc.send_angles([0, -90, 0, 0, 0, 0], 40)
time.sleep(3)

# release all servo motors
mc.release_all_servos()
time.sleep(1)

# get real-time coordinates and print out
start = time.time()
while time.time()-start < 60: # within a period of time

    try:
        # get current coordinates
        coords = mc.get_coords()
        
        # extract coordinate values
        X, Y, Z, Rx, Ry, Rz = coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]
        
        # print coordinate values
        print('X{:7}  Y{:7}  Z{:7}  Rx{:9}  Ry{:7}  Rz{:7}'.format(X, Y, Z, Rx, Ry, Rz))
    except:
        pass