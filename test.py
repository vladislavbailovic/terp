import os

from terp.routing import router
from terp.sources import parser

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
    index = tax.get_index()
    if index:
        print("Generating index: {}".format(
            index.get_type()
        ))
        generate_item_output(index, out)

    for item in tax.items:
        if hasattr(item, 'items'):
            generate_taxonomy_output(item, out)

    return True

def generate_item_output(item, out):
    path = os.path.join(out, item.get_destination())
    print("Generating item output: {} using {}".format(path, item.get_template()))
    return True


cache = parser.parse('data')
routed = router.route(cache)
report = generate_output(routed, 'out')

