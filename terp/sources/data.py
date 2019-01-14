from collections.abc import Mapping


class Cache(Mapping):
    def __init__(self, *args, **kw):
        self._storage = {
            'source': None,
            'relpath': None,
            'cached': None,
        }
        self._storage.update(dict(*args, **kw))

    def __getitem__(self, key):
        return self._storage[key]
    def __setitem__(self, key, value):
        self._storage[key] = value
    def __len__(self):
        return len(self._storage)
    def __iter__(self):
        return iter(self._storage)
    def __str__(self):
        return self._storage.__str__()

    def copy(self):
        cp = Cache()
        cp._storage = self._storage.copy()
        return cp
