from splitter import Splitter
from normalizer import Normalizer
import pika
import json

normalizer = Normalizer()

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='normalizer_competingConsumers_queue', durable=False)

def splitter_normalizer(big_message, mode):
    for message in big_message:
        if mode == 'jumbo':
            norm_message = normalizer.normalize_jumbo(message)
        elif mode == 'AH':
            category = message.get("mainCategory")
            if category not in ["Drogisterij", "Gezondheid, sport", "Baby en kind", "Huishouden", "Huisdier", "Koken, tafelen, vrije tijd"]:
                norm_message = normalizer.normalize_ah(message)
        channel.basic_publish(exchange='',
                            routing_key='normalizer_competingConsumers_queue',
                            body=json.dumps(norm_message),
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # Make message persistent
                            ))

def callback_ah(ch, method, properties, body):
    # Decode and convert the JSON message back to a Python dictionary
    message = json.loads(body.decode())
    print(f"Received: {message}")

    # Insert the product into the database
    splitter_normalizer(message, 'AH')
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

def callback_jumbo(ch, method, properties, body):
    # Decode and convert the JSON message back to a Python dictionary
    message = json.loads(body.decode())
    print(f"Received: {message}")

    # Insert the product into the database
    splitter_normalizer(message, 'jumbo')
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

# Example usage
if __name__ == "__main__":
    try:
        # AH
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Declare the same queue
        channel.queue_declare(queue='AH_json', durable=True)

        # Set up the consumer
        channel.basic_qos(prefetch_count=1)  # Fair dispatch (each consumer consumes 1 message at a time)
        channel.basic_consume(queue='AH_json', on_message_callback=callback_ah)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

        # jumbo
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Declare the same queue
        channel.queue_declare(queue='Jumbo_json', durable=True)

        # Set up the consumer
        channel.basic_qos(prefetch_count=1)  # Fair dispatch (each consumer consumes 1 message at a time)
        channel.basic_consume(queue='Jumbo_json', on_message_callback=callback_jumbo)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        

    except KeyboardInterrupt:
        print("Stopping consumers...")

        # finally:
        #     splitter.close_connection()
        #     normalizer.close_connection()