import unittest

from d3is.parser import Parser
from d3is.item import Item
from betamax import Betamax
from requests import Session

CASSETTE_LIBRARY_DIR = 'test/cassettes'

CAT_WEAPONS = 'weapons'
CAT_ARMOR = 'armor'
CAT_JEWLRY = 'jewelry'

CAT_ARMOR_ITEM_COUNT = 13;
CAT_WEAPONS_ITEM_COUNT = 29;
PARSED_ITEM_COUNT = 36;

class TestParser(unittest.TestCase):
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
        
        self.cut = Parser()
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
        self.assertIn('/d3/en/item/dagger/',self.categories[CAT_WEAPONS])
        
    def test_parse_category_armor_boots_link(self):
        self.assertIn('/d3/en/item/boots/',self.categories[CAT_ARMOR])
        
    def test_parse_category_jewelry_link(self):
        self.assertListEqual(self.categories[CAT_JEWLRY], ['/d3/en/item/amulet/','/d3/en/item/ring/'])
        
    def test_amulet_not_in_armor_category(self):
        self.assertNotIn('/d3/en/item/amulet/', self.categories[CAT_ARMOR])
        
    def test_ring_not_in_armor_category(self):
        self.assertNotIn('/d3/en/item/ring/', self.categories[CAT_ARMOR])
        
    def test_follower_item_enchantress_not_in_weapons(self):
        self.assertNotIn('/d3/en/item/enchantress-focus/',self.categories[CAT_ARMOR])
    
    def test_follower_item_scoundrel_not_in_weapons(self):
        self.assertNotIn('/d3/en/item/scoundrel-token/',self.categories[CAT_ARMOR])
    
    def test_follower_item_templar_not_in_weapons(self):
        self.assertNotIn('/d3/en/item/templar-relic/',self.categories[CAT_ARMOR])
        
    def test_weapon_type_count(self):
        self.assertEqual(len(self.categories[CAT_WEAPONS]), CAT_WEAPONS_ITEM_COUNT)

    def test_jewlry_type_count(self):
        self.assertEqual(len(self.categories[CAT_JEWLRY]), 2)
        
    def test_armor_type_count(self):
        self.assertEqual(len(self.categories[CAT_ARMOR]), CAT_ARMOR_ITEM_COUNT)     

    def test_shield_in_weapon_category(self):
        self.assertIn('/d3/en/item/shield/', self.categories[CAT_WEAPONS])
