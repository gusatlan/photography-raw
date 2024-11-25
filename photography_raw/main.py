from os_utils.osutils import get_source_dir, get_source_file_extensions, get_target_dir, read_source, copy_source


if __name__ == '__main__':
    source_files = read_source(path=get_source_dir(), extensions=get_source_file_extensions())
    copy_source(source_files=source_files, target_dir=get_target_dir())
