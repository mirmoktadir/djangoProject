from django.shortcuts import render
from django.db.models import Q
from store.models import Product, OrderItem


# Create your views here.

def hello(request):
    # Filtering and shorting and limiting with related field
    query_set = Product.objects.select_related('collection').prefetch_related('promotions').filter(
        Q(inventory__lt=10) & Q(
            unit_price__lt=20)).order_by('title')[5:10]

    # collecting only values and then filtering
    ordered_products = OrderItem.objects.values(
        'product_id').distinct()  # picking ordered product id from  OrderedItem model
    query_ordered_product = Product.objects.filter(
        id__in=ordered_products).order_by('title')  # select all the products with those ids from Product model

    return render(request, 'hello.html', {'name': 'Moktadir', 'products': list(query_ordered_product)})

####### Filtering with F object
# def me_hello(request):
#     query = Product.objects.filter(
#         inventory=F("unit_price")
#     )
#
#     return render(request, 'hello.html', {'name': 'Moktadir', 'products': list(query)})

####### Get Single Object with special key
# product = Product.objects.get(pk=1)
