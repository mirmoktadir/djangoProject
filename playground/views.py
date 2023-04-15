from django.shortcuts import render
from django.db.models import Value, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from store.models import Product, Customer


# Create your views here.

def hello(request):
    # we can add new attribute to query objects with annotations
    custom_id = ExpressionWrapper(
        F("id") * 0.8, output_field=DecimalField())
    query_set = Customer.objects.annotate(is_new=Value(True), new_id=F('id') + 1,
                                          full_name=Concat("first_name", Value(" "), "last_name"),
                                          custom_id=custom_id
                                          )
    return render(request, 'hello.html', {'name': 'Moktadir', 'result': list(query_set)})
