import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, ChoiceLoader, select_autoescape, TemplatesNotFound


Env = Environment(
    loader=ChoiceLoader([
        PackageLoader('terp', 'tpl'),
        FileSystemLoader(os.getcwd())
    ]),
    autoescape=select_autoescape(
        default=True
    )
)


def out(routed, out_dir):
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
        generate_item_output(index, out)

    for item in tax.items:
        if hasattr(item, 'items'):
            generate_taxonomy_output(item, out)

    return True


def generate_item_output(item, out):
    path = os.path.join(out, item.get_destination())
    tpl_cascade = item.get_template()
    try:
        template = Env.get_or_select_template(tpl_cascade)
        print("Generating item output: {} using {}".format(path, template))
        if item.data.get('cached'):
            with open(item.data.get('cached'), 'r') as f:
                content = f.read()
        else:
            content = ''
        print(template.render(item=item, content=content))
    except TemplatesNotFound:
        pass
    return True
