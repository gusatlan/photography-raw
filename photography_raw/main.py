from os_utils.osutils import get_source_dir, get_source_file_extensions, get_target_dir, read_source, copy_source, build_current_target_dir, get_target_extension, convert_images


if __name__ == '__main__':
    source_files = read_source(path=get_source_dir(), extensions=get_source_file_extensions())
    copy_source(source_files=source_files, target_dir=get_target_dir())
    convert_images(
        source_dir=build_current_target_dir(target_dir=get_target_dir(), raw=True),
        target_dir=build_current_target_dir(target_dir=get_target_dir(), raw=False),
        file_type=get_target_extension()
    )

    convert_images(
        source_dir=build_current_target_dir(target_dir=get_target_dir(), raw=True),
        target_dir=build_current_target_dir(target_dir=get_target_dir(), raw=False),
        file_type='JPEG'
    )

