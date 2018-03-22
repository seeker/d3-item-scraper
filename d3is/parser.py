from bs4.element import SoupStrainer
from bs4 import BeautifulSoup
from d3is.item import Item
from itertools import filterfalse
import logging

class Parser(object):
    '''
    Parses html into items.
    '''
    import re
    from bs4 import SoupStrainer
    from d3is.item import Item
    
    filter_legendary = SoupStrainer('tr')
    filter_ul = SoupStrainer('ul')
    
    follower_item_filter = re.compile('.*(enchantress\-focus|scoundrel\-token|templar\-relic)/$')

    def __init__(self, item_filter=None):
        self.item_filter = item_filter


    def parse_jewelry(self,jewelry_links, plain_link):
        for j in ['ring', 'amulet']:
            if j in plain_link:
                jewelry_links.append(plain_link)
                return True

        return False

    def parse_offhand(self,weapon_links, plain_link):
        for j in ['shield', 'mojo', 'orb', 'quiver', 'phylactery']:
            if j in plain_link:
                weapon_links.append(plain_link)
                return True

        return False

    def parse_armor_links(self, soup, result_dict):
        """
        Parse the armor category.
        This will be split up into armor, jewelry and weapons.
        This is due to Kanai's cube categorising offhand items as weapons.
        """
        
        armor = soup.select_one("div.column-1")
        links = armor.find_all("a", href=True)
        
        armor_links = []
        jewelry_links = []
        weapon_links = []

        for link in links:
            plain_link = link['href']

            if self.follower_item_filter.match(plain_link) is not None:
                continue
            
            if self.parse_jewelry(jewelry_links, plain_link):
                continue

            if self.parse_offhand(weapon_links,  plain_link):
                continue

            armor_links.append(plain_link)

        result_dict['jewelry'] = jewelry_links
        result_dict['armor'] = armor_links
        result_dict['weapons'] = weapon_links

    def parse_weapon_links(self, soup, result_dict):
        '''
        Parse the weapon category.
        '''

        weapons = soup.select_one("div.column-2")
        weapon_links_elem = weapons.find_all("a", href=True)

        weapon_links = []
        for link in weapon_links_elem:
            weapon_links.append(link['href'])

        result_dict['weapons'].extend(weapon_links)

    def filter_items(self, items):
        items[:] = filterfalse(self.item_filter.filter_item_name, items)

    def categories(self, html):
        '''
        Returns a dict with the categories and matching links
        '''
        categories = {}
        soup = BeautifulSoup(html, "html.parser")

        self.parse_armor_links(soup, categories)
        self.parse_weapon_links(soup, categories)

        return categories;

    def items(self, html):
        """
        Parse and return the items on a item page.
        Only items with an orange affix text will be returned.
        :param html: html of a page to parse
        :return: a array of items with a legendary affix
        """
        
        rows = BeautifulSoup(html, "html.parser")
        legendaries = rows.select("tr.legendary")
        set_items = rows.select("tr.set")

        items = self.extract_items('d3-color-orange', legendaries)
        sets = self.extract_items('d3-color-green',set_items)
        items.extend(sets)

        return items

    def extract_items(self, class_, item_elements):
        """
        Extract item data from elements. Only items with a legendary affix will be extracted.
        :param class_: class that identifies the item name
        :param item_elements: elements containing items to extract
        :return: a array of extracted items
        """
        items = []

        for element in item_elements:
            try:
                item_name = element.find('a', class_=class_).text

                if item_name == "Ring of Royal Grandeur":
                    '''
                    Blizzard uses the wrong color on the item page, which breaks the parser.
                    '''
                    items.append(Item(item_name, "Reduces the number of items needed for set bonuses by 1 (to a minimum of 2)."))
                    continue

                item_text = self.extract_item_affix(element)

                if item_text == None:
                    logging.debug("{} has no affix, skipping...".format(item_name))
                    continue

                items.append(Item(item_name, item_text))
            except(AttributeError):
                logging.error("Failed to parse {}".format(item_name))

        if self.item_filter is not None:
            self.filter_items(items)

        return items

    def extract_item_affix(self, elem):
        """
        Extract the legendary affix of an item, if any.
        :param elem: the item for which to extract the affix
        :return: the affix text, or None if there is no affix
        """
        text = elem.find('span', class_='d3-color-ffff8000')
        class_name = elem.find('span', class_='d3-color-ffff0000')
        range = elem.find('span', class_='d3-color-ff9b9b9b')

        if text == None:
            return None

        item_text = text.text

        if class_name != None:
            item_text += (' ' + class_name.text)

        if range != None:
            item_text += (' ' + range.text)

        return item_text
    
    def pages(self, html):
        '''
        Get the number of pages on the item page.
        '''
        
        ul = BeautifulSoup(html, 'html.parser', parse_only=self.filter_ul)
        pagination = ul.find('ul', class_='ui-pagination')
        return len(pagination.find_all('a'))
