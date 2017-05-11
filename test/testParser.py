'''
Created on 11 May 2017

@author: Nicholas Wright
'''
import unittest
import codecs

from d3is.parser import Parser
from d3is.item import Item
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

with Betamax.configure() as config:
    config.cassette_library_dir = 'test/cassettes'

class TestParser(BetamaxTestCase):
    url = 'https://us.battle.net/d3/en/item/ring/'

    def generate_cassette_name(self):
        '''
            Reuse one cassette for all tests
        '''
        return getattr(self, '__class__').__name__

    def setUp (self):
        super(TestParser, self).setUp()
        self.cut = Parser()

    def get_ring_page(self):
        return self.session.get(self.url).text

    def test_parsed_item_count(self):
        items = self.cut.items(self.get_ring_page())
        
        self.assertEqual(len(items), 34)
        
    def test_parsed_item_text_with_variables(self):
        items = self.cut.items(self.get_ring_page())
        
        self.assertIn(Item("Halo of Karini", "You take 45–60% less damage for 3 seconds after your Storm Armor electrocutes an enemy more than 30 yards away."), items)
        
    def test_parsed_item_text_with_symbols(self):
        items = self.cut.items(self.get_ring_page())
        
        self.assertIn(Item("The Tall Man's Finger", "Zombie Dogs instead summons a single gargantuan dog with more damage and health than all other dogs combined."), items)

    def test_parsed_item_text(self):
        items = self.cut.items(self.get_ring_page())
        
        self.assertIn(Item("Ring of Royal Grandeur", "Reduces the number of items needed for set bonuses by 1 (to a minimum of 2)."), items)

    def test_parsed_pages(self):
        self.assertEqual(self.cut.pages(self.get_ring_page()), 4)

if __name__ == "__main__":
    unittest.main()
