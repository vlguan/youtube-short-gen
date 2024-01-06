import os
import sys
from moviepy.editor import *
from utils.tiktokvoicemain.main import tts
def args(text):
    if (text[-1] =="."):
        text = text[:-1]
    sentences = text.split(".")
    return sentences
def main(sentences, voice):
    # splitup passage into shorter sentences
    sentences = args(sentences)
    audio_files=[]
    # def tts(session_id, text_speaker, req_text, filename, play):
    for i,sentence in enumerate(sentences):
        file_name = 'audioOutput/output' + str(i) + '.mp3'
        tts('73782eef66d5ab64bf83342be9623375', voice, sentence, file_name)
        audio_files.append(AudioFileClip(file_name))
    for i in range(len(audio_files)):
        file_namex = 'audioOutput/output' + str(i) + '.mp3'
        os.remove(file_namex)
    audio_clip = concatenate_audioclips([audio for audio in audio_files])
    audio_clip.write_audiofile('audioOutput/fulltts.mp3')
if __name__ == "__main__":
    main()