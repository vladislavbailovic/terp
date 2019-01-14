import os
from datetime import datetime

from .artifact import Item, ItemCollection
from . import types


def route(cache):
    """Goes through cached items and figures out where what goes, and what template to use"""
    routed = []
    taxonomies = {}
    for type in [types.HTML, types.AMP]:
        format = type[0]
        for item in cache:
            routed.append(
                Item(format, item)
            )
            if item.get('created'):
                when = datetime.strptime(
                    item['created'][0],
                    '%Y-%m-%d'
                )
                created = when.strftime('%Y-%m')
                taxonomies = add_taxonomy_item(taxonomies, 'archives', created, item, format)
            if item.get('belongs-to'):
                episode = item['belongs-to'][0]
                taxonomies = add_taxonomy_item(taxonomies, 'series', episode, item, format)

    for tax, archive in taxonomies.items():
        routed.append(archive)

    items = routed.copy()
    routed.append(Item(types.SITEMAP[0], {
        'relpath': 'sitemap',
        'items': items,
    }))

    return routed


def add_taxonomy_item(taxonomies, taxonomy, term, item, format):
    tax_idx = taxonomy + format
    if not taxonomies.get(tax_idx):
        taxonomies[tax_idx] = ItemCollection(format, {'type': taxonomy})
    if not taxonomies[tax_idx].get_item_by('type', term):
        taxonomies[tax_idx].items.append(ItemCollection(
            format, {'type': term, 'parent_type': taxonomy}
        ))
    data = item.copy()
    data['parent_type'] = taxonomy
    taxonomies[tax_idx].get_item_by('type', term).add_item(data)

    return taxonomies
