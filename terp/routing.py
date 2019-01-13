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
                    'html', {'type': created, 'parent_type': 'archives'}
                ))
            item['parent_type'] = 'archives'
            item['relpath'] = os.path.join(
                'archives',
                taxonomies['archives'].get_item_by('type', created).get_destination(),
                os.path.basename(item['relpath'])
            )
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

    def get_type(self):
        type = self.data.get('type')
        return type if type else 'item'

    def get_template(self, path=None):
        relpath = path if path else self.get_destination()
        used = set()

        dir_tpl = os.path.basename(os.path.dirname(relpath))
        if dir_tpl:
            dir_tpl += '-' + self.get_type()

        parent_type_tpl = None
        if self.data.get('parent_type'):
            parent_type_tpl = self.data['parent_type'] + '-' + self.get_type()
            dir_tpl = self.data['parent_type'] + '-' + dir_tpl

        tpl = [
            os.path.splitext(os.path.basename(relpath))[0],
            dir_tpl,
            parent_type_tpl,
            self.get_type(),
        ]
        return [x + self.get_extension()
                for x in tpl if x and x not in used and (used.add(x) or True)]


class ItemCollection(Item):
    def __init__(self, format, data):
        super().__init__(format, data)
        self.items = []

    def add_item(self, data):
        self.items.append(
            Item(self.format, data)
        )

    def get_destination(self):
        return self.get_type()

    def get_item_by(self, key, val):
        for item in self.items:
            if val == item.data.get(key):
                return item

        return None

    def get_type(self):
        type = self.data.get('type')
        return type if type else 'collection'

    def get_template(self, path=None):
        tpl = super().get_template(path)
        if self.data.get('parent_type'):
            tpl.append(
                self.data.get('parent_type') + self.get_extension()
            )
        return tpl
