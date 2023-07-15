from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

#returns lines as sepearate text string, width of longest line, and height of all lines combined (height is stil subject to fix, edit: seems to work ok) 
def wraptext(text:str,maxWidth:int,fontSize:int) -> tuple[list[str],int,int]:
    font = ImageFont.truetype("arial.ttf",size=fontSize)

    words = text.split(" ")
    line = ""
    lines = []

    for word  in words:
        temp = f"{line} {word}"

        if font.getlength(temp) > maxWidth:
            lines.append(line)
            line = word
        else:
            line = temp
    else:
        if line != "":
            lines.append(line)
    
    greatest_line_width = 0
    total_height = 0

    ascent,descent = font.getmetrics()
    for idx,line in enumerate(lines):

        # font.getsize() is currently broken - use below code when fixed.
        # (width,height),(offset_x,offset_y) = font.getsize(line)
        # total_height += height

        line_width = font.getlength(line)
        if line_width > greatest_line_width:
            greatest_line_width = line_width

    height_of_single_line = font.getbbox("".join(lines))[3]

    total_height = (height_of_single_line * len(lines)) + descent

    return lines , int(greatest_line_width) , total_height





def generate_caption_image(
        text:str,
        maxWidth:int,
        fontsize:int,
        output_path:str,
        fill_background:str | tuple[int,int,int] | None = None,
        text_fill:str | tuple[int,int,int] = (0,0,0),
        text_stroke_fill: str | tuple[int,int,int] = (0,0,0), 
        text_stroke_width: int = 0,
    ) -> str:

    font = ImageFont.truetype("arial.ttf", fontsize)

    #padding between border of background and text
    pad_vertical = 20
    pad_horizontal = 20

    text_area_width = maxWidth - (pad_horizontal * 2)


    lines, text_width, text_height = wraptext(text,text_area_width,fontsize)

    # when font.getsize() is fixed, use offset_x and offset_y in conjunction with padding
    img = Image.new(mode="RGBA",size = (text_width + (pad_horizontal * 2),text_height + ( pad_vertical * 2)),color=fill_background)

    draw = ImageDraw.Draw(img)


    # center align text on image
    total_height = pad_vertical
    
    for indx,line in enumerate(lines):
        line_w = font.getlength(line)
        line_h = font.getbbox(line)[3]

        start_line_pos_x = ((text_width - line_w) / 2) + pad_horizontal
        start_line_pos_y = total_height

        total_height += line_h
        draw.text((start_line_pos_x,start_line_pos_y),line,fill=text_fill,font=font,stroke_fill=text_stroke_fill,stroke_width=text_stroke_width)



    # draw.text((0,0),"\n ".join(lines),fill=text_fill,font=font,stroke_fill=text_stroke_fill,stroke_width=text_stroke_width)

    img.save(output_path,format="png")

    return output_path
    
if __name__ == "__main__":
    generate_caption_image("the cat jumped over hello",300,50,"test.png")