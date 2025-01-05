from supermarktconnector.ah import AHConnector
from jumbo.jumbo import JumboConnector
from pprint import pprint

connector = AHConnector()
connectorJumbo = JumboConnector()

#print(connector.get_sub_categories(connector.get_categories()[0]))
#pprint(connectorJumbo.get_sub_categories(connectorJumbo.get_categories()[0]))

pprint(connectorJumbo.search_products(size=30))

# # print(list(connector.search_all_products(query='hak')))
# item = connector.get_product_details(195105)

# #print(item['productCard']['isBonus'])
# print(item.get('productCard'))

