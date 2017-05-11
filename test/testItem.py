'''
Created on 11 May 2017

@author: Nicholas Wright
'''
import unittest
from d3is.item import Item

class Test(unittest.TestCase):


    def setUp(self):
        self.item_a = Item("foo", "bar")
        self.item_b = Item("foo", "bar")
        self.item_c = Item("fo", "bar")
        self.item_d = Item("foo", "baz")


    def tearDown(self):
        pass


    def test_equal(self):
        self.assertTrue(self.item_a == self.item_b)

    def test_not_equal_name(self):
        self.assertTrue(self.item_a != self.item_c)
    
    def test_not_equal_affix(self):
        self.assertTrue(self.item_a != self.item_d)
        
    def test_item_string(self):
        self.assertEqual(str(self.item_a), "foo: bar")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()