import shopify

from dashboard.store_api import Store
from pathlib import Path


class ShopifyStore(Store):
    API_VERSION = '2020-07'

    def __init__(self, shop):
        self.shop = shop
        # self.session = shopify.Session(shop.shopify_domain, self.API_VERSION, self.shop.shopify_token)
        # shopify.ShopifyResource.activate_session(session)

        # c = shopify.Customer.find_first() # Order, Product, Customer

    def get_customers(self):
        customers = []
        with shopify.Session.temp(self.shop.shopify_domain, self.API_VERSION, self.shop.shopify_token):
            page = shopify.Customer.find()
            customers.extend(page)
            while page.has_next_page():
                page = page.next_page()
                customers.append(page)
        return customers

    def get_products(self):
        products = []
        with shopify.Session.temp(self.shop.shopify_domain, self.API_VERSION, self.shop.shopify_token):
            page = shopify.Product.find()
            products.extend(page)
            while page.has_next_page():
                page = page.next_page()
                products.append(page)
        return products

    def get_orders(self):
        ordres = []
        with shopify.Session.temp(self.shop.shopify_domain, self.API_VERSION, self.shop.shopify_token):
            page = shopify.Order.find()
            ordres.extend(page)
            while page.has_next_page():
                page = page.next_page()
                ordres.append(page)
        return ordres

    # def graphQL(self, query):
    #     document = Path("shopify_app/queries/graphql").read_text()
    #     with shopify.Session.temp(self.shop.shopify_domain, self.API_VERSION, self.shop.shopify_token):
    #         result = shopify.GraphQL().execute(
    #             query=document,
    #             variables={"order_id": "gid://shopify/Order/12345"},
    #             operation_name="GetOneOrder",
    #         )
    #     return result
