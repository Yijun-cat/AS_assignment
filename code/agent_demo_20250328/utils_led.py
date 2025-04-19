# utils_led.py
# Change LED color using LLM

from utils_llm import llm_qianfan, llm_yi
from utils_robot import mc

print('import LED control module')

# Alternative colors
# Lake Baikal, Chinese Red, Ocean Blue, Green Leaf, Gold, Sapphire Blue, Peppa Pig, Dark Green, Black

# system prompt
SYS_PROMPT = 'The following sentence contains a target object.'
'Help me return one possible color of this object in the form of RGB pixel values (ranging from 0 to 255), formatted as a tuple, '
'for example, (255, 30, 60). Reply with the tuple itself, starting with parentheses, '
'and do not include any language content. Here is the sentence:'

def llm_led(PROMPT_LED='Help me change the color of the LED light to the color of Lake Baikal'):
    '''
    Change LED color using LLM
    '''
    
    PROMPT = SYS_PROMPT + PROMPT_LED
    
    n = 1
    while n < 5:
        try:
            # Call LLM API
            # response = llm_qianfan(PROMPT) 
            response = llm_yi(PROMPT) 
            
            # Extrace color
            rgb_tuple = eval(response)
        
            # Set RGB color
            mc.set_color(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
            print('Changed LED color', rgb_tuple)

            break
            
        except Exception as e:
            print('The model returned an invalid JSON structure. Try again.', e)
            n += 1