import json
from dataclasses import asdict

from .catalog import Catalog
from .exceptions import (
    CorruptedFileError,
    DuplicateIDError,
    InvalidEntityError,
    UnsupportedVersionError,
)
from .model import Route

FORMAT_VERSION = 1


def route_to_dict(route):
    return asdict(route)


def route_from_dict(data):
    if not isinstance(data, dict):
        raise CorruptedFileError("Запись должна быть словарём")
    try:
        return Route(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            year=data["year"],
            length_km=data["length_km"],
            stop_count=data["stop_count"],
        )
    except (KeyError, InvalidEntityError):
        raise CorruptedFileError("Запись повреждена")


def save(catalog, path):
    data = {
        "format_version": FORMAT_VERSION,
        "items": [route_to_dict(r) for r in catalog],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(catalog, path):
    # 1. Читаем и разбираем JSON. Каталог пока не трогаем.
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise CorruptedFileError(f"Не удалось прочитать файл: {e}")

    # 2. Проверяем корень и версию.
    if not isinstance(data, dict) or "format_version" not in data:
        raise CorruptedFileError("В корне нет поля format_version.")
    if data["format_version"] != FORMAT_VERSION:
        raise UnsupportedVersionError(data["format_version"])
    items = data.get("items")
    if not isinstance(items, list):
        raise CorruptedFileError("Поле items должно быть списком.")

    # 3. Собираем всё во ВРЕМЕННЫЙ каталог.
    temp = Catalog()
    for raw in items:
        route = route_from_dict(raw)
        try:
            temp.add(route)
        except DuplicateIDError as e:
            raise CorruptedFileError(f"В файле повторяется ID {e.item_id}.")

    # 4. Всё прошло: одним действием подменяем содержимое.
    catalog.replace_with(temp)