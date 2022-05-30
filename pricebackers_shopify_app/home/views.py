from django.shortcuts import render
import shopify
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from shopify_app.decorators import shop_login_required


# @csrf_exempt
@shop_login_required
def index(request):
    products = shopify.Product.find(limit=3)
    orders = shopify.Order.find(limit=3, order="created_at DESC")
    return render(request, 'home/index.html', {'products': products, 'orders': orders})
