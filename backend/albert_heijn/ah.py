import requests
from pprint import pprint
from datetime import datetime

HEADERS = {
    'Host': 'api.ah.nl',
    'x-dynatrace': 'MT_3_4_772337796_1_fae7f753-3422-4a18-83c1-b8e8d21caace_0_1589_109',
    'x-application': 'AHWEBSHOP',
    'user-agent': 'Appie/8.8.2 Model/phone Android/7.0-API24',
    'content-type': 'application/json; charset=UTF-8',
}


class AHConnector:
    @staticmethod
    def get_anonymous_access_token():
        response = requests.post(
            'https://api.ah.nl/mobile-auth/v1/auth/token/anonymous',
            headers=HEADERS,
            json={"clientId": "appie"}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def __init__(self):
        self._access_token = self.get_anonymous_access_token()

    def search_products(self, query=None, page=0, size=750, sort='RELEVANCE'):
        response = requests.get(
            'https://api.ah.nl/mobile-services/product/search/v2',
            params={"sortOn": sort, "page": page, "size": size, "query": query},
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()


    def search_all_products(self, **kwargs):
        """
        Iterate all the products available, filtering by query or other filters. Will return generator.
        :param kwargs: See params of 'search_products' method, note that size should not be altered to optimize/limit pages
        :return: generator yielding products
        """
        response = self.search_products(page=0, **kwargs)
        yield from response['products']

        for page in range(1, response['page']['totalPages']):
            response = self.search_products(page=page, **kwargs)
            yield from response['products']

    def get_product_by_barcode(self, barcode):
        response = requests.get(
            'https://api.ah.nl/mobile-services/product/search/v1/gtin/{}'.format(barcode),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_product_details(self, product):
        """
        Get advanced details of a product
        :param product: Product ID (also called webshopId) or original object containing webshopId
        :return: dict containing product information
        """
        product_id = product if not isinstance(product, dict) else product['webshopId']
        response = requests.get(
            'https://api.ah.nl/mobile-services/product/detail/v4/fir/{}'.format(product_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_categories(self):
        response = requests.get(
            'https://api.ah.nl/mobile-services/v1/product-shelves/categories',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_sub_categories(self, category):
        category_id = category if not isinstance(category, dict) else category['id']
        response = requests.get(
            'https://api.ah.nl/mobile-services/v1/product-shelves/categories/{}/sub-categories'.format(category_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_bonus_items(self,amount):
        """
        Retrieve all items with 'isBonus' set to True from Albert Heijn's product search.
        Extract specific fields from 'item["productCard"]'.

        :param connector: Amount of items to be returned
        :return: List of dictionaries with requested item details.
        """
        bonus_items = []
        product_count = 0  # Counter to limit the total number of products processed
        #connector = AHConnector()
        max_products = amount  # Limit the search to parameter amount products

        for item in self.search_all_products():
            try:
                if item['isBonus'] == True :
                    # Dynamically build the dictionary, skipping missing fields
                    bonus_item = {key: item.get(key) for key in [
                        'webshopId',
                        'brand',
                        'title',
                        'isBonus',
                        'mainCategory',
                        'subCategory',
                        'priceBeforeBonus',
                        'salesUnitSize',
                        'unitPriceDescription',
                        'bonusStartDate',
                        'bonusEndDate',
                        'bonusMechanism',
                        'bonusSegmentDescription',
                        'bonusSegmentId',
                    ] if key in item}
                    bonus_items.append(bonus_item)
                    product_count += 1

                if product_count >= max_products:
                    break

            except Exception as exception:
                print(f"An error occurred while processing an item: {exception}")

        return bonus_items



if __name__ == '__main__':
    connector = AHConnector()
    #pprint(connector.search_products())
    # pprint(len(list(connector.search_all_products(query='smint'))))
    # pprint(connector.get_product_details(connector.get_product_by_barcode('8410031965902')))
    # pprint(connector.get_categories())
    # pprint(connector.get_sub_categories(connector.get_categories()[0]))

    # pprint(connector.search_products('Smint')['products'])

    # pprint(connector.get_product_details(177119))
    
    bonus_items = connector.get_bonus_items(10)
    
    # Print the retrieved bonus items
    for item in bonus_items:
        pprint(item)

    

