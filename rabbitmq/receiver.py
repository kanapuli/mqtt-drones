#!/Users/venkat/Downloads/scripbox/venv/bin/python3.6

# import the  rabbitmq client library
import pika
# import the time package to introduce delays
import time
# import the uuid module to generate correlation uuid
import uuid
# declare a global variable called channel which serves for the messaging bus
channel = None
drone_message = None

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
    start_consuming(frame)


def start_consuming(frame):
    channel.basic_consume(on_message_received, queue='scripbox', no_ack=False)


def on_message_received(ch, method, properties, body):
    """
    Callback method which is called when a message is consumed
    """
    # the body contains the command flag followed by a colon ':'  and the message for the drone
    # decode the body to utf8
    received_bytes = body.decode('utf-8')
    # split the received_bytes to get the command _flag and message
    recieved_message = received_bytes.split(':')
    # since rabbit mq body is a byte
    if (str(recieved_message[0]) == "c01"):
        # c01 - command center orders the drone to deliver a item
        print("Order Received from the command center to deliver an item to the following address \n", str(
            recieved_message[1]))
        time.sleep(2)
        # print in the drone's console that the item has been lift off
        print('\nLifting off the Item to the delivery address.')
        print('\nUpdating Status to the command centre ......')
        # Assume the drone has reached the delivery address . Now send a
        # message to the warehouse command center that it has reached the
        # delivery area
        time.sleep(5)
        rpc_sendback("c02")
        # Assume the drone has delivered the item and issue the status message
        # to the command center
        time.sleep(5)
        rpc_sendback("c03")
        # #Assume the drone has reached the parking spot and issue the message to  the command center that is available for next instruction
        time.sleep(5)
        rpc_sendback("c04")

    else:
        print("Received Instruction from Warehouse " +
              str(recieved_message[1]))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    # channel.start_consuming()


def rpc_sendback(rpc_flag):
    """
    Based on the flag , a message will be sent from drone to the rabbit mq broker 
    args : rpc_flag 
               c02 - drone sends message to command center that it has reached the delivery area
               c03 - drone sends message to the command center that it has unloaded the item
               c04 - drone sends message to the command center that it has reached the parking spot and available for delivery 
    """
    credential = pika.PlainCredentials('guest', 'guest')
    rpc_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, virtual_host='/', credentials=credential))
    rpc_channel = rpc_connection.channel()
    rpc_channel.queue_declare(queue=str(rpc_flag))
    #send message to the command center using basic_publish
    if rpc_flag == "c02":
        rpc_channel.basic_publish(exchange='', routing_key=str(
            rpc_flag), body='Drone has reached the delivery address')
    elif rpc_flag == "c03":
        rpc_channel.basic_publish(exchange='', routing_key=str(rpc_flag),
                                  body='Drone has unloaded the item')
    elif rpc_flag == "c04":
        rpc_channel.basic_publish(exchange='', routing_key=str(rpc_flag),
                                  body='Drone has reached the parking spot and available for next instruction')


def consume_message(message):
    """
    Starts the Rabbit Mq connection with the basic parameters
    """
    # Assign the message to the  global drone_message
    global drone_message
    drone_message = message
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
