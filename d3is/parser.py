from bs4.element import SoupStrainer
from bs4 import BeautifulSoup
from d3is.item import Item
import logging

class Parser(object):
    '''
    Parses html into items.
    '''
    from bs4 import SoupStrainer
    from d3is.item import Item
    
    filter_legendary = SoupStrainer('tr')
    filter_ul = SoupStrainer('ul')
    
    def __init__(self):
        pass
        
    def items(self, html):
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
        ul = BeautifulSoup(html, 'html.parser', parse_only=self.filter_ul)
        pagination = ul.find('ul', class_='ui-pagination')
        return len(pagination.find_all('a'))
