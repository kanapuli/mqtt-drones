#import the rabbitmq model for the creation of consumer connection and it's management
from rabbitmq import receiver as rx

def main():
    """
    The drone consumer method starts here
    """
    #call the  receiver consume_message function to consume the channel consume_message
    rx.consume_message("")


if __name__ == '__main__':
    main()
