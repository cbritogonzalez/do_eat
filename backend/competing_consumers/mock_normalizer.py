import pika
import json

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='normalizer_competingConsumers_queue', durable=True)

# Send messages to the queue
for i in range(10):
    # Create a JSON message
    message = {
        "title": "cucumbers",
        "brand": "AH",
        "bonus_start_date": "3/1/2025",
        "bonus_end_date": None,
        "bonus_mechanism": None,
        "initial_price": "1.05",
        "final_price": None,
        "market": "jumbo" #or AH
    }

    # Convert the message to a JSON string
    json_message = json.dumps(message)
    channel.basic_publish(exchange='',
                          routing_key='normalizer_competingConsumers_queue',
                          body=json_message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Make message persistent
                          ))
    print(f"Sent: {json_message}")

# Close the connection
connection.close()