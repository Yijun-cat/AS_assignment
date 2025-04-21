
# recording + speech recognition

print('import recording + speech recognition module')

import pyaudio
import wave
import numpy as np
import os
import sys
from API_KEY import *

# Confirm device number
# import sounddevice as sd
# print(sd.query_devices())

def record(MIC_INDEX=0, DURATION=5):
    '''
    To use the microphone for recording, you need to obtain the microphone ID with the 'arecord -l' command.
    DURATION: Recording duration
    '''
    print('Start {} seconds recording'.format(DURATION))
    os.system('sudo arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(MIC_INDEX, DURATION))
    print('Recording ended')

def record_auto(MIC_INDEX=1):
    '''
    Start microphone recording and save it to the 'temp/speech_record.wav' audio file
    Recording automatically starts when the volume exceeds the threshold, and automatically stops after the volume stays below the threshold for a couple of seconds.
    MIC_INDEX：microphone device number
    '''
    
    CHUNK = 1024               # Sampling width
    RATE = 16000               # Sampling rate
    
    QUIET_DB = 2000            # Decibel threshold—start recording if above, stop if below

    delay_time = 1             # After the sound drops to the decibel threshold, the duration before recording automatically stops
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2 # Number of channels
    
    # initialize recording
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_INDEX
                   )
    
    frames = []             # All audio frames
    
    flag = False            # Whether recording has started
    quiet_flag = False      # Current volume is below the threshold
    
    temp_time = 0           # Which frame is the current time
    last_ok_time = 0        # Which frame was the last valid (normal) one
    START_TIME = 0          # Which frame recording started at
    END_TIME = 0            # Which frame recording ended at
    
    print('可以说话啦！')
    
    while True:
        
        # get sound of current chunk
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        # get sound level(dB) of current chunk
        temp_volume = np.max(np.frombuffer(data, dtype=np.short))
        
        if temp_volume > QUIET_DB and flag==False:
            print("Volume is higher than threshold，start recording")
            flag =True
            START_TIME = temp_time
            last_ok_time = temp_time
    
        if flag: # Different scenarios during recording
    
            if(temp_volume < QUIET_DB and quiet_flag==False):
                print("Recording， current volume is lower than threshold")
                quiet_flag = True
                last_ok_time = temp_time
                
            if(temp_volume > QUIET_DB):
                # print('recording，current volume higher than threshold，default recording')
                quiet_flag = False
                last_ok_time = temp_time
    
            if(temp_time > last_ok_time + delay_time*15 and quiet_flag==True):
                print("Volume lower than threshold, after {:.2f} seconds，measure current volume".format(delay_time))
                if(quiet_flag and temp_volume < QUIET_DB):
                    print("Current volume still lower than threshold，end recording")
                    END_TIME = temp_time
                    break
                else:
                    print("Current volume higher than threshold again，continue recording")
                    quiet_flag = False
                    last_ok_time = temp_time
                    
        # print('current frame {} volume {}'.format(temp_time+1, temp_volume))
        temp_time += 1
        if temp_time > 150:  # Timeout exit directly
            END_TIME = temp_time
            print('Timeout，end recording')
            break
    
    # stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # output wav audio file
    output_path = 'temp/speech_record.wav'
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames[START_TIME-2:END_TIME]))
    wf.close()
    print('save audio file', output_path)

import appbuilder

# configure key
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
asr = appbuilder.ASR() # speech recognition module
def speech_recognition(audio_path='temp/speech_record.wav'):
    '''
    AppBuilder-SDK speech recognition module
    '''
    print('Start speech recognition')
    # Load wav audio file
    with wave.open(audio_path, 'rb') as wav_file:
        
        # get basic information audio file
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        
        # get audio data info
        frames = wav_file.readframes(num_frames)
        
    # send request to API
    content_data = {"audio_format": "wav", "raw_audio": frames, "rate": 16000}
    message = appbuilder.Message(content_data)
    speech_result = asr.run(message).content['result'][0]
    print('Speech recognition result：', speech_result)
    return speech_result