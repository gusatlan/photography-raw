import os
import logging
import shutil
from datetime import datetime

SOURCE_DIR_ENV = 'source_dir'
TARGET_DIR_ENV = 'target_dir'
SOURCE_DIR = '/media/gustavooliveira/3133-3934/'
TARGET_DIR = '/media/fileserver2/fotografia/'

FILE_SOURCE_EXTENSIONS_ENV='file_source_extensions'
FILE_SOURCE_EXTENSIONS='.cr2, .cr3, .nef, .arw, .dng'

FILE_TARGET_EXTENSION_ENV='file_target_extension'
FILE_TARGET_EXTENSION='tiff'

logger = logging.getLogger(__name__)


def get_parameter(env_variable:str, default_value:str) -> str:
    try:
        return os.environ[env_variable.upper()]
    except:
        logger.warning(f'{env_variable} empty, using default {default_value}')
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


def read_source(path:str, extensions:list) -> list:
    files = []

    logger.info(f'Scanning source directory {path}')

    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        logger.info(f'Verifying {file}')

        if os.path.isdir(full_path):
            [files.append(f) for f in read_source(path=full_path, extensions=extensions)]
        elif file.lower().endswith(tuple(extensions)):
            files.append(os.path.join(path, file))
            logger.info(f'Matched {file}')
    
    return files


def build_current_target_dir(target_dir:str, raw:bool=True) -> str:
    date = datetime.now()
    current_target_dir = os.path.join(target_dir, str(date.year), str(date.month), str(date.day))

    if raw:
        current_target_dir = os.path.join(current_target_dir, 'raw')
    else:
        current_target_dir = os.path.join(current_target_dir, get_target_extension().lower().strip())

    return current_target_dir


def copy_source(source_files:list, target_dir:str) -> None:
    current_target_dir = build_current_target_dir(target_dir=target_dir, raw=True)
    os.makedirs(name=current_target_dir, exist_ok=True)

    logger.info(f'Saving source files in {current_target_dir}')

    for source_file in source_files:
        target_file = os.path.join(current_target_dir, os.path.basename(source_file))

        logger.info(f'Copying {source_file} to {target_file}')
        shutil.copy(src=source_file, dst=target_file)
