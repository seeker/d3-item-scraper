'''
Created on 6 Jul 2017

@author: Nicholas Wright
'''
import unittest

from d3is.item import Item
from d3is.customJson import JsonItemEncoder
from nose.tools import assert_raises

import json

class Test(unittest.TestCase):

    def setUp(self):
        self.item = Item("foo", "bar")
        self.item2 = Item("baz", "boo", "onion knight")
        self.items = [self.item, self.item2]

    def test_encode_item(self):
        self.assertEqual('{"affix": "bar", "name": "foo"}', json.dumps(self.item, cls=JsonItemEncoder, sort_keys=True))

    def test_item_list(self):
        self.assertIn(self.item, self.items)
        self.assertIn(self.item2, self.items)

    def test_encode_list_of_items(self):
        self.assertEqual('[{"affix": "bar", "name": "foo"}, {"affix": "boo", "name": "baz", "restriction": "onion knight"}]', json.dumps(self.items, cls=JsonItemEncoder, sort_keys=True))

    def test_encode_not_item(self):
        assert_raises(TypeError, json.dumps, Dummy, cls=JsonItemEncoder)


class Dummy:
    foo = "bar"
