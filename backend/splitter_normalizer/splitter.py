import json
import pika

# Class that splits json file containing all items and processes each item and places in a queue
class Splitter:

    # Initialize RabbitMQ queue
    def __init__(self, rabbitmq_host='localhost', queue_name='supermarket_queue'):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

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
    def enque_message(self, parsed_messages):
        for message in parsed_messages:
            # Publish each message to the RabbitMQ queue
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message)
            )
            print(f"Message enqueued: {message}")

    # consume messages from RabbitMQ queue
    def process_queue(self):
        # Consume messages from the RabbitMQ queue
        def callback(ch, method, properties, body):
            message = json.loads(body)
            print(f"Processing message: {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=False)
        print("Waiting for messages. To exit, press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()


# Example splitter for ah
# if __name__ == "__main__":
#     splitter = Splitter(rabbitmq_host='localhost', queue_name='ah_queue')

#     ah_file = 'savedata_AH.json'

#     parsed_messages_ah = splitter.preprocess_message(ah_file)
#     if parsed_messages_ah:
#         splitter.enque_message(parsed_messages_ah)
#         #splitter.process_queue()

#     splitter.close_connection()






# Test Splitter below
# if __name__ == "__main__":

#     ah_file = 'savedata_AH.json'
#     jumbo_file = 'savedata_jumbo.json'

#     splitter = Splitter()

#     parsed_messages_ah = splitter.preprocess_message(ah_file)
#     parsed_messages_jumbo = splitter.preprocess_message(jumbo_file)
    
#     if parsed_messages_ah and parsed_messages_jumbo:
#         ah_queue = queue.Queue()
#         jumbo_queue = queue.Queue()

#         splitter.enque_message(parsed_messages_ah, ah_queue)
#         splitter.enque_message(parsed_messages_jumbo,jumbo_queue)
#         print(f"ah nr items in queue: {ah_queue.qsize()}")
#         print(f"jumbo nr items in queue: {jumbo_queue.qsize()}")

#         # splitter.process_queue(ah_queue)
#         # splitter.process_queue(jumbo_queue)
