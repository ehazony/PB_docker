import shopify
import json

from django.contrib.auth.models import User
from rest_framework import serializers

from shopify_app.models import Shop
import requests


API_VERSION = '2020-07'

class ShopifyOauth:
    SCOPES = (
        "read_orders,write_orders,read_customers,write_customers,"
        "read_products,write_products,read_content,write_content,"
        "read_price_rules,write_price_rules,read_themes,write_themes"
    )
    ACCESS_MODE = "per_user"
    REDIRECT_ENDPOINT = "/account/oauth/shopify/authorize"
    ACCESS_TOKEN_HEADER = "X-Shopify-Access-Token"
    ACCESS_TOKEN_ENDPOINT = "/admin/oauth/access_token"
    AUTHORIZE_ENDPOINT = "/admin/oauth/authorize"
    SHOP_DETAILS_ENDPOINT = f"/admin/api/2021-04/shop.json"

SHOPIFY_API_VERSION = "2021-04"

# s = Shop.objects.all().first()
# session = shopify.Session(s.shopify_domain, API_VERSION, s.shopify_token)
# shopify.ShopifyResource.activate_session(session)

# c = shopify.Customer.find_first() # Order, Product, Customer


def get_shop_details(access_token,shop_name):
    res = requests.get(
        f"https://{shop_name}{ShopifyOauth.SHOP_DETAILS_ENDPOINT}",
        headers={ShopifyOauth.ACCESS_TOKEN_HEADER: access_token}
    )
    shop_data = json.loads(res.text)['shop']
    return shop_data['email'], shop_data['shop_owner']

# email, shop_owner = get_shop_details(s.shopify_token, s.shopify_domain)

class ShopifyUserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True, max_length=255)
    shop_name = serializers.CharField(required=True, max_length=255)
    token = serializers.CharField(required=True, max_length=255)

    def create(self, validated_data):
        user, _created = User.objects.get_or_create(
            email=validated_data['email'],
        )
        if _created:
            user.username = validated_data['email']
            password = User.objects.make_random_password(length=10)
            user.is_active = True
            user.set_password(password)
            user.first_name = validated_data['full_name']
            user.save()

        return user