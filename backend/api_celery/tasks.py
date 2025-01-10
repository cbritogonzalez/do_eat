from api_celery.celery import app
from api_celery.albert_heijn import AHConnector
from api_celery.jumbo import JumboConnector

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

        folder_path = "api_celery"
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
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")

@app.task
def fetch_jumbo():
    logging.info("Starting to fetch data from Jumbo API.")
    try:
        connection_jumbo = JumboConnector()
        logger.info("Connected to Jumbo API.")
        data = list(connection_jumbo.search_all_products())

        folder_path = "api_celery"
        file_path = os.path.join(folder_path, "savedata_jumbo.json")
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder: {folder_path}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted existing file: {file_path}")
        
        with open(file_path, "w") as save_file:
            json.dump(data, save_file, indent=1)
        
        logger.info("Data successfully fetched and saved to 'savedata_jumbo.json'.")
    except Exception as e:
        logger.error(f"Error occurred while fetching data: {e}")
