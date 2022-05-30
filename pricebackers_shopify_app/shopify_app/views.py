import json

from dj_rest_auth.app_settings import create_token
from dj_rest_auth.models import get_token_model
from dj_rest_auth.registration.app_settings import RegisterSerializer
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.utils import jwt_encode
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.template import RequestContext
from django.apps import apps
import hmac, base64, hashlib, binascii, os
import shopify
from django.views.decorators.csrf import csrf_exempt

from shopify_app import models
from shopify_app.models import Shop
from shopify_app.utils import get_shop_details
from pricebackers_shopify_app import settings


def _new_session(shop_url):
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION
    return shopify.Session(shop_url, api_version)

# Ask user for their ${shop}.myshopify.com address
def login(request):
    # If the ${shop}.myshopify.com address is already provided in the URL,
    # just skip to authenticate
    if request.GET.get('shop'):
        return authenticate(request)
    return render(request, 'shopify_app/login.html', {})

def authenticate(request):
    shop_url = request.GET.get('shop', request.POST.get('shop')).strip()
    if not shop_url:
        messages.error(request, "A shop param is required")
        return redirect(reverse(login))
    scope = apps.get_app_config('shopify_app').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    request.session['shopify_oauth_state_param'] = state
    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    return redirect(permission_url)

def create_uninstall_webhook(shop, access_token):
    print('in create_uninstall_webhook')
    with shopify_session(shop, access_token):
        app_url = apps.get_app_config("shopify_app").APP_URL
        webhook = shopify.Webhook()
        webhook.topic = "app/uninstalled"
        webhook.address = "https://{host}/shopify/uninstall/".format(host=app_url)
        webhook.format = "json"
        webhook.save()

def finalize(request):
    api_secret = apps.get_app_config('shopify_app').SHOPIFY_API_SECRET
    params = request.GET.dict()

    if request.session['shopify_oauth_state_param'] != params['state']:
        messages.error(request, 'Anti-forgery state token does not match the initial request.')
        return redirect(reverse(login))
    else:
        request.session.pop('shopify_oauth_state_param', None)

    myhmac = params.pop('hmac')
    line = '&'.join([
        '%s=%s' % (key, value)
        for key, value in sorted(params.items())
    ])
    h = hmac.new(api_secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
    if hmac.compare_digest(h.hexdigest(), myhmac) == False:
        messages.error(request, "Could not verify a secure login")
        return redirect(reverse(login))

    try:
        shop_url = params['shop']
        session = _new_session(shop_url)
        access_token=session.request_token(request.GET)
        request.session['shopify'] = {
            "shop_url": shop_url,
            "access_token": access_token
        }
        email, shop_owner = get_shop_details(access_token, shop_url)
        shop_record, created = Shop.objects.get_or_create(shopify_domain=shop_url, defaults={"shopify_token": access_token, "email": email, "full_name":shop_owner})
        after_authenticate_jobs(shop_record, created)
    except Exception as e:
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse(login))
    messages.info(request, "Logged in to shopify store.")
    request.session.pop('return_to', None)
    # return redirect(request.session.get('return_to', reverse('root_path')))
    token = get_token_model().objects.get(user__email=shop_record.email)
    # return redirect('https://app.pricebackers.com?user_token={}'.format(str(token)))
    return redirect('http://localhost:3000?access_token={}'.format(str(token)))

@csrf_exempt
def uninstall(request):
    print('in uninstall')
    uninstall_data = json.loads(request.body)
    shop = uninstall_data.get("domain")
    shop = Shop.objects.filter(shopify_domain=shop).first()
    get_user_model().objects.get(email = shop.email).delete()
    shop.delete()
    return HttpResponse(status=204)

def logout(request):
    request.session.pop('shopify', None)
    messages.info(request, "Successfully logged out.")
    return redirect(reverse(login))



def shopify_session(shopify_domain, access_token):
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION
    return shopify.Session.temp(shopify_domain, api_version, access_token)


def create_user(shop: Shop):
    password = User.objects.make_random_password()
    first, last = shop.full_name.split(' ')
    user = get_user_model().objects.create_user(email = shop.email, username= shop.email, password = password, first_name = first, last_name = last)
    if getattr(settings, 'REST_USE_JWT', False):
        token = jwt_encode(user)
    else:
        token, _ = get_token_model().objects.get_or_create(user=user)




def after_authenticate_jobs(shop: models.Shop,created):
    create_uninstall_webhook(shop.shopify_domain, shop.shopify_token)
    if created:
        create_user(shop)