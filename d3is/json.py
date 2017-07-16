'''
Created on 6 Jul 2017

@author: Nicholas Wright
'''
from json import JSONEncoder

class JsonItemEncoder(JSONEncoder):
    '''
    Simple Json encoder to encode items to json
    '''

    def default(self, o):
        try:
            item = {}
            item['name'] = o.name
            item['affix'] = o.affix
        except TypeError:
            pass
        else:
            return item

        return JSONEncoder.default(self, o)
