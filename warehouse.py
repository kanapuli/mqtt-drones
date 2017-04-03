
# import the rabbit mq package to initialize and manage the broker
# start_connection
from rabbitmq import publisher as tx
# import models to get the warehouse items
from models import models as m


def main():
    """
    The Warehouse Command publisher method starts here
    """
    # get the warehouse items to be delivered from the models package
    warehouse_items = m.get_warehouse_items()
    # invoke the broker start connection method and pass the  warehouse item
    # as the parameter. The loop runs only once since we have only one item as
    # mentioned in the assignment mail.
    for key in warehouse_items:
        # pass the command_flag(desc is in publisher.py) and the item to be
        # delivered
        tx.start_connection(flag="c01", item_for_delivery=warehouse_items[key])


if __name__ == "__main__":
    main()
