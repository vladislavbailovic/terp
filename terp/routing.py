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
            taxonomies = add_taxonomy_item(taxonomies, 'archives', created, item)
        if item.get('belongs-to'):
            episode = item['belongs-to'][0]
            taxonomies = add_taxonomy_item(taxonomies, 'series', episode, item)

    for tax, archive in taxonomies.items():
        routed.append(archive)

    return routed


def add_taxonomy_item(taxonomies, taxonomy, term, item):
    if not taxonomies.get(taxonomy):
        taxonomies[taxonomy] = ItemCollection('html', {'type': taxonomy})
    if not taxonomies[taxonomy].get_item_by('type', term):
        taxonomies[taxonomy].items.append(ItemCollection(
            'html', {'type': term, 'parent_type': taxonomy}
        ))
    item['parent_type'] = taxonomy
    item['relpath'] = os.path.join(
        taxonomy,
        taxonomies[taxonomy].get_item_by('type', term).get_destination(),
        os.path.basename(item['relpath'])
    )
    taxonomies[taxonomy].get_item_by('type', term).add_item(item)

    return taxonomies


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
        return self.slugify(os.path.splitext(relpath)[0] + self.get_extension())

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
