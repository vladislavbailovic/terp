import os
import shutil
import markdown

from terp import routing

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


def generate_output(routed, out_dir):
    """Goes through the routed info and writes out the result using templates"""
    cwd = os.getcwd()
    results = []
    for item in routed:
        result = None
        if hasattr(item, 'items'):
            result = generate_taxonomy_output(item, out_dir)
        else:
            result = generate_item_output(item, out_dir)
        results.append(result)

    return results

def generate_taxonomy_output(tax, out):
    out = os.path.join(out, tax.get_destination())
    index = os.path.join(out, 'index' + tax.get_extension())

    print("Generating index: {} at {} using {}".format(
        tax.get_type(), index, tax.get_template(index)
    ))
    # ...

    for item in tax.items:
        if hasattr(item, 'items'):
            generate_taxonomy_output(item, out)
        else:
            generate_item_output(item, out)

    return True

def generate_item_output(item, out):
    path = os.path.join(out, item.get_destination())
    print("Generating item output: {} using {}".format(path, item.get_template(path)))
    return True

def process_raw_input_entry(path, md):
    cwd = os.getcwd()
    relpath = os.path.relpath(path, start=cwd)
    destpath = os.path.join(get_cache_directory(cwd), relpath)
    os.makedirs(os.path.dirname(destpath), exist_ok=True)
    md.convertFile(
        input=path,
        output=destpath
    )
    data = {
        "path": path,
        "relpath": relpath,
        "cached": destpath,
    }
    for (key, val) in md.Meta.items():
        data[key] = val
    return data


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
routed = routing.route(cache)
report = generate_output(routed, 'out')

