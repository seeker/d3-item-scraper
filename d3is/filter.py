import logging


class ExtractionFilter:
    """
    Class to filter items that cannot be extracted with Kanai's cube.
    """

    excluded_items = ['Hellfire', 'Paddle', 'Pig Sticker', 'Cluckeye', 'Ashbringer']

    def filter_item_name(self, item):
        """
        Check if the item should be filtered.
        :param item:  the item to check
        :return: true if the item is filtered
        """

        for exclude in self.excluded_items:
            if exclude in item.name:
                logging.debug("{} cannot be extracted".format(item.name))
                return True

        return False
