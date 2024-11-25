import logging
import rawpy
from PIL import Image
from utils.utils import get_logger



def convert_image(source_file:str, target_file:str, file_type: str, raw:bool=True) -> None:
    img = None
    
    if raw:
        with rawpy.imread(source_file) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
    else:
        img = Image.open(source_file)


    img.save(target_file, format=file_type.upper().strip())
    get_logger().info(f'Converted {source_file} to {target_file}')
