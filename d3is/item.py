class Item(object):
    '''
    Class that holds item data.
    '''

    def __init__(self, name, affix):
        self.name = name
        self.affix = affix
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self, *args, **kwargs):
        return "{}: {}".format(self.name, self.affix)