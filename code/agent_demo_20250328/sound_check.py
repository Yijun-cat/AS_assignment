# sound_check.py
# Quickly check all voice-related functions: microphone, recording, speaker playing sound, speech recognition, speech synthesis

from utils_asr import *             # recording & speech recognition
from utils_tts import *             # speech synthesis
print('Start recording for 5 seconds')
record(DURATION=5)   # recording
print('Play Recording')
play_wav('temp/speech_record.wav')
speech_result = speech_recognition()
print('Start speech synthesis')
tts(speech_result)
print('Playing speech synthesis audio')
play_wav('temp/tts.wav')

