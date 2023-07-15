from moviepy.video import VideoClip
import moviepy.video.fx.all as vfx
from moviepy.editor import ImageClip
from PIL import Image
import numpy

def fade_in(clip:VideoClip.VideoClip,animation_duration:float,animation_intital_size:float = 1.3,opacity_fade_in:bool = True,opacity_fade_in_duration:float = 0.5) -> VideoClip.VideoClip:
    if animation_intital_size < 1:
        raise ValueError("animation initial size must be greater than 1")


    animation_reduction_speed = (animation_intital_size - 1) / animation_duration
    fade_in_resize_animation = lambda t : 1 if t >= animation_duration else (animation_intital_size - (t * animation_reduction_speed))
    
    #apply resize animation
    clip = vfx.resize(clip,fade_in_resize_animation)
    
    #apply opacity fade in effect
    if(opacity_fade_in):
        #prevent error if clip duration has not yet been set
        if clip.duration == None:
            clip = clip.set_duration(opacity_fade_in_duration)
        
        clip = clip.crossfadein(opacity_fade_in_duration)

    return clip


# destination denotes how far along the parent clip the image should slide across
# height_pos denotes where in the parent clip the image clip should sit on a vertical axis, given as an absolute
def slide_in_horizontal(
        image:Image,
        animation_duration:float, 
        slide_in_from:str,
        parent_clip_width:int,
        height_pos:int,
        destination:float = 0.5
    ) -> VideoClip.VideoClip:
    img_width, img_height = image.size
    print(img_width,img_height)

    initial_position_x = 0

    #invert destination if coming from right
    if(slide_in_from == "right"):
        destination = 1 - destination

    
    destination_pos_x = int((parent_clip_width * destination) - (img_width / 2))

    distance_to_slide_across = (parent_clip_width * destination) + (img_width / 2)

    animation_slide_in_speed = distance_to_slide_across / animation_duration

    if slide_in_from == "right":
        initial_position_x = int(parent_clip_width)
        movement_multipler = -1
        
    if slide_in_from == "left":
        initial_position_x = -img_width
        movement_multipler = 1

    # movement multiplier is used to determine direction position moves across
    slide_in_animation_position = lambda t: (destination_pos_x,height_pos) if t > animation_duration else (initial_position_x + ( movement_multipler * (t * animation_slide_in_speed)),height_pos)

    clip = ImageClip(numpy.array(image))
    clip = clip.set_position(slide_in_animation_position)
    return clip
    

    


