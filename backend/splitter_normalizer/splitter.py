import sys
import os
import queue
import ast
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from albert_heijn.ah import AHConnector
from pprint import pprint

class Splitter:
    # split the message into individual messages
    def preprocess_message(self, input_message):
        messages = input_message.strip().split("}\n")
        parsed_messages = []

        for message in messages:
            message = message.strip()
            # fix error when it still checks after last element
            if not message.endswith("}"):
                message += "}"
            try:
                parsed_messages.append(ast.literal_eval(message))
            except (SyntaxError, ValueError) as e:
                print(f"error parsing message: {message}\n {e}")

        # euro symbol error, fix later
        return parsed_messages
    
    # add the message into a queue
    def enque_message(self,parsed_messages, output_queue):
        for message in parsed_messages:
            output_queue.put(message)
    
    # logs entries into the queue || Is WireTap something like this?
    def process_queue(self,input_queue):
        while not input_queue.empty():
            item = input_queue.get()
            print(f"Processing item {item}")
            input_queue.task_done()



if __name__ == "__main__":

    with open('ah_example.txt', 'r') as file:
        input_message = file.read()

    splitter = Splitter()
    preprocess_message = splitter.preprocess_message(input_message)
    output_queue = queue.Queue()
    enq_message = splitter.enque_message(preprocess_message, output_queue)

    splitter.process_queue(output_queue)