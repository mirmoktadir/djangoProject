from django.shortcuts import render
from django.db.models.aggregates import Count
from store.models import Product


# Create your views here.

def hello(request):
    # we can have any summary like total count, max item, max price we use aggregate.
    # we can filter them too
    result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'))
    return render(request, 'hello.html', {'name': 'Moktadir', 'result': result})
