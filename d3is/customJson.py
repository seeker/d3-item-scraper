'''
Created on 6 Jul 2017

@author: Nicholas Wright
'''
from json import JSONEncoder
from d3is.item import Item

class JsonItemEncoder(JSONEncoder):
    '''
    Simple Json encoder to encode items to json
    '''

    def default(self, o):
        if isinstance(o, Item):
            item = {}
            item['name'] = o.name
            item['affix'] = o.affix
            if o.class_restriction is not None:
                item['restriction'] = o.class_restriction
            return item

        return JSONEncoder.default(self, o)
