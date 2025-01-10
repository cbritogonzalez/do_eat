# #!/usr/bin/env python
# import pika
# import json
# import os

# def send_json_file(file_path, queue_name):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    
#     # Create a new channel for this file
#     channel = connection.channel()
#     channel.queue_declare(queue=queue_name)

#     # Read the JSON file
#     with open(file_path, 'r') as json_file:
#         json_data = json.load(json_file)

#     # Convert the JSON data to a string for sending
#     message = json.dumps(json_data)

#     # Send the message to the queue
#     channel.basic_publish(exchange='', routing_key=queue_name, body=message)
#     print(f" [x] Sent data from {file_path} to queue '{queue_name}'")

#     # Close the channel after sending
#     channel.close()
#     connection.close()


# if __name__ == "__main__":
#     # Example JSON files to send
#     # json_files = ["api_celery/savedata_AH.json", "api_celery/savedata_jumbo.json"]
#     json_files = ["api_celery/savedata_jumbo.json"]

#     for file_path in json_files:
#         if os.path.exists(file_path):
#             send_json_file(file_path, queue_name='json_files')
#         else:
#             print(f" [!] File {file_path} does not exist.")

#!/usr/bin/env python
import pika
import json
import os


def send_json_file(file_path, queue_name, chunk_size=5000):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    # Read the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Split data into chunks
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    for idx, chunk in enumerate(chunks):
        # Convert the JSON chunk to a string for sending
        message = json.dumps(chunk)

        # Send the message to the queue
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent chunk {idx + 1}/{len(chunks)} to queue '{queue_name}'")

    channel.close()
    connection.close()


if __name__ == "__main__":
    # Example JSON files to send
    json_files = ["api_celery/data/savedata_AH.json", "api_celery/data/savedata_jumbo.json"]
    # json_files = ["api_celery/savedata_jumbo.json"]

    for file_path in json_files:
        if os.path.exists(file_path):
            send_json_file(file_path, queue_name='json_files')
        else:
            print(f" [!] File {file_path} does not exist.")
