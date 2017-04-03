#import the sys module 
import sys
#append the project path to the sys.path to help python finding up the packages
sys.path.append('/Users/venkat/Downloads/scripbox/')
from models import models as m 
#import the python standard unit test library
import unittest

class ModelsTest(unittest.TestCase):

    def test_item_not_empty(self):
        """
        Check if the item is empty
        """
        items = m.get_warehouse_items()
        self.assertIsNotNone(items)

    def test_item_address_valid(self):
        """
        check if the address is a valid string
        """
        items = m.get_warehouse_items()
        for key in items.keys():
            self.assertNotEqual(items[key] , "")
    
    def test_remove_items(self):
        """
        check if remove item is working
        """
        items = m.get_warehouse_items()
        items.pop('item1')
        self.assertFalse(items.__contains__('item1'))
        


if __name__ == '__main__':
    unittest.main()