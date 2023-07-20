import moviepy.editor as mpe
import moviepy.video.fx.all as vfx
from image import generate_caption_image
from pathlib import Path
from animations import fade_in
from reusable_clips import subscribe_image_animation
import os
import random

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


def get_random_file_from_dir(directory:str,extension:str = None) -> str:
    # if provided directory is invalid
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"the directory '{directory}' does not exist.")
    
    # add leading period to extension
    if extension != None and extension[0] != ".":
        extension = "." + extension
    
    contents = os.listdir(directory)
    contents = list(map(lambda file: Path(directory).joinpath(file),contents))

    targets = list(filter(lambda path: os.path.isfile(path) and (True if extension == None else Path(path).suffix == extension),contents))

    # if no file are found that match the criteria
    if len(targets) == 0:
        raise FileNotFoundError(f"no files were found in the directory '{directory}'{'' if extension == None else f' , with file extension: .{extension}'}")
    
    return str(random.choice(targets))


def generateVideo(
        watermark:str,
        text1:str,
        text2:str,
        label:str,
        out_file_path:str,
        media_folder:str | None,
        background_clip_path:str | None = None,
        music_file_path:str | None = None,
        generated_assets_folder_path:str | None = None
    ):

    # query correct media argument paramters.
    if not media_folder and not (background_clip_path and music_file_path):
        raise ValueError(f"must specify media folder path, or both background clip path and music file path")

    # select media file paths if specific file paths not specified.
    if background_clip_path == None:
        background_clip_path = get_random_file_from_dir(str(Path(media_folder).joinpath("videos")))

    if music_file_path == None:
        music_file_path = get_random_file_from_dir(str(Path(media_folder).joinpath("music")))
    

    clip_duration = 15

    clip = mpe.VideoFileClip(background_clip_path)
    clip = clip.subclip(0,15)

    clip,clip_width,clip_height = fit_video_to_9_16(clip)
    

    label_image_path = generate_caption_image(label,maxWidth=clip_width,fontsize=140,output_path=str(Path(generated_assets_folder_path,"label.png")),fill_background="black",text_fill="white")

    text1_image_path = generate_caption_image(text1,maxWidth=clip_width * 0.8,fontsize=100,output_path=str(Path(generated_assets_folder_path,"txt1.png")),text_fill=(255,255,255),text_stroke_fill=(0,0,0),text_stroke_width=2)

    text2_image_path = generate_caption_image(text2,maxWidth=clip_width * 0.8,fontsize=100,output_path=str(Path(generated_assets_folder_path,"txt2.png")),text_fill=(255,255,255),text_stroke_fill=(0,0,0),text_stroke_width=2)

    label_clip = mpe.ImageClip(label_image_path,duration=15)

    label_clip = label_clip.set_position(("center",0.2),relative=True)

    text1_clip = mpe.ImageClip(text1_image_path,transparent=True)
    text1_clip = fade_in(text1_clip,animation_duration=1.5)
    text1_clip = text1_clip.set_start(0)
    text1_clip = text1_clip.set_duration(clip_duration * 2/3)
    text1_clip = text1_clip.set_position(("center",0.4),relative=True)

    text2_clip = mpe.ImageClip(text2_image_path,transparent=True)
    text2_clip = fade_in(text2_clip,animation_duration=1.5)
    text2_clip = text2_clip.set_start(12)
    text2_clip = text2_clip.set_duration(3)
    text2_clip = text2_clip.set_position(("center",0.4),relative=True)


    
    
    watermark_start_show_time = 8
    
    subscribe_clip = subscribe_image_animation(clip_height * 0.8 ,0.5,clip_width,duration_start=2,animation_duration=3,presence_duration=6)

    watermark_image_path = generate_caption_image(watermark,clip_width,60,fill_background=None,text_fill="black",text_stroke_fill="white",text_stroke_width=1,output_path=str(Path(generated_assets_folder_path,"watermark.png")))

    watermark_clip = mpe.ImageClip(watermark_image_path).set_start(watermark_start_show_time).set_duration(clip_duration - watermark_start_show_time)

    watermark_clip = watermark_clip.set_position(("center",0.8),relative=True)

    watermark_clip = watermark_clip.set_opacity(0.4)


    out = mpe.CompositeVideoClip([clip,label_clip,text1_clip,text2_clip,subscribe_clip,watermark_clip])
    out = out.set_duration(clip_duration)

    if(music_file_path):
        audio = mpe.AudioFileClip(music_file_path).set_duration(clip_duration)
        out = out.set_audio(audio)

    out.write_videofile(out_file_path)


def fit_video_to_9_16(clip:mpe.VideoFileClip) -> tuple[mpe.VideoFileClip,int,int]:
    (w, h) = clip.size

    #calculate correct width dimensions
    width_mid_point = w / 2
    crop_width = h * 9/16
    x1 = int(width_mid_point - (crop_width / 2))
    x2 = int(width_mid_point + (crop_width / 2))

    #if odd pixel width, make even. Added to prevent video chorruption. Not sure why it works, but it seems to.
    if (x2 - x1) % 2 != 0:
        x2 -= 1

    y1, y2 = 0, h

    cropped_clip = vfx.crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    return cropped_clip,crop_width,h


if __name__ == "__main__":
    generateVideo("kalanz","if a girl loves a guy...","he will be on her mind every minute of the day.","GIRL FACTS","sample.mp4")