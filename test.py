import os
import shutil
import markdown

def get_files(root):
    """Gets list of files"""
    return (
        os.path.abspath(os.path.join(directory, filename))
        for directory, subdir, files in os.walk(root)
        for filename in files if os.path.splitext(filename)[1] == ".md"
    )

def process_raw_input(root):
    md = markdown.Markdown(extensions=['meta'])
    prepare_cache_directory(os.getcwd())
    for f in get_files(root):
        data = process_raw_input_entry(f, md)
        print(data)
        md.reset()


def process_raw_input_entry(path, md):
    cwd = os.getcwd()
    relpath = os.path.relpath(path, start=cwd)
    destpath = os.path.join(get_cache_directory(cwd), relpath)
    os.makedirs(os.path.dirname(destpath), exist_ok=True)
    md.convertFile(
        input=path,
        output=destpath
    )
    return {
        "path": path,
        "relpath": relpath,
        "cached": destpath,
        "data": md.Meta,
    }


def prepare_cache_directory(working_directory):
    clear_cache_directory(working_directory)
    working = get_cache_directory(working_directory)
    os.makedirs(working)


def clear_cache_directory(working_directory):
    working = get_cache_directory(working_directory)
    if os.path.exists(working):
        print("directory exists, clearing")
        shutil.rmtree(working)


def get_cache_directory(working_directory):
    return os.path.join(working_directory, '.terp-working', 'cache')


process_raw_input('data')

