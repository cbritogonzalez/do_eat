import sys
import os
import json
import pika

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Class that splits json file containing all items and processes each item and places in a queue
class Splitter:

    # Initialize RabbitMQ queue
    def __init__(self, rabbitmq_host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='ah_queue')
        self.channel.queue_declare(queue='jumbo_queue')

    # read items from json file and split the message into individual messages
    def preprocess_message(self, input_file):
        try:
            with open(input_file, 'r') as file:
                parsed_messages = json.load(file)
            if not isinstance(parsed_messages, list):
                raise ValueError("Expected JSON to be a list of messages")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading JSON: {e}")
            parsed_messages = []

        return parsed_messages

    # add the message into a RabbitMQ queue
    def enque_message(self, parsed_messages, queue_name):
        for message in parsed_messages:
            # Publish each message to the RabbitMQ queue
            self.channel.basic_publish(
                exchange='',
                routing_key = queue_name,
                body=json.dumps(message)
            )
            print(f"Message enqueued: {message}")

    def close_connection(self):
        self.connection.close()

