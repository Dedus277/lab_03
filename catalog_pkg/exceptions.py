class CatalogError(Exception):
    """Базовая ошибка каталога."""


class InvalidEntityError(CatalogError):
    """Сущность нарушает инварианты при создании объекта."""


class DuplicateIDError(CatalogError):
    """Объект с таким ID уже есть в каталоге."""

    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__(f"Маршрут с ID {item_id} уже существует.")


class ItemNotFoundError(CatalogError):
    """Объект с таким ID не найден в каталоге."""

    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__(f"Маршрут с ID {item_id} не найден.")


class UnsupportedVersionError(CatalogError):
    """Версия формата файла не поддерживается."""

    def __init__(self, version):
        self.version = version
        super().__init__(f"Неподдерживаемая версия формата: {version}.")


class CorruptedFileError(CatalogError):
    """Файл каталога повреждён или имеет неверную структуру."""
