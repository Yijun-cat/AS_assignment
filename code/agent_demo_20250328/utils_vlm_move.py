# utils_vlm_move.py
# Input a command, have the multimodal model recognize the image, and use the suction pump to pick up and move the object

from utils_robot import *
from utils_asr import *
from utils_vlm import *

import time

def vlm_move(PROMPT='Put the green block on Peppa Pig', input_way='keyboard'):
    '''
    multimodal model recognize the image, and use the suction pump to pick up and move the object
    input_way: speech input, keyboard input
    '''

    print('Multimodal model recognize the image, and use the suction pump to pick up and move the object')

    # Reset the robotic arm to zero position
    print('Reset the robotic arm to zero position"')
    mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    time.sleep(3)
    
    ## Step 1：Complete hand-eye calibration"
    print('Step 1: Complete hand-eye calibration"')
    
    ## Step 2: Give instruction
    # PROMPT_BACKUP = 'Put the green block on Peppa Pig for me."' # 默认指令
    
    # if input_way == 'keyboard':
    #     PROMPT = input('第二步：输入指令')
    #     if PROMPT == '':
    #         PROMPT = PROMPT_BACKUP
    # elif input_way == 'speech':
    #     record() # 录音
    #     PROMPT = speech_recognition() # 语音识别
    print('Step 2, the instruction is:', PROMPT)
    
    ## Step 3: Capture a top-down view
    print('Step 3: Capture a top-down view')
    top_view_shot(check=False)
    
    ## Step 4: Input the image into the multimodal vision model
    print('Step 4: Input the image into the multimodal vision model')
    img_path = 'temp/vl_now.jpg'
    
    n = 1
    while n < 5:
        try:
            print('   Try the {} time access the multimodal model'.format(n))
            # result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')  # fluctuations in localization accuracy in yi_vision, temporarily switch to the QwenVL series
            result = QwenVL_api(PROMPT, img_path='temp/vl_now.jpg')
            print('    Successfully invoked the multimodal model!')
            print(result)
            break
        except Exception as e:
            print('    Data structure error returned by the multimodal large model. Trying again', e)
            n += 1
    
    ## Step 5: Post-processing and visualization of the visual large model's output results
    print("Step 5: Post-processing and visualization of the visual large model's output results")
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
    
    ## Step 6: Convert hand-eye calibration results to robotic arm coordinates
    print('Step 6: Hand-eye calibration: convert pixel coordinates to robotic arm coordinates')
    # Starting point, robotic arm coordinates
    START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    # Endpoint，robotic arm coordinates
    END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    
    ## Step 7: Use the suction pump to pick up and move the object
    print('Step 7: Use the suction pump to pick up and move the object')
    pump_move(mc=mc, XY_START=[START_X_MC, START_Y_MC], XY_END=[END_X_MC, END_Y_MC])
    
    ## Step 8: Mission complete
    print('Step 8: Mission complete')
    GPIO.cleanup()            # clean up GPIO pin channel
    cv2.destroyAllWindows()   # destory all opencv windows
    # exit()
   
def vlm_vqa(PROMPT='Please count how many blocks are in the picture',input_way='keyboard'):
    # Reset the robotic arm to zero position
    print('Reset the robotic arm to zero position"')
    mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    time.sleep(3)
    print('Step 2, the instruction is:', PROMPT)
    top_view_shot(check=False)
    img_path = 'temp/vl_now.jpg'
    result = QwenVL_api(PROMPT, img_path='temp/vl_now.jpg', vlm_option=1)
    print('    Successfully invoked the multimodal model')
    # print(result)
    GPIO.cleanup()            #  clean up GPIO pin channel
    cv2.destroyAllWindows()   # destory all opencv windows 
    return result

    
    
    
