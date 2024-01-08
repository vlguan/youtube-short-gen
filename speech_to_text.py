from utils.tiktokvoicemain.main import tts
import whisper_timestamped as whisper
import sys
import random
from moviepy.editor import *
def adhdCrop_clip(video1, video2, duration):
    video1 = crop_clip(video1, duration, (9,8))
    video2 = crop_clip(video2, duration, (9,8))
    final_clip = clips_array([[video1],[video2]])
    return final_clip
def crop_clip(video,duration, target_aspect_ratio=(9, 16)):
     
    # Get video dimensions
    original_width, original_height = video.size

    # Calculate target width based on the aspect ratio
    target_width = int(original_height * target_aspect_ratio[0] / target_aspect_ratio[1])

    # Calculate horizontal and vertical black bars to add
    horizontal_padding = (original_width - target_width) // 2
    vertical_padding = 0  # No vertical padding for centering in this example

    # Apply cropping
    cropped_clip = video.crop(x1=horizontal_padding, x2=original_width - horizontal_padding,
                             y1=vertical_padding, y2=original_height - vertical_padding)

    # Resize to target dimensions
    # final_clip = cropped_clip.resize(width=target_width, height=original_height)
    upperLimit = int(cropped_clip.duration - duration)
    randomSection = random.randint(0, upperLimit)
    cropped_clip = cropped_clip.subclip(randomSection, randomSection + duration)
    # Write the result to a new file
    return cropped_clip

def create_subtitles(results, videosize):
    subs = []
    textPos = ('center',(videosize*3)/4)
    # seperates the words from whisper
    for seg in results["segments"]:
        for i,word in enumerate(seg["words"]):
            text = word["text"].upper()
            start = word["start"]
            # print(start)
            end = word["end"]
            dur = end - start
           #text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
            txt_clip = TextClip(txt=text, fontsize=90, color='white',font='Take-Looks', method='caption', stroke_width=1,stroke_color='black').set_start(start).set_duration(dur)
            # txt_clip.write_videofile('Videos/sub%d.mp4'%i)
            subs.append(txt_clip.set_position(textPos))
    return subs
def main(speedup, adhdBool):
    model = whisper.load_model("medium", device='cpu')
    ttsAudio = AudioFileClip('audioOutput/fulltts.mp3').fx(vfx.speedx,speedup)
    # if ttsAudio.duration > 60:
    #     print(ttsAudio.duration)
    #     raise ValueError('tts too long skippped')
    audio = whisper.load_audio('audioOutput/fulltts.mp3')
    result = whisper.transcribe(model, audio, language='en')
    randInt = random.randint(1,20)
    if adhdBool:
        vid1 = VideoFileClip('Videos/satisfying.mp4')
        vid2 = VideoFileClip('Videos/rand%d.mp4'%randInt)
        clip = adhdCrop_clip(vid1, vid2,  (ttsAudio.duration)*speedup)
    else:
        print("rand%d.mp4 is being clipped"%randInt)
        video = VideoFileClip('Videos/rand%d.mp4'%randInt)
        
        clip = crop_clip(video, (ttsAudio.duration)*speedup)
    w,h = clip.size
    subs = create_subtitles(result,h)
    final = CompositeVideoClip([clip] + subs).fx(vfx.speedx,speedup)
    final = final.set_audio(ttsAudio)
    return final
    # final.write_videofile('Videos/productTest.mp4')
if __name__ == "__main__":
    main()