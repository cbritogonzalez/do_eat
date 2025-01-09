import queue
import datetime
from splitter import Splitter

# First remove useless fields
# Second convert some fields to the needed column
# Add AH/Jumbo differentiating
# Translate everything in English

#  message = {
#         "title": "cucumbers",
#         "brand": "AH",
#         "bonus_start_date": "3/1/2025",
#         "bonus_end_date": None,
#         "bonus_mechanism": None,
#         "initial_price": "1.05",
#         "final_price": None,
#         "market": "jumbo" #or AH 
#     }

class Normalizer:

    # Function to normalize AH data
    def normalize_ah(self,ah_data):
        return {
            "title": ah_data.get("title"),
            "brand": ah_data.get("brand"),
            "bonus_start_date": self.normalize_date(ah_data.get("bonusStartDate")),
            "bonus_end_date": self.normalize_date(ah_data.get("bonusEndDate")),
            "bonus_mechanism": ah_data.get("bonusMechanism"),
            "final_price": None if ah_data.get("isBonus", False) else ah_data.get("priceBeforeBonus"),
            "initial_price": ah_data.get("priceBeforeBonus"),
            "market": "AH"
        }

    # Function to normalize Jumbo data
    def normalize_jumbo(self,jumbo_data):
        promotion = jumbo_data.get("promotion", {})
        prices = jumbo_data.get("prices", {})
        tags = promotion.get("tags", [])
        bonus_mechanism = None
        
        # Extract the bonus mechanism with numbers if available
        for tag in tags:
            if "text" in tag and any(char.isdigit() for char in tag["text"]):
                bonus_mechanism = tag["text"]
                break

        return {
            "title": jumbo_data.get("title"),
            "brand": None,
            "bonus_start_date": self.normalize_date(promotion.get("fromDate")),
            "bonus_end_date": self.normalize_date(promotion.get("toDate")),
            "bonus_mechanism": bonus_mechanism,
            "final_price": prices.get("promotionalPrice", {}).get("amount") if promotion else None,
            "initial_price": prices.get("price", {}).get("amount"),
            "market": "jumbo"
        }
    
    # Function to convert timestamp or string to Year-Month-Day format
    def normalize_date(self,date_input):
        if isinstance(date_input, int):  # Jumbo timestamps
            return datetime.datetime.fromtimestamp(date_input / 1000).strftime("%d/%m/%Y")
        if isinstance(date_input, str):  # AH dates
            try:
                return datetime.datetime.strptime(date_input, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                pass
        return None



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
        uniform_data = []
        normalizer = Normalizer()
        
        uniform_data = []

        # Normalize all items from the AH queue
        for ah_data in list(ah_queue.queue): 
            uniform_data.append(normalizer.normalize_ah(ah_data))

        # Normalize all items from the Jumbo queue
        # for jumbo_data in list(jumbo_queue.queue):  
        #     uniform_data.append(normalizer.normalize_jumbo(jumbo_data))

        for item in uniform_data:
            print(item)

