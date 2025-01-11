from celery import app
from albert_heijn import AHConnector
from jumbo import JumboConnector
import pika

import os
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.task
def fetch_albert_heijn():
    logging.info("Starting to fetch data from Albert Heijn API.")
    try:
        connection_AH = AHConnector()
        logger.info("Connected to Albert Heijn API.")
        data = list(connection_AH.search_all_products())

        folder_path = "api_celery/data"
        file_path = os.path.join(folder_path, "savedata_AH.json")
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder: {folder_path}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted existing file: {file_path}")
        
        with open(file_path, "w") as save_file:
            json.dump(data, save_file, indent=1)
        
        logger.info("Data successfully fetched and saved to 'savedata_AH.json'.")

        # Send the JSON file to RabbitMQ
        send_json_file(file_path, queue_name="AH_json_files")
        logger.info("Sent 'savedata_AH.json'.")

    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")

# @app.task
# def fetch_jumbo():
#     logging.info("Starting to fetch data from Jumbo API.")
#     try:
#         connection_jumbo = JumboConnector()
#         logger.info("Connected to Jumbo API.")
#         data = list(connection_jumbo.search_all_products())

#         folder_path = "api_celery/data"
#         file_path = os.path.join(folder_path, "savedata_jumbo.json")
        
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
#             logger.info(f"Created folder: {folder_path}")
        
#         if os.path.exists(file_path):
#             os.remove(file_path)
#             logger.info(f"Deleted existing file: {file_path}")
        
#         with open(file_path, "w") as save_file:
#             json.dump(data, save_file, indent=1)
        
#         logger.info("Data successfully fetched and saved to 'savedata_jumbo.json'.")

        
#     except Exception as e:
#         logger.error(f"Error occurred while fetching data: {e}")


def send_json_file(file_path, queue_name, chunk_size=8000):
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
