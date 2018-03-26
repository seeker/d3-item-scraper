import unittest

from d3is.filter import ExtractionFilter
from d3is.item import Item

class Test(unittest.TestCase):
    def setUp(self):
        self.cut = ExtractionFilter()

        self.hellfire_ring = Item("Hellfire Ring", "")
        self.hellfire_amulet = Item("Hellfire Amulet", "")

    def test_hellfire_ring_filtered(self):
        self.assertEqual(True, self.cut.filter_item_name(self.hellfire_ring))

    def test_hellfire_amulet_filtered(self):
        self.assertEqual(True, self.cut.filter_item_name(self.hellfire_amulet))


if __name__ == '__main__':
    unittest.main()
