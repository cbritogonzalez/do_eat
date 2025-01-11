from splitter import Splitter
from normalizer import Normalizer

# Example usage
if __name__ == "__main__":
    try:
        splitter = Splitter()

        # Enqueue AH data into RabbitMQ queue
        ah_data = splitter.preprocess_message('savedata_AH.json')
        splitter.enque_message(ah_data, 'ah_queue')

        # Enqueue Jumbo data into RabbitMQ queue
        jumbo_data = splitter.preprocess_message('savedata_jumbo.json')
        splitter.enque_message(jumbo_data, 'jumbo_queue')

        normalizer = Normalizer()

        # Process messages from AH queue without consuming them
        print("Processing AH queue...")
        ah_normalized = normalizer.process_messages('ah_queue', normalizer.normalize_ah)
        print(f"Normalized AH messages: {ah_normalized}")

        # Process messages from Jumbo queue without consuming them
        print("Processing Jumbo queue...")
        jumbo_normalized = normalizer.process_messages('jumbo_queue', normalizer.normalize_jumbo)
        print(f"Normalized Jumbo messages: {jumbo_normalized}")

        print("Queues finished processing.")

    except KeyboardInterrupt:
        print("Stopping consumers...")

    finally:
        splitter.close_connection()
        normalizer.close_connection()