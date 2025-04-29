# drag_angles.py
# Demo: drag teaching ( real-time angle )

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

# release all servos
mc.release_all_servos()
time.sleep(1)

# get real-time coordinates and print out
start = time.time()
while time.time()-start < 120: # within a certain period of time

    try:
        # get current coordinates
        angles = mc.get_angles()
        
        # extract coordinate values
        A, B, C, D, E, F = angles[0], angles[1], angles[2], angles[3], angles[4], angles[5]
        
        # print coordinate values
        print('A{:7}  B{:7}  C{:7}  D{:7}  E{:7}  F{:7}'.format(A, B, C, D, E, F))
    except:
        pass