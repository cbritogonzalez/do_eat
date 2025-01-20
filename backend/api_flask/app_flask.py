from flask import Flask, jsonify
from threading import Thread
import schedule
import time
import json
from albert_heijn import AHConnector
from jumbo import JumboConnector
import pika
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 15777216


def send_json_data(data_json, queue_name):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=data_json)
        logger.info(f"JSON data sent to queue '{queue_name}'.")
        connection.close()
    except Exception as e:
        logger.error(f"Error while sending data to RabbitMQ: {e}")


def fetch_albert_heijn():
    logging.info("Starting to fetch data from Albert Heijn API.")
    try:
        connection_ah = AHConnector()
        logger.info("Connected to Albert Heijn API.")
        data = list(connection_ah.search_all_products())
        logger.info("Data successfully fetched from Albert Heijn API.")

        data_json = json.dumps(data, indent=1)
        send_json_data(data_json, queue_name="AH_json")
        logger.info("Data successfully sent to RabbitMQ queue 'AH_json'.")
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")


def fetch_jumbo():
    logging.info("Starting to fetch data from Jumbo API.")
    try:
        connection_jumbo = JumboConnector()
        logger.info("Connected to Jumbo API.")
        data = list(connection_jumbo.search_all_products())
        logger.info("Data successfully fetched from Jumbo.")

        data_chunks = list(chunk_data(data, CHUNK_SIZE))
        for i, chunk in enumerate(data_chunks):
            data_json = json.dumps(chunk, indent=1)
            send_json_data(data_json, queue_name="Jumbo_json")
            logger.info(f"Chunk {i + 1} of {len(data_chunks)} sent to RabbitMQ queue 'Jumbo_json'.")
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")


def chunk_data(data, chunk_size):
    chunk = []
    current_size = 0
    for item in data:
        item_size = len(json.dumps(item).encode('utf-8'))
        if current_size + item_size > chunk_size:
            yield chunk
            chunk = [item]
            current_size = item_size
        else:
            chunk.append(item)
            current_size += item_size
    if chunk:
        yield chunk


def run_scheduler():
    logging.info("Scheduler thread started.")
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/schedule/fetch_albert_heijn', methods=['POST'])
def schedule_ah_task():

    schedule.every(360).seconds.do(fetch_albert_heijn)
    return jsonify({"status": "Scheduled Albert Heijn fetch every 30 seconds"}), 200


@app.route('/schedule/fetch_jumbo', methods=['POST'])
def schedule_jumbo_task():

    schedule.every(300).seconds.do(fetch_jumbo)
    return jsonify({"status": "Scheduled Jumbo fetch every 30 seconds"}), 200


if __name__ == '__main__':
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    app.run(host='0.0.0.0', port=5000)
