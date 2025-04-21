# utils_vlm.py
# Multimodal model, Visualization

import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw

print('Import vision model')

# Import English font，specify size
font = ImageFont.truetype('asset/arial.ttf', 26)

from API_KEY import *
from utils_tts import *
OUTPUT_VLM = ''
# System prompt
SYSTEM_PROMPT_CATCH = '''
I will provide a command for the robotic arm. 
Please extract the starting object and ending object from this command, locate the top-left and bottom-right pixel coordinates of these two objects in the image, and output the data in JSON format.

e.g., If my instruction is: Place the red block on top of the house.
你输出这样的格式：
{
 "start":"red block",
 "start_xyxy":[[102,505],[324,860]],
 "end":"house",
 "end_xyxy":[[300,150],[476,310]]
}

Only reply with the JSON itself; do not include any other content

My current instruction is:
'''

SYSTEM_PROMPT_VQA = '''
Tell me the name, category, and function of each object in the image. Describe each object in one sentence.

Example:
Plate, household item, holding things
Loratadine Tablets, medicine, treatment for allergies

My current instruction is:
'''


# Yi-Vision function

import openai
from openai import OpenAI
import base64

def yi_vision_api(PROMPT='Put the red block on the pen', img_path='temp/vl_now.jpg', vlm_option=0):

    '''
    LingYiWanWu Model Open Platform, Visual-Language Multimodal Model API"
    '''
    if vlm_option==0:
        SYSTEM_PROMPT=SYSTEM_PROMPT_CATCH
    elif vlm_option==1:
        SYSTEM_PROMPT=SYSTEM_PROMPT_VQA
        
    client = OpenAI(
        api_key=YI_KEY,
        base_url="https://api.lingyiwanwu.com/v1"
    )
    
    # Encode to base64
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
    
    # Send a request to the large model
    completion = client.chat.completions.create(
      model="yi-vision",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT + PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    # Parse the results returned by the large model
    if vlm_option == 0: #localization task
        result = eval(completion.choices[0].message.content.strip())
    elif vlm_option == 1: # Visual Question Answering (VQA) task
        result = completion.choices[0].message.content.strip()
        print(result)
        tts(result)  # speech synthesis, export wav audio file
        play_wav('temp/tts.wav')  # play speech synthesis audio file
    print('    Large model invoked successfully!')
    
    return result


def QwenVL_api(PROMPT='Put the red block on the pen', img_path='temp/vl_now.jpg', vlm_option=0):
    '''
    通义千问QwenVL视觉语言多模态大模型API，模型列表请见：https://help.aliyun.com/zh/model-studio/getting-started/models?spm=0.0.0.i3#9f8890ce29g5u
    '''
    if vlm_option==0:
        SYSTEM_PROMPT=SYSTEM_PROMPT_CATCH
    elif vlm_option==1:
        SYSTEM_PROMPT=SYSTEM_PROMPT_VQA
        
    client = OpenAI(
        api_key=Qwen_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # Encode to base64
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')

    # Send a request to the large model
    completion = client.chat.completions.create(
        model="qwen-vl-max-2024-11-19",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT + PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image
                        }
                    }
                ]
            },
        ]
    )

    # Parse the results returned by the large model
    if vlm_option == 0: # localization task
        result = eval(completion.choices[0].message.content.strip())
    elif vlm_option == 1: # Visual Question Answering (VQA) task
        result = completion.choices[0].message.content.strip()
        print(result)
        tts(result)  # speech synthesis, export wav audio file
        play_wav('temp/tts.wav')  # play speech synthesis audio file j
    print('    Large model invoked successfully')

    return result

def post_processing_viz(result, img_path, check=False):
    
    '''
    Post-processing and visualization of vision large model outputs
    check: Is manual confirmation needed on the screen? press q to continue or quit
    '''

    # Post-processing
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # scale factor
    FACTOR = 999
    # Start object name
    START_NAME = result['start']
    # End object name
    END_NAME = result['end']
    # Starting point, top-left pixel coordinates
    START_X_MIN = int(result['start_xyxy'][0][0] * img_w / FACTOR)
    START_Y_MIN = int(result['start_xyxy'][0][1] * img_h / FACTOR)
    # Starting point, bottom-right pixel coordinates
    START_X_MAX = int(result['start_xyxy'][1][0] * img_w / FACTOR)
    START_Y_MAX = int(result['start_xyxy'][1][1] * img_h / FACTOR)
    # Starting point, center pixel coordinates
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # Endpoint, top-left pixel coordinates
    END_X_MIN = int(result['end_xyxy'][0][0] * img_w / FACTOR)
    END_Y_MIN = int(result['end_xyxy'][0][1] * img_h / FACTOR)
    # Endpoint, bottom-right pixel coordinates
    END_X_MAX = int(result['end_xyxy'][1][0] * img_w / FACTOR)
    END_Y_MAX = int(result['end_xyxy'][1][1] * img_h / FACTOR)
    # Endpoint, center pixel coordinates
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    
    # Visualization
    # Draw a bounding box around the starting object
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # Draw the center point of the starting object
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # Draw a bounding box around the end object
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # Draw the center point of the end object
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # write object name
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR 转 RGB
    img_pil = Image.fromarray(img_rgb) # array 转 pil
    draw = ImageDraw.Draw(img_pil)
    # write starting object name
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # coordinates, name, font, rgb color
    # write end object name
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # coordinates, name, font, rgb color
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB to BGR
    # Save the visualization image
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)

    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # Display the visualization image on the screen
    cv2.imshow('zihao_vlm', img_bgr) 

    if check:
        print('   Please confirm that the visualization was successful, press c continue, press q exit')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # press c continue
                break
            if key == ord('q'): # press q exit
                # exit()
                cv2.destroyAllWindows()
                raise NameError('press q exit')
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass

    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER
