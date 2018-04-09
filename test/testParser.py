import unittest

from d3is.parser import Parser
from d3is.item import Item
from d3is.loader import Loader
from betamax import Betamax
from requests import Session
from d3is.filter import ExtractionFilter

CASSETTE_LIBRARY_DIR = 'test/cassettes'

CAT_WEAPONS = 'weapons'
CAT_ARMOR = 'armor'
CAT_JEWLRY = 'jewelry'

CAT_ARMOR_ITEM_COUNT = 13;
CAT_WEAPONS_ITEM_COUNT = 29;
PARSED_ITEM_COUNT = 65;

ITEMS = None

class TestParser(unittest.TestCase):
    url_prefix = '/en/item'
    url_item = Loader.ITEM_BASE_URL
    url_ring = url_item + 'ring/'
    url_bracer = url_item + 'bracers/'

    @classmethod
    def setUpClass(cls):
        session = Session()
        recorder = Betamax(
            session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )

        with recorder.use_cassette('ring-page'):
            cls.ring_page = session.get(cls.url_ring).text
            
        with recorder.use_cassette('item-page'):
            cls.item_page = session.get(cls.url_item).text

        with recorder.use_cassette('bracer-page'):
            cls.bracer_page = session.get(cls.url_bracer).text
        
        cls.parse_pages(cls)

    def setUp(self):
        self.items = TestParser.ITEMS

    def parse_pages(cls, item_filter = None):
        cls.cut = Parser(item_filter)
        cls.categories = cls.cut.categories(cls.item_page)
        cls.ITEMS = cls.cut.items(cls.ring_page)
        cls.ITEMS.extend(cls.cut.items(cls.bracer_page))

    def get_item_by_name(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item

        return None

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
        self.assertEqual(self.cut.pages(self.ring_page), 3)
        
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

        self.assertNotIn(Item("Hellfire Ring", "Chance on hit to engulf the ground in lava, dealing 200% weapon damage per second for 6 seconds."), self.ITEMS)

    def test_set_item(self):
        self.assertIn(Item("Krelm's Buff Bracers", "You are immune to Knockback and Stun effects."),self.items)

    def test_wizard_restriction(self):
        test_item = self.get_item_by_name("Manald Heal")

        self.assertEqual(test_item.class_restriction, "Wizard")

    def test_barbarian_restriction(self):
        test_item = self.get_item_by_name("Band of Might")

        self.assertEqual(test_item.class_restriction, "Barbarian")

    def test_necromancer_restriction(self):
        test_item = self.get_item_by_name("Circle of Nailuj's Evol")

        self.assertEqual(test_item.class_restriction, "Necromancer")

    def test_monk_restriction(self):
        test_item = self.get_item_by_name("Band of the Rue Chambers")

        self.assertEqual(test_item.class_restriction, "Monk")

    def test_witch_doctor_restriction(self):
        test_item = self.get_item_by_name("The Short Man's Finger")

        self.assertEqual(test_item.class_restriction, "Witch Doctor")

    def test_crusader_restriction(self):
        test_item = self.get_item_by_name("Eternal Union")

        self.assertEqual(test_item.class_restriction, "Crusader")

    def test_demon_hunter_restriction(self):
        test_item = self.get_item_by_name("Elusive Ring")

        self.assertEqual(test_item.class_restriction, "Demon Hunter")

