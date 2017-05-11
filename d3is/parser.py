from bs4.element import SoupStrainer
from bs4 import BeautifulSoup
from d3is.item import Item
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
        rows = BeautifulSoup(html, "html.parser", parse_only=self.filter_legendary)
        legendaries = rows.find_all(class_="legendary")
        
        items = []
        
        for leg in legendaries:
            try:
                item_name = leg.find('a', class_='d3-color-orange').text
                item_text = leg.find('li', class_='d3-color-orange').text
                items.append(Item(item_name, item_text))
            except(AttributeError):
                print("Failed to parse {}".format(leg))
            
        return items
    
    def pages(self, html):
        ul = BeautifulSoup(html, 'html.parser', parse_only=self.filter_ul)
        pagination = ul.find('ul', class_='ui-pagination')
        return len(pagination.find_all('a'))
