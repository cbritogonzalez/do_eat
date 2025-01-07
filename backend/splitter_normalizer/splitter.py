import sys
import os
import queue
import ast
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from albert_heijn.ah import AHConnector
from pprint import pprint

class Splitter:
    # read items from json file and split the message into individual messages
    def preprocess_message(self, input_file):
        try:
            with open(input_file, 'r') as file:
                parsed_messages = json.load(file)
            if not isinstance(parsed_messages, list):
                raise ValueError("Expected JSON to be a list of messages")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading JSON: {e}")
            parsed_messages = []
        
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

    ah_file = 'savedata_AH.json'
    jumbo_file = 'savedata_jumbo.json'

    splitter = Splitter()

    parsed_messages_ah = splitter.preprocess_message(ah_file)
    parsed_messages_jumbo = splitter.preprocess_message(jumbo_file)
    
    if parsed_messages_ah and parsed_messages_jumbo:
        ah_queue = queue.Queue()
        jumbo_queue = queue.Queue()

        splitter.enque_message(parsed_messages_ah, ah_queue)
        splitter.enque_message(parsed_messages_jumbo,jumbo_queue)
        print(f"ah nr items in queue: {ah_queue.qsize()}")
        print(f"jumbo nr items in queue: {jumbo_queue.qsize()}")

        # splitter.process_queue(ah_queue)
        # splitter.process_queue(jumbo_queue)
