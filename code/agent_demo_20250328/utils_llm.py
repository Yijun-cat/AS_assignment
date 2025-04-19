# utils_llm.py
# Call the large language model API

print('import LLM API module')


import os

import qianfan
def llm_qianfan(PROMPT='Hello，who are you？'):
    '''
    Baidu AI Cloud Qianfan Large Model Platform API"
    '''
    
    # input ACCESS_KEY and SECRET_KEY
    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY
    
    # choose LLM
    MODEL = "ERNIE-Bot-4"
    # MODEL = "ERNIE Speed"
    # MODEL = "ERNIE-Lite-8K"
    # MODEL = 'ERNIE-Tiny-8K'

    chat_comp = qianfan.ChatCompletion(model=MODEL)
    
    # Provide as input to the LLM
    resp = chat_comp.do(
        messages=[{"role": "user", "content": PROMPT}], 
        top_p=0.8, 
        temperature=0.3, 
        penalty_score=1.0
    )
    
    response = resp["result"]
    return response

import openai
from openai import OpenAI
from API_KEY import *
def llm_yi(message):
    '''
    lingyiwanwu LLM API
    '''
    
    API_BASE = "https://api.lingyiwanwu.com/v1"
    API_KEY = YI_KEY

    MODEL = 'yi-large'
    # MODEL = 'yi-medium'
    # MODEL = 'yi-spark'
    
    # Access the LLM API
    client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    completion = client.chat.completions.create(model=MODEL, messages= message)
    result = completion.choices[0].message.content.strip()
    return result
    
