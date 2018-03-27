class Item(object):
    """
    Class that holds item data.
    """

    def __init__(self, name, affix, class_restriction = None):
        """
        Create a new item instance to store data.
        :param name: the name of the item
        :param affix: the legendary affix of a item
        :param class_restriction: the character class this item is restricted to. None means the affix is not restricted
         to a class. Other restrictions (e.g. weapon type) still apply
        """
        self.name = name.strip()
        self.affix = affix.strip()
        if class_restriction is not None:
            self.class_restriction = class_restriction.strip()
        else:
            self.class_restriction = None
    
    def __eq__(self, other):
        return self.name == other.name and self.affix == other.affix
    
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