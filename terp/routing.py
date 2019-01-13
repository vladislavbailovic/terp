import os


def route(cache):
    """Goes through cached items and figures out where what goes, and what template to use"""
    routed = []
    taxonomies = {}
    for item in cache:
        routed.append(
            Item('html', item)
        )
        if item.get('created'):
            created = item['created'][0]
            if not taxonomies.get('archives'):
                taxonomies['archives'] = ItemCollection('html', {'type': 'archives' })
            if not taxonomies['archives'].get_item_by('type', created):
                taxonomies['archives'].items.append(ItemCollection(
                    'html', {'type': created}
                ))
            taxonomies['archives'].get_item_by('type', created).add_item(item)

    for tax, archive in taxonomies.items():
        routed.append(archive)

    return routed


class Item:
    extensions_map = {
        'html': '.html'
    }
    def __init__(self, format, data):
        self.data = data
        self.format = format

    def get_destination(self):
        relpath = self.data.get('relpath')
        if not relpath:
            return None
        return os.path.splitext(relpath)[0] + self.get_extension()

    def get_extension(self):
        return Item.extensions_map[self.format]


class ItemCollection(Item):
    def __init__(self, format, data):
        super().__init__(format, data)
        self.items = []

    def add_item(self, data):
        self.items.append(
            Item(self.format, data)
        )

    def get_destination(self):
        return self.data.get('type')

    def get_item_by(self, key, val):
        for item in self.items:
            if val == item.data.get(key):
                return item

        return None
