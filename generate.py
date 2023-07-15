import moviepy.editor as mpe
import moviepy.video.fx.all as vfx
from image import generate_caption_image
from pathlib import Path

# youtube shorts should be 1080 x 1920
# under 60 seconds
# shorts


def wraptext(text:str,spreadWidth:int,fontsize:int) -> str:
    # edit so that fontwidth is calculated
    
    words = text.split(" ")
    chars_per_line = spreadWidth / 40 
    line_char_count = 0
    out = ""

    for word in words:
        chars = len(word)
        if line_char_count + chars > chars_per_line:
            out = f"{out}\n{word}"
            line_char_count = chars
        else:
            out = f"{out} {word}"
            line_char_count += chars
    
    return out


def generateVideo(watermark:str,text1:str,text2:str,label:str,background_clip_path:str,out_file_path:str,music_file_path:str | None = None,generated_assets_folder_path:str | None = None):
    clip_duration = 15
    
    clip = mpe.VideoFileClip(background_clip_path)
    clip = clip.subclip(0,15)

    clip,clip_width,clip_height = fit_video_to_9_16(clip)
    

    label_image_path = generate_caption_image(label,maxWidth=clip_width,fontsize=100,output_path=str(Path(generated_assets_folder_path,"label.png")),fill_background="black",text_fill="white")

    text1_image_path = generate_caption_image(text1,maxWidth=clip_width * 0.6,fontsize=70,output_path=str(Path(generated_assets_folder_path,"txt1.png")),text_fill=(255,255,255),text_stroke_fill=(0,0,0),text_stroke_width=2)

    text2_image_path = generate_caption_image(text2,maxWidth=clip_width * 0.6,fontsize=70,output_path=str(Path(generated_assets_folder_path,"txt2.png")),text_fill=(255,255,255),text_stroke_fill=(0,0,0),text_stroke_width=2)

    label_clip = mpe.ImageClip(label_image_path,duration=15)

    label_clip = label_clip.set_position(("center",0.2),relative=True)

    text1_clip = mpe.ImageClip(text1_image_path,transparent=True)
    text1_clip = text1_clip.set_start(0)
    text1_clip = text1_clip.set_duration(clip_duration * 2/3)
    text1_clip = text1_clip.set_position(("center",0.4),relative=True)

    text2_clip = mpe.ImageClip(text2_image_path,transparent=True)
    text2_clip = text2_clip.set_start(12)
    text2_clip = text2_clip.set_duration(3)
    text2_clip = text2_clip.set_position(("center",0.4),relative=True)


    out = mpe.CompositeVideoClip([clip,label_clip,text1_clip,text2_clip])
    out = out.set_duration(clip_duration)

    if(music_file_path):
        audio = mpe.AudioFileClip(music_file_path).set_duration(clip_duration)
        out = out.set_audio(audio)

    out.write_videofile(out_file_path)


def fit_video_to_9_16(clip:mpe.VideoFileClip) -> tuple[mpe.VideoFileClip,int,int]:
    (w, h) = clip.size
    crop_width = h * 9/16
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h

    cropped_clip = vfx.crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    return cropped_clip,crop_width,h


if __name__ == "__main__":
    generateVideo("kalanz","if a girl loves a guy...","he will be on her mind every minute of the day.","GIRL FACTS","sample.mp4")