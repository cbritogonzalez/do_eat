import requests
from math import ceil
from supermarktconnector.errors import PaginationLimitReached
import logging
from pprint import pprint
import json
logger = logging.getLogger('supermarkt_connector')
logger.setLevel(logging.INFO)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'
}


class JumboConnector:
    jumbo_api_version = "v17"

    def search_products(self, query=None, page=0, size=30):
        """
        Fetch a single page of products.
        """
        response = requests.get(
            f'https://mobileapi.jumbo.com/{self.jumbo_api_version}/search',
            headers=HEADERS,
            params={"offset": page * size, "limit": size, "q": query},
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def search_all_products(self, **kwargs):
        """
        Fetch all available products iteratively.
        :param kwargs: See params of 'search_products' method.
        :return: generator yielding products
        """
        size = kwargs.pop('size', None) or 30
        page = 0

        while True:
            # Fetch the products for the current page
            response = self.search_products(page=page, size=size, **kwargs)

            # Extract products
            products = response.get('products', {}).get('data', [])
            if not products:  # Stop when no products are found
                break

            # Yield products one by one
            yield from products

            # Increment page for the next batch
            page += 1

            # Optional: Stop if the total count is reached
            total_products = response['products'].get('total', 0)
            if page * size >= total_products:
                break

    def get_product_by_barcode(self, barcode):
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/search',
            headers=HEADERS,
            params={"q": barcode},
        )
        if not response.ok:
            response.raise_for_status()
        products = response.json()['products']['data']
        return products[0] if products else None

    def get_product_details(self, product):
        """
        Get advanced details of a product
        :param product: Product ID or raw product object containing ID field
        :return: dict containing product information
        """
        product_id = product if not isinstance(product, dict) else product['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/products/{}'.format(product_id),
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_categories(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/categories',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['categories']['data']

    def get_sub_categories(self, category):
        category_id = category if not isinstance(category, dict) else category['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/categories',
            headers=HEADERS,
            params={"id": category_id}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['categories']['data']

    def get_all_stores(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/stores',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['stores']['data']

    def get_store(self, store):
        store_id = store if not isinstance(store, dict) else store['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/stores/{}'.format(store_id),
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['store']['data']

    def get_all_promotions(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/promotion-overview',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['tabs']

    def get_promotions_store(self, store):
        store_id = store if not isinstance(store, dict) else store['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/' + self.jumbo_api_version + '/promotion-overview',
            headers=HEADERS,
            params={"store_id": store_id}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['tabs']


if __name__ == '__main__':
    connector = JumboConnector()
    # try:
    #     results = list(connector.search_all_products())
    #     pprint(len(results))
    # except Exception as e:
    #     logger.error(f"An error occurred: {e}")
    
    # with open("savedata_jumbo_new.json", "w") as save_file:
    #     save_file.write("[\n")
    #     first = True
    #     for item in connector.search_all_products():
    #         if not first:
    #             save_file.write(",\n")
    #         json.dump(item, save_file)
    #         first = False
    #     save_file.write("\n]")
    # pprint("TEST")
    # item = list(connector.search_all_products())
    # with open("savedata_jumbo_new.json", "w") as save_file:
    #     json.dump(item, save_file, indent=2) 

    # pprint("TEST")
    # try:
    #     results = list(connector.search_all_products())
    #     # pprint(len(results))
    #     with open("savedata_jumbo_new.json", "w") as save_file:
    #         json.dump(results, save_file)
    #     print("TEST")
    # except Exception as e:
    #     logger.error(f"An error occurred: {e}")
