import pika
import json

from normalizer import Normalizer

    # read items from json file and split the message into individual messages
def preprocess_message(input_file):
    try:
        with open(input_file, 'r') as file:
            parsed_messages = json.load(file)
        if not isinstance(parsed_messages, list):
            raise ValueError("Expected JSON to be a list of messages")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading JSON: {e}")
        parsed_messages = []

    return parsed_messages

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='AH_json', durable=True)

# Send messages to the queue
# for i in range(10):
# Create a JSON message
json_message1 = preprocess_message('savedata_AH.json')

# Convert the message to a JSON string
# json_message = json.dumps(message)
channel.basic_publish(exchange='',
                        routing_key='AH_json',
                        body=json.dumps(json_message1).encode('utf-8'),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Make message persistent
                        ))
print(f"Sent: non-normalized message")
# Close the connection
connection.close()