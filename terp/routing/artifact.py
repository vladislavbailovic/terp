import os

class Item:
    extensions_map = {
        'html': '.html',
        'amp': '.amp',
        'sitemap-xml': '.xml',
    }
    def __init__(self, format, data):
        self.data = data
        self.format = format

    def get_destination(self):
        relpath = self.data.get('relpath')
        if not relpath:
            return None
        return self.slugify(os.path.splitext(relpath)[0] + self.get_extension())

    def get_extension(self):
        return Item.extensions_map[self.format]

    def get_type(self):
        type = self.data.get('type')
        return type if type else 'item'

    def get_template(self):
        relpath = self.get_destination()
        used = set()

        dir_tpl = os.path.basename(os.path.dirname(relpath))
        if dir_tpl:
            dir_tpl += '-' + self.get_type()

        parent_type_tpl = None
        if self.data.get('parent_type'):
            parent_type_tpl = self.data['parent_type'] + '-' + self.get_type()
            if dir_tpl:
                dir_tpl = self.data['parent_type'] + '-' + dir_tpl

        tpl = [self.slugify(x) for x in [
            os.path.splitext(os.path.basename(relpath))[0],
            dir_tpl,
            parent_type_tpl,
            self.get_type(),
        ] if x]
        return [x + self.get_extension()
                for x in tpl if x not in used and (used.add(x) or True)]

    def slugify(self, what):
        return what.replace(' ', '-').lower()


class ItemCollection(Item):
    def __init__(self, format, data):
        super().__init__(format, data)
        self.items = []

    def add_item(self, data):
        self.items.append(
            Item(self.format, data)
        )

    def has_index(self):
        return True

    def get_index(self):
        if not self.has_index():
            return None
        data = self.data.copy()
        data['relpath'] = 'index' + self.get_extension()
        data['items'] = self.items
        return Item(self.format, data)

    def get_destination(self):
        return self.slugify(self.get_type())

    def get_item_by(self, key, val):
        for item in self.items:
            if val == item.data.get(key):
                return item

        return None

    def get_type(self):
        type = self.data.get('type')
        return type if type else 'collection'
