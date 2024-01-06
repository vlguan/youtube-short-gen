from speech_to_text import main as stt
from text_to_speech import main as tts
import random
from moviepy.editor import *
from enConstants import voices
randVoice = voices[random.randint(0,len(voices)-1)]
file_path = 'stories.txt'
with open(file_path,'r') as file:
    textArray = [[line.strip() for line in file.readlines()]]
for i, textBody in enumerate(textArray[0]):
    print(randVoice, type(randVoice))
    tts(textBody, randVoice)
    video = stt(1.2)
    video.write_videofile('Videos/final/prod%d.mp4'%i)
print("Success, Videos should be prod0-%d"%i)

