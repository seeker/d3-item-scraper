import unittest

from d3is.parser import Parser
from d3is.loader import Loader
from d3is.item import Item
from betamax import Betamax
from requests import Session

BASE_URL = Loader.BASE_URL

CASSETTE_LIBRARY_DIR = 'test/cassettes'

CAT_WEAPONS = 'weapons'
CAT_ARMOR = 'armor'
CAT_JEWLRY = 'jewelry'

CAT_ARMOR_ITEM_COUNT = 19;
CAT_WEAPONS_ITEM_COUNT = 23;
PARSED_ITEM_COUNT = 38;

class TestLoader(unittest.TestCase):
    url_ring = Loader.ITEM_BASE_URL + 'ring/'
    url_item = Loader.ITEM_BASE_URL

    def setUp (self):
        session = Session()
        recorder = Betamax(
            session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )

        self.recorder = recorder

        with recorder.use_cassette('ring-page'):
            self.ring_page = session.get(self.url_ring).text
            
        with recorder.use_cassette('item-page'):
            self.item_page = session.get(self.url_item).text
        
        self.cut = Loader(BASE_URL, session)

    def test_load_rings(self):
        with self.recorder.use_cassette('ring-page'):
            html = self.cut.load_items_html("item/ring/")
        
        self.assertIn("Halo of Karini", html)
        
    def test_load_item_index(self):
        with self.recorder.use_cassette('item-page'):
            html = self.cut.load_item_index()
        
        self.assertIn("Rings", html)
