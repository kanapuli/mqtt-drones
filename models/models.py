#declare a item variable
warehouse_item = {}

def get_warehouse_items():
    """
    items - dictionary of item name and the delivery address
    returns: It returns a dictionary of warehouse itemes that need to be delivered
    """
    global warehouse_item
    items = { 
        'item1': 'Scripbox Inc ,6th floor, GoldenTower,old airport road,Bengaluru,Karnataka'
        }
    warehouse_item  = items
    return items

def remove_warehouse_item(key):
    """
    Removes the warehouse item  with specified name from the dictionary
    args: key - dictionary item Name
    returns: None
    """
    #check whether the  key exists . __contains__ returns a bool
    if warehouse_item.__contains__(key):
        warehouse_item.pop(key)
