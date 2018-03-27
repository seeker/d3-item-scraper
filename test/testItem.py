import unittest
from d3is.item import Item


class Test(unittest.TestCase):

    def setUp(self):
        self.item_a = Item("foo", "bar")
        self.item_b = Item("foo", "bar")
        self.item_c = Item("fo", "bar")
        self.item_d = Item("foo", "baz")
        self.item_e = Item(" foo ", " baz ")
        self.item_f = Item("foo", "bar", "baz")

    def test_equal(self):
        self.assertTrue(self.item_a == self.item_b)

    def test_not_equal_name(self):
        self.assertTrue(self.item_a != self.item_c)
    
    def test_not_equal_affix(self):
        self.assertTrue(self.item_a != self.item_d)
        
    def test_item_string(self):
        self.assertEqual(str(self.item_a), "foo: bar")
        
    def test_item_repr(self):
        self.assertEqual(str([self.item_a]), "[foo: bar]")

    def test_text_trim(self):
        self.assertEqual(self.item_d, self.item_e)

    def test_equal_with_different_class_restriction(self):
        self.assertEqual(self.item_a, self.item_f)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
