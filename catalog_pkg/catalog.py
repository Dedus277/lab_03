from .exceptions import DuplicateIDError, ItemNotFoundError
from .model import Route

class Catalog:
    """Каталог транспортных маршрутов."""

    def __init__(self):
        self.items = {}
    def add(self, item):
        if item.id in self.items:
            raise DuplicateIDError(item.id)
        self.items[item.id] = item

    def get(self, item_id):
        if item_id not in self.items:
            raise ItemNotFoundError(item_id)
        return self.items[item_id]
    def remove(self, item_id):
        if item_id not in self.items:
            raise ItemNotFoundError(item_id)
        del self.items[item_id]
    def find_category(self, category):
        return [route for route in self.items.values() if route.category == category]
    def find_name(self,name):
        name = name.casefold()
        return [route for route in self.items.values() if name in route.name.casefold()]
    def __len__(self):
        return len(self.items)
    def __iter__(self):
        return iter(tuple(self.items.values()))
    def __contains__(self,item_id):
        return item_id in self.items
