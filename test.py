import os
import shutil
import markdown

def process_raw_input(root):
    """Goes through item in source dir and generates initial data cache"""
    md = markdown.Markdown(extensions=['meta'])
    prepare_cache_directory(os.getcwd())
    cache = []
    for f in get_files(root):
        data = process_raw_input_entry(f, md)
        cache.append(data)
        md.reset()

    return cache


def reverse_route(cache):
    """Goes through cached items and figures out where what goes, and what template to use"""
    routed = []
    for item in cache:
        # Augment cache item with routing data
        # Add archives, tags, etc
        item['destination'] = os.path.splitext(item.get('relpath'))[0] + '.html'
        routed.append(item)

    return routed

def generate_output(routed, out_dir):
    """Goes through the routed info and writes out the result using templates"""
    cwd = os.getcwd()
    results = []
    for item in routed:
        out = os.path.join(
            cwd,
            out_dir,
            item['destination']
        )
        print("Generating {} from {}".format(out, item['cached']))
        results.append(True)

    return results


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


def get_files(root):
    """Gets list of files"""
    return (
        os.path.abspath(os.path.join(directory, filename))
        for directory, subdir, files in os.walk(root)
        for filename in files if os.path.splitext(filename)[1] == ".md"
    )


cache = process_raw_input('data')
routed = reverse_route(cache)
report = generate_output(routed, 'out')

