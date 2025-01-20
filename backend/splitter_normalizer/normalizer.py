import datetime
import json
import pika
from googletrans import Translator
from splitter import Splitter


class Normalizer:
    def __init__(self, rabbitmq_host='rabbitmq'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='normalizer_competingConsumers_queue', durable=False)

    # translate string from NL to EN
    def translate_title(self, string_to_translate):
        translator = Translator()
        title = string_to_translate or ""  # Provide a default in case "title" is missing
        translated_title = translator.translate(title, src="nl", dest="en").text
        return translated_title

    # normalize format of the AH message
    def normalize_ah(self, message):
        title = message.get("title")
        return {
            "title": title, #self.translate_title(title),
            "brand": message.get("brand"),
            "bonus_start_date": self.normalize_date(message.get("bonusStartDate")),
            "bonus_end_date": self.normalize_date(message.get("bonusEndDate")),
            "bonus_mechanism": message.get("bonusMechanism"),
            "final_price": None if message.get("isBonus", False) else message.get("priceBeforeBonus"),
            "initial_price": message.get("priceBeforeBonus"),
            "market": "AH"
        }

    # normalize format of the Jumbo message
    def normalize_jumbo(self, message):
        promotion = message.get("promotion", {})
        prices = message.get("prices", {})
        tags = promotion.get("tags", [])
        bonus_mechanism = None

        for tag in tags:
            if "text" in tag and any(char.isdigit() for char in tag["text"]):
                bonus_mechanism = tag["text"]
                break

        return {
            "title": message.get("title"),
            "brand": None,
            "bonus_start_date": self.normalize_date(promotion.get("fromDate")),
            "bonus_end_date": self.normalize_date(promotion.get("toDate")),
            "bonus_mechanism": bonus_mechanism,
            "final_price": prices.get("promotionalPrice", {}).get("amount") if promotion else None,
            "initial_price": prices.get("price", {}).get("amount"),
            "market": "jumbo"
        }

    # Normalize date to be in the same format
    def normalize_date(self, date_input):
        if isinstance(date_input, int):  # Jumbo timestamps
            return datetime.datetime.fromtimestamp(date_input / 1000).strftime("%d/%m/%Y")
        if isinstance(date_input, str):  # AH dates
            try:
                return datetime.datetime.strptime(date_input, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                pass
        return None
    
    # process messages without consuming them
    def process_messages(self, queue_name, normalize_function):
        self.channel.queue_declare(queue=queue_name)
        messages = []

        while True:
            method_frame, properties, body = self.channel.basic_get(queue=queue_name, auto_ack=False)
            if method_frame:
                message = json.loads(body)
                normalized_message = normalize_function(message)
                messages.append(normalized_message)
            else:
                break  # Exit when no more messages are available

        return messages

    # process messages by consuming them (Jumbo doesn't work smh)
    def process_queue(self, queue_name, normalize_function):
        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                normalized_message = normalize_function(message)
                print(f"Normalized message: {normalized_message}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        print(f"Waiting for messages in {queue_name}. To exit, press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()