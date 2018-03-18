#!/usr/bin/env python
# encoding: utf-8
from asyncio.log import logger
if __name__ == "__main__":
    
    from argparse import ArgumentParser
    import requests
    import logging
    import json
    
    from d3is.item import Item
    from d3is.parser import Parser
    from d3is.loader import Loader
    from operator import attrgetter
    from d3is.item import Item
    from d3is.customJson import JsonItemEncoder
    from filter import ExtractionFilter
    
    BASE_URL = 'https://eu.diablo3.com/en/'
    ITEM_BASE_URL = 'https://eu.diablo3.com/en/item/'

    logging.basicConfig(level=logging.INFO)
    
    def process_category(item_page_links):
        '''
        Load and parse all item pages and return a list containing all aggregated items in sorted oder.
        :param item_page_links links to load and parse
        '''
        category_items = []
        
        for item_page_link in item_page_links:
            logger.info("Processing item page {}".format(item_page_link))
            items = parser.items(loader.load_items_html(item_page_link))
            category_items.extend(items)
    
        category_items.sort(key=attrgetter('name'))
        return category_items
    
    parser = Parser(ExtractionFilter())
    loader = Loader(BASE_URL)
    html = loader.load_item_index()
    
    categories = parser.categories(html)
    
    keys = categories.keys()
    
    logger.info("Processing categories: {}".format(keys))
    items = {}

    for key in keys:
        logger.info("Processing category: {}".format(key))
        items[key] = process_category(categories[key])

    with open('items.json', 'w') as outfile:
        json.dump(items, outfile, cls=JsonItemEncoder, sort_keys=True)
