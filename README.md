# mqtt-drones
A MQTT implementation to control a fleet of drones from  a Command center

The Assignment is establish a connection between the Warehouse Command center and a fleet of Drones to deliver an item .
# Technology Used : RabbitMQ , Python pika library
The assignment is a perfect example for MQTT which uses  RPC style communications to link multiple nodes.
# Files
1. The Command center main method invoke is written in warehouse.py which uses the python's pika library and it makes use of the publisher.py file where the rabbit mq messaging brokers connection and management logic is written

2. The drone request handling and reply logic is  written in drone.py which points to receiver.py

3. The warehouse items are structures as a dictionary which contains the item names and the corresponding delivery address.Here the dictionary has assigned only one key . It can be increased to n numbers and the drone code run n number of times in a loop to deliver the items

# Unit Tests
1. Test are included for the manipulation of models .
2. Since pika library is heavily used , test cases are relatively not necessary for the publisherpy and receiver.py .Hence it is ignored.
   But yes to support the solution is working , a video has been made , which shows the live working copy of how the project works and it 
   can be browsed via public shared dropbox link
   # https://www.dropbox.com/sh/v25r5hp47jrkewb/AABUOt63ooD3lBiZGCYnGzfea?dl=0
