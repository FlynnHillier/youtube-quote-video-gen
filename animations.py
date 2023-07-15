from moviepy.video import VideoClip
import moviepy.video.fx.all as vfx

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