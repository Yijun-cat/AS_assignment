# utils_robot.py
# Start and connect the robotic arm, and import toolkits

print('Imort arm connection module')

from pymycobot.mycobot280 import MyCobot280
from pymycobot import PI_PORT, PI_BAUD
import cv2
import numpy as np
import time
from utils_pump import *

# connect arm
mc = MyCobot280(PI_PORT, PI_BAUD)
# Set motion mode to interpolation
mc.set_fresh_mode(0)

import RPi.GPIO as GPIO
# Initialize GPIO
GPIO.setwarnings(False)   # do not print warning info
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(20, 1)        # Turn off the suction pump solenoid valve

def back_zero():
    '''
    Reset the robotic arm to zero position
    '''
    print('Reset the robotic arm to zero position')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)

def relax_arms():
    print('Release all servos')
    mc.release_all_servos()

def head_shake():
    # head shake
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    time.sleep(1)
    for count in range(2):
        mc.send_angle(5, 30, 80)
        time.sleep(0.5)
        mc.send_angle(5, -30,80)
        time.sleep(0.5)
    # mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    # time.sleep(1)
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(2)

def head_dance():
    # dance
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    time.sleep(1)
    for count in range(1):
        mc.send_angles([(-0.17),(-94.3),118.91,(-39.9),59.32,(-0.52)],80)
        time.sleep(1.2)
        mc.send_angles([67.85,(-3.42),(-116.98),106.52,23.11,(-0.52)],80)
        time.sleep(1.7)
        mc.send_angles([(-38.14),(-115.04),116.63,69.69,3.25,(-11.6)],80)
        time.sleep(1.7)
        mc.send_angles([2.72,(-26.19),140.27,(-110.74),(-6.15),(-11.25)],80)
        time.sleep(1)
        mc.send_angles([0,0,0,0,0,0],80)

def head_nod():
    # nod
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    for count in range(2):
        mc.send_angle(4, 13, 70)
        time.sleep(0.5)
        mc.send_angle(4, -20, 70)
        time.sleep(1)
        mc.send_angle(4,13,70)
        time.sleep(0.5)
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)

def move_to_coords(X=150, Y=-130, HEIGHT_SAFE=230):
    print('Move to the specified coordinates：X {} Y {}'.format(X, Y))
    mc.send_coords([X, Y, HEIGHT_SAFE, 0, 180, 90], 20, 0)
    time.sleep(4)

def single_joint_move(joint_index, angle):
    print('Joint {} move to {} degree(s)'.format(joint_index, angle))
    mc.send_angle(joint_index, angle, 40)
    time.sleep(2)

def move_to_top_view():
    print('Move to top view')
    mc.send_angles([-62.13, 8.96, -87.71, -14.41, 2.54, -16.34], 10)
    time.sleep(3)

def top_view_shot(check=False):
    '''
    Take a picture and save
    check：Is manual confirmation needed on the screen that the photo was taken successfully, and press the 'q' to continue?
    '''
    print('Move to top view')
    move_to_top_view()
    
    # Acquire the camera; passing in 0 means to use the system's default camera
    cap = cv2.VideoCapture(0)
    # open cap
    cap.open(0)
    time.sleep(0.3)
    success, img_bgr = cap.read()
    
    # save image
    print('    save to temp/vl_now.jpg')
    cv2.imwrite('temp/vl_now.jpg', img_bgr)

    # show image on the screen
    cv2.destroyAllWindows()   # destory all opencv windows
    cv2.imshow('zihao_vlm', img_bgr) 
    
    if check:
        print( "Plese confirm that the photo was taken successfully，press press 'c' to continue，'q' to quit" )
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # press c to continue
                break
            if key == ord('q'): # press q to quit
                # exit()
                cv2.destroyAllWindows()   # destory all opencv windows
                raise NameError("press 'q' to quit")
    else:
        if cv2.waitKey(10) & 0xFF == None:
            pass
        
    # turn off camera
    cap.release()
    # close the image window
    # cv2.destroyAllWindows()

def eye2hand(X_im=160, Y_im=120):
    '''
    Input the target point's pixel coordinates in the image and convert them to the robotic arm's coordinates
    '''

    # Organize the coordinates of the two calibration points
    cali_1_im = [130, 290]                       # Bottom-left corner, Pixel coordinates of the first calibration point:*(must be filled manually!)
    cali_1_mc = [-21.8, -197.4]                  # Bottom-left corner, Robotic arm coordinates of the first calibration point:*(must be filled manually)
    cali_2_im = [640, 0]                         # Top-right corner, Pixel coordinates of the second calibration point:
    cali_2_mc = [215, -59.1]                    # Top-right corner, Robotic arm coordinates of the second calibration point:*(must be filled manually)

    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]     # Pixel coordinates
    X_cali_mc = [cali_1_mc[0], cali_2_mc[0]]     # Arm coordianates
    Y_cali_im = [cali_2_im[1], cali_1_im[1]]     # Pixel coordinates: Input in ascending order (small → large).
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]     # Robotic arm coordinates: Input in descending order (large → small).

    # X offset
    X_mc = int(np.interp(X_im, X_cali_im, X_cali_mc))

    # Y offset
    Y_mc = int(np.interp(Y_im, Y_cali_im, Y_cali_mc))

    return X_mc, Y_mc

# Pick up and move the object with the suction pump.
def pump_move(mc, XY_START=[230,-50], HEIGHT_START=90, XY_END=[100,220], HEIGHT_END=100, HEIGHT_SAFE=220):

    '''
    用吸泵，将物体从起点吸取移动至终点

    mc：机械臂实例
    XY_START：起点机械臂坐标
    HEIGHT_START：起点高度，方块用90
    XY_END：终点机械臂坐标
    HEIGHT_END：终点高度
    HEIGHT_SAFE：搬运途中安全高度
    '''
    
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    # 设置运动模式为插补
    mc.set_fresh_mode(0)
    
    # # Reset the robotic arm to zero position
    # print('    Reset the robotic arm to zero position')
    # mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    # time.sleep(4)
    
    # 吸泵移动至物体上方
    print('    吸泵移动至物体上方')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 20, 0)
    time.sleep(4)

    # 开启吸泵
    pump_on()
    
    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_START, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 升起物体
    print('    升起物体')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 向下放下物体
    print('    向下放下物体')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_END, 0, 180, 90], 20, 0)
    time.sleep(3)

    # 关闭吸泵
    pump_off()

    # Reset the robotic arm to zero position
    print('    Reset the robotic arm to zero position')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)
