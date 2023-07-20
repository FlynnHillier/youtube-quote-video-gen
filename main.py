from generate import generateVideo
import json
from operator import itemgetter
from pathlib import Path

def load_config(config_path="config.json") -> dict[str,str]:
    with open(config_path) as f:
        config = json.load(f)
    required_entries = [
        "watermark",
        "inputs_delimeter",
        "label",
        "out_dir",
        "temp_assets_dir",
    ]

    missing_keys = []
    present_keys = config.keys()
    for key in required_entries:
        if key not in present_keys:
            missing_keys.append(key)
    
    if len(missing_keys) != 0:
        raise TypeError(f"missing entries within '{config_path}' :  [ {', '.join(missing_keys)} ]")

    return config


watermark,label,inputs_delimeter,out_dir,temp_assets_dir = itemgetter("watermark","label","inputs_delimeter","out_dir","temp_assets_dir")(load_config())

with open("inputs.txt") as f:
    lines = f.readlines()
    for indx,line in enumerate(lines):
        line = line.removesuffix("\n")
        split = line.split(inputs_delimeter)
        if len(split) != 2:
            print("skipping, not length 2.")
            continue
            
    
        text1,text2 = split

        text1 = text1.lstrip()
        text1 += "..."
        generateVideo(
            watermark=watermark,
            text1=text1,
            text2=text2,
            label=label,
            out_file_path=str(Path(out_dir).joinpath(f"clip_{watermark}_{indx}.mp4")),
            generated_assets_folder_path=temp_assets_dir,
            media_folder="assets",
        )