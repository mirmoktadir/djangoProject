from django.shortcuts import render
from django.db.models import Q
from store.models import Product, OrderItem


# Create your views here.

def hello(request):
    # Filtering and shorting and limiting
    query_set = Product.objects.filter(Q(inventory__lt=10) & Q(
        unit_price__lt=20)).order_by('title')[5:10]

    # collecting only values and then filtering
    ordered_products = OrderItem.objects.values('product_id').distinct()  # picking ordered product id from  OrderedItem model
    query_ordered_product = Product.objects.filter(
        id__in=ordered_products)  # select all the products with those ids from Product model
    return render(request, 'hello.html', {'name': 'Moktadir', 'products': list(query_ordered_product)})

# Filtering with F object
# def me_hello(request):
#     query = Product.objects.filter(
#         inventory=F("unit_price")
#     )
#
#     return render(request, 'hello.html', {'name': 'Moktadir', 'products': list(query)})
