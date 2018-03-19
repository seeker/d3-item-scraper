import unittest

from d3is.parser import Parser
from d3is.item import Item
from d3is.loader import Loader
from betamax import Betamax
from requests import Session
from filter import ExtractionFilter

CASSETTE_LIBRARY_DIR = 'test/cassettes'

CAT_WEAPONS = 'weapons'
CAT_ARMOR = 'armor'
CAT_JEWLRY = 'jewelry'

CAT_ARMOR_ITEM_COUNT = 13;
CAT_WEAPONS_ITEM_COUNT = 29;
PARSED_ITEM_COUNT = 36;

class TestParser(unittest.TestCase):
    url_prefix = '/en/item'
    url_item = Loader.ITEM_BASE_URL
    url_ring = url_item + 'ring/'

    def setUp (self):
        session = Session()
        recorder = Betamax(
            session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )
    
        with recorder.use_cassette('ring-page'):
            self.ring_page = session.get(self.url_ring).text
            
        with recorder.use_cassette('item-page'):
            self.item_page = session.get(self.url_item).text
        
        self.parse_pages()

    def parse_pages(self, item_filter = None):
        self.cut = Parser(item_filter)
        self.categories = self.cut.categories(self.get_item_page())
        self.items = self.cut.items(self.get_ring_page())

    def get_ring_page(self):
        return self.ring_page
    
    def get_item_page(self):
        return self.item_page

    def test_parsed_item_count(self):
        self.assertEqual(len(self.items), PARSED_ITEM_COUNT)
        
    def test_parsed_item_text_with_variables(self):
        self.assertIn(Item("Halo of Karini", "You take 74% less damage for 5 seconds after your Storm Armor electrocutes an enemy more than 15 yards away. (Wizard Only) [60 - 80]%"), self.items)
        
    def test_parsed_item_text_with_symbols(self):
        self.assertIn(Item("The Tall Man's Finger", "Zombie Dogs instead summons a single gargantuan dog with more damage and health than all other dogs combined. (Witch Doctor Only)"), self.items)

    def test_parsed_item_text(self):
        self.assertIn(Item("Ring of Royal Grandeur", "Reduces the number of items needed for set bonuses by 1 (to a minimum of 2)."), self.items)
        
    def test_last_page_parsed(self):
        self.assertIn(Item("Briggs' Wrath","Uncursed enemies are pulled to the target location when a curse is applied to them. (Necromancer Only)"), self.items)

    def test_parsed_pages(self):
        self.assertEqual(self.cut.pages(self.get_ring_page()), 3)
        
    def test_parse_category_weapons(self):
        self.assertIn(CAT_WEAPONS, self.categories)
        
    def test_parse_category_armor(self):
        self.assertIn(CAT_ARMOR, self.categories)
        
    def test_parse_category_jewelry(self):
        self.assertIn(CAT_JEWLRY, self.categories)
        
    def test_parse_category_weapons_dagger_link(self):
        self.assertIn(self.url_prefix + '/dagger/',self.categories[CAT_WEAPONS])
        
    def test_parse_category_armor_boots_link(self):
        self.assertIn(self.url_prefix + '/boots/',self.categories[CAT_ARMOR])
        
    def test_parse_category_jewelry_link(self):
        self.assertListEqual(self.categories[CAT_JEWLRY], [self.url_prefix + '/amulet/',self.url_prefix + '/ring/'])
        
    def test_amulet_not_in_armor_category(self):
        self.assertNotIn(self.url_prefix + '/amulet/', self.categories[CAT_ARMOR])
        
    def test_ring_not_in_armor_category(self):
        self.assertNotIn(self.url_prefix + '/ring/', self.categories[CAT_ARMOR])
        
    def test_follower_item_enchantress_not_in_weapons(self):
        self.assertNotIn(self.url_prefix + '/enchantress-focus/',self.categories[CAT_ARMOR])
    
    def test_follower_item_scoundrel_not_in_weapons(self):
        self.assertNotIn(self.url_prefix + '/scoundrel-token/',self.categories[CAT_ARMOR])
    
    def test_follower_item_templar_not_in_weapons(self):
        self.assertNotIn(self.url_prefix + '/templar-relic/',self.categories[CAT_ARMOR])
        
    def test_weapon_type_count(self):
        self.assertEqual(len(self.categories[CAT_WEAPONS]), CAT_WEAPONS_ITEM_COUNT)

    def test_jewlry_type_count(self):
        self.assertEqual(len(self.categories[CAT_JEWLRY]), 2)
        
    def test_armor_type_count(self):
        self.assertEqual(len(self.categories[CAT_ARMOR]), CAT_ARMOR_ITEM_COUNT)     

    def test_shield_in_weapon_category(self):
        self.assertIn(self.url_prefix + '/shield/', self.categories[CAT_WEAPONS])

    def test_item_filter(self):
        self.parse_pages(ExtractionFilter())

        self.assertNotIn(Item("Hellfire Ring", "Chance on hit to engulf the ground in lava, dealing 200% weapon damage per second for 6 seconds."), self.items)
