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