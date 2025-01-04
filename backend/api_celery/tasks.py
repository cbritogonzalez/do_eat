from app import celery_app
import logging
from jumbo import JumboConnector
from albert_heijn import AHConnector
from pprint import pprint
import json


@celery_app.task(name='tasks.fetch_albert_heijn_data')
def fetch_albert_heijn_data():
    logging.info('Fetching data from Albert Heijn')
    connector_AH = AHConnector()
    try:
        products_ah = list(connector_AH.get_bonus_items(400))
        logging.info(f"Fetched {len(products_ah)} products from Albert Heijn.")

        # products_json_ah = json.dumps(products_ah, indent=2, ensure_ascii=False)
        products_json_ah = json.dumps(products_ah, default=str)
        return products_json_ah
    except Exception as e:
        logging.error(f"Error while fetching data: {e}")
        raise


@celery_app.task(name='tasks.fetch_jumbo_data')
def fetch_jumbo_data():
    logging.info('Fetching dara from Jumbo')
    connector_Jumbo = JumboConnector()
    try:
        products_jumbo = list(connector_Jumbo.search_all_products(query=''))
        logging.info(f"Fetched {len(products_jumbo)} products from Jumbo.")
        products_json_jumbo = json.dumps(products_jumbo, default=str)
        return products_json_jumbo
    except Exception as e:
        logging.error(f"Error : {e}")
        raise

    