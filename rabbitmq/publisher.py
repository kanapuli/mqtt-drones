#!/Users/venkat/Downloads/scripbox/venv/bin/python3.6

# import the  rabbitmq client library
import pika

# declare a global variable called channel which serves for the messaging bus
channel = None
# warehouse_command - string object to hold the message from warehouse.py
warehouse_command = None
# declare a command flag
"""
command_flag - c00 default value(no action)
               c01 - command center orders the drone to deliver a item
               c02 - drone sends message to command center that it has reached the delivery area
               c03 - drone sends message to the command center that it has unloaded the item
               c04 - drone sends message to the command center that it has reached the parking spot and available for delivery 
"""
command_flag = "c00"

# Callback function  when  pika connects  to rabbitmq


def on_connected(connection):
    """
    Function creates a channel when connection with rabbit mq is successful
    args: connection  is the  rabbitmq connection  object
    """
    # open a channel
    connection.channel(on_open_channel)


def on_open_channel(new_channel):
    """
    Callback function which is called when connection is successful  and in turn it declares a queue
    args: new_channel is the channel object which is to be assigned to the global channel
    """
    # assign new channel  to the global channel variable
    global channel
    channel = new_channel

    # channel is assigned and  declare a queue named scripbox.
    # queue Properties -  durable is True so that the queue withstands rabbitmq reboot
    # Pass a callback on_queue_declared which fires when a queue declaration
    # is successful
    channel.queue_declare(queue='scripbox', durable=True,
                          auto_delete=False, callback=on_queue_declared)


def on_queue_declared(frame):
    """
    Func Called when rabbitmq sends back the frame response that says queue declaration is successful
    """
    #publish the first command to the drone to deliver an item
    channel.basic_publish(exchange='', routing_key='scripbox', body=str(
        command_flag + ':' + warehouse_command))
    print('Waiting for Status update from the drone')
    #declare a queue_list which contains the command flags
    queue_list= ['c02','c03','c04']
    #Start consuming for the  replies from the drone status. Loop for each command_flag
    while True: 
        for q in (queue_list):
            #create a new broker connection to consume the drone status messages
            credential = pika.PlainCredentials('guest', 'guest')
            rpc_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, virtual_host='/', credentials=credential))
            #create a new channel called rpc_newchannel
            rpc_channel = rpc_connection.channel()
            #queues are delcared in the name of command_flags
            rpc_channel.queue_declare(queue=q)
            #Get the messages using pika Blocking connection method called channel.basic_get
            method_frame ,header_frame,body = rpc_channel.basic_get(q)
            if method_frame:
                print(body)
                rpc_channel.basic_ack(method_frame.delivery_tag)
           

def start_connection(flag, item_for_delivery):
    """
    Starts the Rabbit Mq connection with the basic parameters
    """
    # Assign the item_for_delivery to the  global warehouse_command
    global warehouse_command
    warehouse_command = item_for_delivery
    # Assign the flag to the global command_flag
    global command_flag
    command_flag = flag
    # The Rabbit mq runs in the localhost and the username , password is
    # athavan
    credentials = pika.PlainCredentials('guest', 'guest')
    # Pass the mqhost , port , virtualhost and credentials
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.SelectConnection(parameters, on_connected)
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        # close the connnection
        connection.close()
        # loop until we are fully closed. It will stop on its own
        connection.ioloop.start()
