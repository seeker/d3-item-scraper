class Item(object):
    """
    Class that holds item data.
    """

    def __init__(self, name, affix):
        self.name = name.strip()
        self.affix = affix.strip()
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self, *args, **kwargs):
        """
        Return the string representation of the instance.
        Outputs item name and the affix text.
        """
        
        return "{}: {}".format(self.name, self.affix)
    
    def __repr__(self, *args, **kwargs):
        """
        Returns the string representation when the class is used in collections.
        """
        
        return self.__str__()