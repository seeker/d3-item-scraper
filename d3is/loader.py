'''
Created on 16 Jul 2017

@author: Nicholas Wright
'''
from requests import Session

import logging

class Loader(object):
    '''
    Class for loading html from links for parsing.
    '''

    def __init__(self, base_url, session = Session()):
        '''
        Create a new loader to load HTML from URLs.
        :param base_url the URL relative URLs will be resolved against
        '''
        self.base_url = base_url
        self.session = session;

    def load_items_html(self, item_page_link):
        '''
        Load HTML for a given item page
        :param item_page_link relative link to an item page (e.g. /d3/en/item/helm/)
        '''
        link = "{}{}".format(self.base_url,item_page_link)
        logging.debug("Processing link {}".format(link))
        return self.session.get(link).text
