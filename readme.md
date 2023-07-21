# setup
## dependencies
- ```pip install -r requirements.txt```

## pre-requisites
- install ffmpeg: https://ffmpeg.org/download.html
- install imageMagick (with legacy utils ticked): https://imagemagick.org/script/download.php
    - **windows users**: set enviroment variable *'IMAGEMAGICK_BINARY'* to point toward *magick.exe* (found within installation of imageMagick)
- manually edit moviepy lib file with changes specified within following commit: https://github.com/Zulko/moviepy/pull/2003/commits/1d95b234f1b71357df14f0e54ae85fec23559b2c


# use
- configure `config.json` to fit your needs. 
- create a file called `inputs.txt` within the top-level directory, each line should contain a single quote, with the two sections intended for the video seperated by the character defined by 'inputs_delimeter' in `config.json`.
- create folders: `videos` & `music` within the assets folder. Populate these folders with media that will be used to create the videos with.

## recommendations
I would reccomend the use of an LLM, such as [open-ai's chat-gpt](https://chat.openai.com/), in order to generated the content within the `inputs.txt` file. Doing so will save you alot of time and make the content generation truly effortless.

Here is an example of a prompt i used to generate the content used within the [example section](#example-videos) of this document:
- `write a list of short quotes regarding girls, in a csv format, in which the build up to the quote is held in one colum, while the ending to the quote is held in the other column. These quotes should be targetted such that a young youtube audience would like them. These quotes should be approximately 15-25 words long. Please remove any quotation marks and any commas from within the quotes`



# example videos
Here are a few example videos i created using this software.
- https://www.youtube.com/shorts/CvHybolXe34
- https://www.youtube.com/shorts/LAJQHkAxTcU
- https://www.youtube.com/shorts/zW0TvR2NZ0Q