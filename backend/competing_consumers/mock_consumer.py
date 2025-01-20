import pika
import json
from psycopg2 import sql
import psycopg2
import time
import os

# Read environment variables
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
db_host = os.getenv('POSTGRES_HOST', 'localhost')  # Default to 'localhost' if not set
db_port = os.getenv('POSTGRES_PORT', '5432')  # Default to '5432' if not set

def insert_product(data):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()

        # replace market with corresponding ID
        if data["market"] == "jumbo":
            data["market"] = 1
        elif data["market"] == "AH":
            data["market"] = 2

        # Prepare the INSERT statement
        insert_query = sql.SQL("""
            INSERT INTO products (product_title, brand, bonus_start_date, bonus_end_date, 
                                  bonus_mechanism, initial_price, final_price, market_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """)

        # Prepare data for insertion
        values = (
            data["title"],
            data["brand"],
            data["bonus_start_date"],
            data["bonus_end_date"],
            data["bonus_mechanism"],
            data["initial_price"],
            data["final_price"],
            data["market"]
        )

        # Execute the INSERT statement
        cursor.execute(insert_query, values)
        connection.commit()  # Commit the transaction
        print(f"Inserted: {data}")

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def callback(ch, method, properties, body):
    # Decode and convert the JSON message back to a Python dictionary
    message = json.loads(body.decode())
    print(f"Received: {message}")

    # Insert the product into the database
    insert_product(message)
    # time.sleep (20)
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message


# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the same queue
channel.queue_declare(queue='normalizer_competingConsumers_queue', durable=False)

# Set up the consumer
channel.basic_qos(prefetch_count=1)  # Fair dispatch (each consumer consumes 1 message at a time)
channel.basic_consume(queue='normalizer_competingConsumers_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
