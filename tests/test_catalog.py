import unittest

from catalog_pkg.catalog import Catalog
from catalog_pkg.exceptions import DuplicateIDError, ItemNotFoundError
from catalog_pkg.model import Route


class TestCatalog(unittest.TestCase):

    def setUp(self):
        # Перед каждым тестом создаётся новый пустой каталог
        self.catalog = Catalog()

    def test_add_and_get(self):
        r = Route("a", "Вокзал", "bus", 1990, 12.5, 15)
        self.catalog.add(r)
        self.assertEqual(self.catalog.get("a"), r)
        self.assertEqual(len(self.catalog), 1)

    def test_duplicate_id(self):
        self.catalog.add(Route("a", "Вокзал", "bus", 1990, 12.5, 15))
        with self.assertRaises(DuplicateIDError):
            self.catalog.add(Route("a", "Другой", "metro", 1985, 20.0, 10))
        # каталог не изменился
        self.assertEqual(len(self.catalog), 1)
        self.assertEqual(self.catalog.get("a").name, "Вокзал")

    def test_get_missing(self):
        with self.assertRaises(ItemNotFoundError):
            self.catalog.get("нет-такого")

    def test_remove(self):
        self.catalog.add(Route("a", "Вокзал", "bus", 1990, 12.5, 15))
        self.catalog.remove("a")
        self.assertEqual(len(self.catalog), 0)
        with self.assertRaises(ItemNotFoundError):
            self.catalog.get("a")

    def test_remove_missing(self):
        with self.assertRaises(ItemNotFoundError):
            self.catalog.remove("нет-такого")

    def test_find_by_category(self):
        self.catalog.add(Route("a", "Один", "bus", 1990, 12.5, 15))
        self.catalog.add(Route("b", "Два", "metro", 1990, 12.5, 15))
        self.catalog.add(Route("c", "Три", "bus", 1990, 12.5, 15))
        result = self.catalog.find_by_category("bus")
        ids = [r.id for r in result]
        self.assertEqual(ids, ["a", "c"])

    def test_find_by_name_ignores_case(self):
        self.catalog.add(Route("a", "Вокзал — Университет", "bus", 1990, 12.5, 15))
        self.catalog.add(Route("b", "Центр — Север", "bus", 1990, 12.5, 15))
        result = self.catalog.find_by_name("ВОКЗАЛ")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "a")

    def test_search_result_is_a_copy(self):
        self.catalog.add(Route("a", "Вокзал", "bus", 1990, 12.5, 15))
        result = self.catalog.find_by_category("bus")
        result.clear()  # портим результат поиска
        # каталог от этого не пострадал
        self.assertEqual(len(self.catalog.find_by_category("bus")), 1)

    def test_iteration_order(self):
        self.catalog.add(Route("c", "Один", "bus", 1990, 12.5, 15))
        self.catalog.add(Route("a", "Два", "bus", 1990, 12.5, 15))
        self.catalog.add(Route("b", "Три", "bus", 1990, 12.5, 15))
        first = [r.id for r in self.catalog]
        second = [r.id for r in self.catalog]
        self.assertEqual(first, ["c", "a", "b"])
        self.assertEqual(second, ["c", "a", "b"])

    def test_contains(self):
        self.catalog.add(Route("a", "Вокзал", "bus", 1990, 12.5, 15))
        self.assertTrue("a" in self.catalog)
        self.assertFalse("b" in self.catalog)


if __name__ == "__main__":
    unittest.main()