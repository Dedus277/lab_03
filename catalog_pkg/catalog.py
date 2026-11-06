from .exceptions import DuplicateIDError, ItemNotFoundError
from .model import Route

class Catalog:
    """Каталог транспортных маршрутов."""

    def __init__(self):
        self.items = {}
    def add(self, item):
        if item_id in self.items:
            raise DuplicateIDError(item_id)
        self.items[item_id] = item

    def get(self, item_id):
        if item_id not in self.items:
            raise ItemNotFoundError(item_id)
        return self.items[item_id]
    def remove(self, item_id):
        if item_id not in self.items:
            raise ItemNotFoundError(item_id)
        del self.items[item_id]
    def find_by_category(self,item_id):
        return [id for id in self.items.values() if id.category == category]