import unittest

from catalog_pkg.exceptions import InvalidEntityError
from catalog_pkg.model import Route


class TestRoute(unittest.TestCase):

    def test_valid_route(self):
        r = Route("bus-12", "Вокзал", "bus", 1990, 12.5, 15)
        self.assertEqual(r.id, "bus-12")
        self.assertEqual(r.name, "Вокзал")
        self.assertEqual(r.stop_count, 15)

    def test_empty_id(self):
        with self.assertRaises(InvalidEntityError):
            Route("", "Вокзал", "bus", 1990, 12.5, 15)

    def test_empty_name(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "", "bus", 1990, 12.5, 15)

    def test_wrong_category(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "ship", 1990, 12.5, 15)

    def test_year_too_small(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 1700, 12.5, 15)

    def test_year_in_future(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 2999, 12.5, 15)

    def test_year_is_string(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", "1990", 12.5, 15)

    def test_too_few_stops(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 1990, 12.5, 1)

    def test_stops_is_bool(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 1990, 12.5, True)

    def test_negative_length(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 1990, -3, 15)

    def test_length_is_string(self):
        with self.assertRaises(InvalidEntityError):
            Route("a", "Вокзал", "bus", 1990, "12", 15)


if __name__ == "__main__":
    unittest.main()