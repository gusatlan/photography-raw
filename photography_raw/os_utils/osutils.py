import os
import logging
import shutil
from datetime import datetime
from image_utils.imageutils import convert_image
from utils.utils import get_logger

SOURCE_DIR_ENV = 'source_dir'
TARGET_DIR_ENV = 'target_dir'
SOURCE_DIR = '/media/gustavooliveira/3133-3934/'
TARGET_DIR = '/media/fileserver2/fotografia/'

FILE_SOURCE_EXTENSIONS_ENV='file_source_extensions'
FILE_SOURCE_EXTENSIONS='.cr2, .cr3, .nef, .arw, .dng'

FILE_TARGET_EXTENSION_ENV='file_target_extension'
FILE_TARGET_EXTENSION='tiff'

FILE_TARGET_EXTENSION_SECUNDARY_ENV='file_target_extension_secundary'
FILE_TARGET_SECUNDARY_EXTENSION='jpeg'
SECUNDARY_ALLOW_ENV='secundary_allow'
SECUNDARY_ALLOW='False'



def get_parameter(env_variable:str, default_value:str) -> str:
    try:
        return os.environ[env_variable.upper().strip()]
    except:
        get_logger().warning(f'{env_variable} empty, using default {default_value}')
        return default_value
    

def get_source_dir() -> str:
    return get_parameter(env_variable=SOURCE_DIR_ENV, default_value=SOURCE_DIR)


def get_target_dir() -> str:
    return get_parameter(env_variable=TARGET_DIR_ENV, default_value=TARGET_DIR)


def get_source_file_extensions() -> list:
    value = get_parameter(env_variable=FILE_SOURCE_EXTENSIONS_ENV, default_value=FILE_SOURCE_EXTENSIONS).split(',')
    value = list([x.strip().lower() for x in value])
    return value


def get_target_extension() -> str:
    return get_parameter(env_variable=FILE_TARGET_EXTENSION_ENV, default_value=FILE_TARGET_EXTENSION)


def get_target_secundary_extension() -> str:
    return get_parameter(env_variable=FILE_TARGET_EXTENSION_SECUNDARY_ENV, default_value=FILE_TARGET_SECUNDARY_EXTENSION)


def get_target_secundary_allow() -> bool:
    return bool(get_parameter(env_variable=SECUNDARY_ALLOW_ENV, default_value=SECUNDARY_ALLOW))


def read_source(path:str, extensions:list) -> list:
    files = []

    get_logger().info(f'Scanning source directory {path}')

    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        get_logger().info(f'Verifying {file}')

        if os.path.isdir(full_path):
            [files.append(f) for f in read_source(path=full_path, extensions=extensions)]
        elif file.lower().endswith(tuple(extensions)):
            files.append(os.path.join(path, file))
            get_logger().info(f'Matched {file}')
    
    return files


def build_current_target_dir(target_dir:str, target_type:str=get_target_extension()) -> str:
    date = datetime.now()
    tgt_type = target_type.lower().strip()
    current_target_dir = os.path.join(target_dir, str(date.year), str(date.month), str(date.day))

    if tgt_type == get_target_extension():
        current_target_dir = os.path.join(current_target_dir, tgt_type)
    else:
        current_target_dir = os.path.join(current_target_dir, tgt_type)

    return current_target_dir


def copy_source(source_files:list, target_dir:str) -> None:
    current_target_dir = build_current_target_dir(target_dir=target_dir, target_type='raw')
    os.makedirs(name=current_target_dir, exist_ok=True)

    get_logger().info(f'Saving source files in {current_target_dir}')

    for source_file in source_files:
        target_file = os.path.join(current_target_dir, os.path.basename(source_file))

        get_logger().info(f'Copying {source_file} to {target_file}')
        shutil.copy(src=source_file, dst=target_file)


def convert_images(source_dir:str, target_dir:str, file_type:str) -> None:
    os.makedirs(name=target_dir, exist_ok=True)

    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, f'{os.path.splitext(file)[0]}.{file_type.lower().strip()}')

        get_logger().info(f'Converting {source_file} to {target_file}')
        convert_image(
            source_file=source_file,
            target_file=target_file,
            file_type=file_type,
            raw=file_type == get_target_extension()
        )
