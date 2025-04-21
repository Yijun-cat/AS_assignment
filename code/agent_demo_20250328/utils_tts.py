# utils_tts.py
# speech synthesis

import os
import appbuilder
from API_KEY import *
import pyaudio
import wave

print('Import speech sythesis module')

tts_ab = appbuilder.TTS()

def tts(TEXT="I am your steel paw of justice!", tts_wav_path = 'temp/tts.wav'):
    '''
    Speech synthesis using text-to-speech (TTS), generate a WAV audio file"
    '''
    inp = appbuilder.Message(content={"text": TEXT})
    out = tts_ab.run(inp, model="paddlespeech-tts", audio_type="wav")
    # out = tts_ab.run(inp, audio_type="wav")
    with open(tts_wav_path, "wb") as f:
        f.write(out.content["audio_binary"])
    # print("TTS speech systhesis，export wav audio file to：{}".format(tts_wav_path))

def play_wav(wav_file='asset/welcome.wav'):
    '''
    play wav audio file
    '''
    prompt = 'aplay -t wav {} -q'.format(wav_file)
    os.system(prompt)

# def play_wav(wav_file='temp/tts.wav'):
#     '''
#     播放wav文件
#     '''
#     wf = wave.open(wav_file, 'rb')
 
#     # 实例化PyAudio
#     p = pyaudio.PyAudio()
 
#     # 打开流
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)

#     chunk_size = 1024
#     # 读取数据
#     data = wf.readframes(chunk_size)
 
#     # 播放音频
#     while data != b'':
#         stream.write(data)
#         data = wf.readframes(chunk_size)
 
#     # 停止流，关闭流和PyAudio
#     stream.stop_stream()
#     stream.close()
#     p.terminate()