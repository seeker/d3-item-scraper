from bs4.element import SoupStrainer
from bs4 import BeautifulSoup
from d3is.item import Item
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

    def __init__(self):
        pass
    
    def parse_armor_links(self, soup, result_dict):
        '''
        Parse the armor category.
        This will be split up into armor and jewelry.
        '''
        
        armor = soup.select_one("div.column-1")
        links = armor.find_all("a", href=True)
        
        armor_links = []
        jewelry_links = []
        for link in links:
            plain_link = link['href']
            skip = False
            
            if self.follower_item_filter.match(plain_link) != None:
                continue
            
            for j in ['ring', 'amulet']:
                if j in plain_link:
                    jewelry_links.append(plain_link)
                    skip = True
            
            if skip:
                continue
            
            armor_links.append(plain_link)
            
        result_dict['jewelry'] = jewelry_links
        result_dict['armor'] = armor_links
    
    def parse_weapon_links(self, soup, result_dict):
        '''
        Parse the weapon category.
        '''
        
        weapons = soup.select_one("div.column-2")
        weapon_links_elem = weapons.find_all("a", href=True)
        
        weapon_links = []
        for link in weapon_links_elem:
            weapon_links.append(link['href'])
        
        result_dict['weapons'] = weapon_links        
    
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
        '''
        Get the items on a item page.
        Only items with an orange affix text will be included.
        '''
        
        rows = BeautifulSoup(html, "html.parser")
        legendaries = rows.select("tr.legendary")
        
        items = []
        
        for leg in legendaries:
            try:
                item_name = leg.find('a', class_='d3-color-orange').text
                text = leg.find('li', class_='d3-color-orange')
                
                if text == None:
                    logging.warn("{} has no affix, skipping...".format(item_name))
                    continue
                
                item_text = text.text
                
                items.append(Item(item_name, item_text))
            except(AttributeError):
                logging.error("Failed to parse {}".format(item_name))
            
        return items
    
    def pages(self, html):
        '''
        Get the number of pages on the item page.
        '''
        
        ul = BeautifulSoup(html, 'html.parser', parse_only=self.filter_ul)
        pagination = ul.find('ul', class_='ui-pagination')
        return len(pagination.find_all('a'))
