# agent_go.py
# Robotic arm + large model + multimodality + speech recognition = embodied intelligent agent

print('\nAn embodied intelligent robotic arm that can understand human speech, interpret images, and recognize actions.')

# import common functions
from utils_asr import *             # recording + speech recognition
from utils_robot import *           # connect the robotic arm
from utils_llm import *             # LLM API
from utils_led import *             # Control LED color
from utils_camera import *          # Camera
from utils_robot import *           # Robotic arm motion
from utils_pump import *            # GPIO, suction pump
from utils_vlm_move import *        # multimodal model recognize the image, use the suction pump to pick up and move the objec
from utils_drag_teaching import *   # Drag teaching
from utils_agent import *           # Intelligent agent action arrangement
from utils_tts import *             # speech synthesis

# print('play welcome message')
pump_off()
# back_zero()
play_wav('asset/welcome.wav')

message=[]
message.append({"role":"system","content":AGENT_SYS_PROMPT})
def agent_play():
    '''
    Main function, voice control action arragnement of agent
    '''
    # back to original position
    back_zero()
    
    # print('test camera')
    # check_camera()
    
    # input command
    # First return to the origin, then change the LED light to dark green, and finally place the green block on the basketball
    start_record_ok = input(
        "Start recording or not? Enter a number to specify the recording duration, press 'k' to type your input, or press 'c' to enter the default command.\n"
        )
    if str.isnumeric(start_record_ok):
        DURATION = int(start_record_ok)
        record(DURATION=DURATION)   # speech recording
        order = speech_recognition() # speech recognition
    elif start_record_ok == 'k':
        order = input('Please enter a command')
    elif start_record_ok == 'c':
        order = 'first return to the origin, then shake head, and lastly place the green block on the basketball'
    else:
        print('No command, exit')
        # exit()
        raise NameError('No command, exit')
    
    # Agent action arrangement
    message.append({"role": "user", "content": order})
    agent_plan_output = eval(agent_plan(message))
    
    print('Motion arrangement of agent\n', agent_plan_output)
    # plan_ok = input("Continue or not？ press 'c' continue, press 'q' to quit")
    plan_ok = 'c'
    if plan_ok == 'c':
        response = agent_plan_output['response'] # Retrieve what the robot wants to say to me
        print('Start speech synthesis')
        tts(response)                     # Synthesize speech and export it as a WAV audio file
        play_wav('temp/tts.wav')          # play the audio file of speech synthesis
        output_other=''
        for each in agent_plan_output['function']: # Execute each function of action arrangement
            print('Start executing actions', each)
            ret=eval(each)
            if ret!=None:
                output_other=ret
    elif plan_ok =='q':
        # exit()
        raise NameError("Press 'q' to quit")
    agent_plan_output['response']+='.'+ output_other
    message.append({"role":"assistant","content":str(agent_plan_output)})

# agent_play()
if __name__ == '__main__':
    while True:
        agent_play()

