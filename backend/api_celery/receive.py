import pika
import json
import threading

def consume_from_queue(queue_name):
    """
    Consumes messages from the specified RabbitMQ queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            print(f" [x] Received data from {queue_name}:")
            # print(json.dumps(data, indent=2))  # Pretty-print the JSON
        except Exception as e:
            print(f"Error while processing message from {queue_name}: {e}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f' [*] Waiting for messages from {queue_name}. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        # Create threads to handle both queues simultaneously
        ah_thread = threading.Thread(target=consume_from_queue, args=('AH_json',))
        jumbo_thread = threading.Thread(target=consume_from_queue, args=('Jumbo_json',))

        # Start the threads
        ah_thread.start()
        jumbo_thread.start()

        # Join threads to keep the program running
        ah_thread.join()
        jumbo_thread.join()
    except KeyboardInterrupt:
        print('Interrupted')
