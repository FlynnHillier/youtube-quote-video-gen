from moviepy.video import VideoClip
import moviepy.video.fx.all as vfx
import moviepy.editor as mpe
from pathlib import Path
from PIL import Image

from animations import slide_in_horizontal

def subscribe_image_animation(
    vertical_pos:int,
    destination_pos_x_as_percentage:float,
    parent_width:int,
    duration_start=2,
    animation_duration=3,
    presence_duration=5,
    subscribe_image_filepath=Path("assets","reusable","subscribe.png")
) -> VideoClip.VideoClip:
    
    img = Image.open(subscribe_image_filepath)
    clip = slide_in_horizontal(
        img,
        animation_duration=animation_duration,
        slide_in_from="right",
        parent_clip_width=parent_width,
        height_pos=vertical_pos,
        destination=destination_pos_x_as_percentage
    )

    clip = clip.set_duration(presence_duration)
    clip = clip.set_start(duration_start)
    return clip
