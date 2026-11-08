from .exceptions import DuplicateIDError, InvalidEntityError, ItemNotFoundError
from .model import Route


class Catalog:
    """Каталог транспортных маршрутов.

    Порядок итерации: порядок добавления маршрутов (первым идёт тот, кого
    добавили раньше). Повторная итерация даёт тот же порядок. Методы поиска
    возвращают новые списки в том же порядке.
    """

    def __init__(self):
        self._items = {}  # id -> Route

    def add(self, item):
        if not isinstance(item, Route):
            raise InvalidEntityError("В каталог можно добавлять только Route.")
        if item.id in self._items:
            raise DuplicateIDError(item.id)
        self._items[item.id] = item

    def get(self, item_id):
        if item_id not in self._items:
            raise ItemNotFoundError(item_id)
        return self._items[item_id]

    def remove(self, item_id):
        if item_id not in self._items:
            raise ItemNotFoundError(item_id)
        del self._items[item_id]

    def find_by_category(self, category):
        return [r for r in self._items.values() if r.category == category]

    def find_by_name(self, query):
        needle = query.casefold()
        return [r for r in self._items.values() if needle in r.name.casefold()]

    def replace_with(self, other):
        self._items = dict(other._items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(tuple(self._items.values()))

    def __contains__(self, item_id):
        return item_id in self._items