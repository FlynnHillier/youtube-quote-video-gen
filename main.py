import moviepy.editor as mpe
# import moviepy.video.fx.all as vfx
import moviepy.video.fx.all as vfx

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


def generateVideo(watermark:str,text1:str,text2:str,label:str,background_clip_path):
    clip = mpe.VideoFileClip(background_clip_path)
    clip = clip.subclip(0,15)

    clip,width,height = fit_video_to_9_16(clip)

    txt1 = mpe.TextClip(
            wraptext(text1,width * 0.8,75),
            fontsize=75,
            color="yellow",
            stroke_color="black",
            stroke_width=2,
            font="Arial",
            align="south"
        )
    txt1 = txt1.set_position("center")
    txt1 = txt1.set_duration(10)

    out = mpe.CompositeVideoClip([clip,txt1])
    out = out.set_duration(15)

    out.write_videofile("out.mp4")


def fit_video_to_9_16(clip:mpe.VideoFileClip) -> tuple[mpe.VideoFileClip,int,int]:
    (w, h) = clip.size
    crop_width = h * 9/16
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h

    cropped_clip = vfx.crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    return cropped_clip,crop_width,h


if __name__ == "__main__":
    generateVideo("kalanz","text1 sample text long hello world hello the cat jump car","text2 sample text","crazy facts!","sample.mp4")