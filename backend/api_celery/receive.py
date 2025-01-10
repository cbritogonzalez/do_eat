#!/usr/bin/env python
import pika
import json
import sys
import os
from datetime import datetime


def save_received_data(json_data):
    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"received_data_{timestamp}.json"
    file_path = os.path.join("api_celery", file_name)

    # Ensure the directory exists
    os.makedirs("api_celery", exist_ok=True)

    # Write the JSON data to a file
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=2)
    
    print(f" [x] Data saved to {file_path}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='json_files')

    # Define the callback for message processing
    def callback(ch, method, properties, body):
        print(f" [x] Received message")
        try:
            # Parse the JSON data
            json_data = json.loads(body)
            print(" [x] Received Data:", json_data)

            # Save the received data to a JSON file
            save_received_data(json_data)

        except json.JSONDecodeError as e:
            print(f" [!] Error decoding JSON: {e}")

    # Consume messages from the queue
    channel.basic_consume(queue='json_files', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
