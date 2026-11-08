import json
import os
import unittest

from catalog_pkg.catalog import Catalog
from catalog_pkg.exceptions import CorruptedFileError, UnsupportedVersionError
from catalog_pkg.model import Route
from catalog_pkg.storage import load, save

FILE = "test_tmp_catalog.json"


class TestStorage(unittest.TestCase):

    def setUp(self):
        # Каталог, в котором уже лежат два маршрута
        self.catalog = Catalog()
        self.catalog.add(Route("old-1", "Старый 1", "bus", 1990, 12.5, 15))
        self.catalog.add(Route("old-2", "Старый 2", "metro", 1985, 20.0, 12))

    def tearDown(self):
        # После каждого теста удаляем временный файл
        if os.path.exists(FILE):
            os.remove(FILE)

    def test_round_trip(self):
        # Сохранили, загрузили в новый каталог, сравнили
        save(self.catalog, FILE)
        new_catalog = Catalog()
        load(new_catalog, FILE)
        self.assertEqual(list(new_catalog), list(self.catalog))

    def test_file_has_format_version(self):
        save(self.catalog, FILE)
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["format_version"], 1)

    def test_broken_json(self):
        # Пишем в файл текст, который не является JSON
        with open(FILE, "w", encoding="utf-8") as f:
            f.write("это не json")
        with self.assertRaises(CorruptedFileError):
            load(self.catalog, FILE)

    def test_unknown_version(self):
        data = {"format_version": 99, "items": []}
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        with self.assertRaises(UnsupportedVersionError):
            load(self.catalog, FILE)

    def test_bad_record_keeps_catalog(self):
        # В файле три записи, средняя с годом 2999 (невалидный)
        data = {
            "format_version": 1,
            "items": [
                {"id": "a", "name": "А", "category": "bus",
                 "year": 1990, "length_km": 5.0, "stop_count": 4},
                {"id": "b", "name": "Б", "category": "bus",
                 "year": 2999, "length_km": 5.0, "stop_count": 4},
                {"id": "c", "name": "В", "category": "bus",
                 "year": 1990, "length_km": 5.0, "stop_count": 4},
            ],
        }
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with self.assertRaises(CorruptedFileError):
            load(self.catalog, FILE)

        # Каталог остался таким же, как был
        self.assertEqual(len(self.catalog), 2)
        self.assertIn("old-1", self.catalog)
        self.assertIn("old-2", self.catalog)
        self.assertNotIn("a", self.catalog)

    def test_missing_field_keeps_catalog(self):
        # У записи нет поля name
        data = {
            "format_version": 1,
            "items": [
                {"id": "a", "category": "bus",
                 "year": 1990, "length_km": 5.0, "stop_count": 4},
            ],
        }
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with self.assertRaises(CorruptedFileError):
            load(self.catalog, FILE)
        self.assertEqual(len(self.catalog), 2)

    def test_duplicate_id_in_file_keeps_catalog(self):
        # В файле две записи с одним ID
        record = {"id": "a", "name": "А", "category": "bus",
                  "year": 1990, "length_km": 5.0, "stop_count": 4}
        data = {"format_version": 1, "items": [record, record]}
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with self.assertRaises(CorruptedFileError):
            load(self.catalog, FILE)
        self.assertEqual(len(self.catalog), 2)


if __name__ == "__main__":
    unittest.main()