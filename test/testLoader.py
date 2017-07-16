import unittest

from d3is.parser import Parser
from d3is.loader import Loader
from d3is.item import Item
from betamax import Betamax
from requests import Session

BASE_URL = 'https://eu.battle.net'

CASSETTE_LIBRARY_DIR = 'test/cassettes'

CAT_WEAPONS = 'weapons'
CAT_ARMOR = 'armor'
CAT_JEWLRY = 'jewelry'

CAT_ARMOR_ITEM_COUNT = 19;
CAT_WEAPONS_ITEM_COUNT = 23;
PARSED_ITEM_COUNT = 38;

class TestLoader(unittest.TestCase):
    url_ring = 'https://us.battle.net/d3/en/item/ring/'
    url_item = 'https://eu.battle.net/d3/en/item/'

    def setUp (self):
        session = Session()
        recorder = Betamax(
            session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )
    
        with recorder.use_cassette('ring-page'):
            self.ring_page = session.get(self.url_ring).text
            
        with recorder.use_cassette('item-page'):
            self.item_page = session.get(self.url_item).text
        
        self.cut = Loader(BASE_URL, session)

    def test_load_rings(self):
        html = self.cut.load_items_html("/d3/en/item/ring/")
        
        self.assertIn("Halo of Karini", html)
