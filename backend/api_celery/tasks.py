from api_celery.celery import app
# from celery import app
from api_celery.albert_heijn import AHConnector
# from albert_heijn import AHConnector
from api_celery.jumbo import JumboConnector
# from jumbo import JumboConnector
import pika

import os
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CHUNK_SIZE = 15777216

# @app.task
# def fetch_albert_heijn():
#     logging.info("Starting to fetch data from Albert Heijn API.")
#     try:
#         connection_AH = AHConnector()
#         logger.info("Connected to Albert Heijn API.")
#         data = list(connection_AH.search_all_products())
        
#         logger.info("Data successfully fetched from Albert Heijn API.")

#         data_json = json.dumps(data, indent=1)

#         send_json_data(data_json, queue_name="AH_json")
#         logger.info("Data successfully sent to RabbitMQ queue 'AH_json'.")
#     except Exception as e:
#         logger.error(f"Error occurred while fetching data: {e}")

@app.task
def fetch_jumbo():
    logging.info("Starting to fetch data from Jumbo API.")
    try:
        connection_jumbo = JumboConnector()
        logger.info("Connected to Jumbo API.")
        data = list(connection_jumbo.search_all_products())
        logger.info("Data successfully fetched from Jumbo.")

        data_chunks = list(chunk_data(data, CHUNK_SIZE))

        # Send each chunk to RabbitMQ
        for i, chunk in enumerate(data_chunks):
            data_json = json.dumps(chunk, indent=1)
            send_json_data(data_json, queue_name="Jumbo_json")
            logger.info(f"Chunk {i+1} of {len(data_chunks)} sent to RabbitMQ queue 'Jumbo_json'.")

        # data_json = json.dumps(data, indent=1)

        # send_json_data(data_json, queue_name="Jumbo_json")
        # logger.info("Data successfully sent to RabbitMQ queue 'Jumbo_json'.")

        
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")


def chunk_data(data, chunk_size):
    """
    Split the data into chunks of a specified size.
    Ensures that the chunk size doesn't exceed the max limit for RabbitMQ.
    """
    chunk = []
    current_size = 0
    for item in data:
        item_size = len(json.dumps(item).encode('utf-8'))  # Get the size of the item in bytes
        if current_size + item_size > chunk_size:
            yield chunk  # Yield the current chunk
            chunk = [item]  # Start a new chunk
            current_size = item_size
        else:
            chunk.append(item)
            current_size += item_size

    # Yield the last chunk
    if chunk:
        yield chunk

def send_json_data(data_json, queue_name):
    """
    Sends the serialized JSON data to a RabbitMQ queue.
    """
    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=queue_name)

        # Publish the JSON data to the queue
        channel.basic_publish(exchange='', routing_key=queue_name, body=data_json)
        logger.info(f"JSON data sent to queue '{queue_name}'.")

        # Close the connection
        connection.close()

    except Exception as e:
        logger.error(f"Error while sending data to RabbitMQ: {e}")