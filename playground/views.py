from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem


# Create your views here.

def hello(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, 'hello.html', {'name': 'Moktadir', 'result': list(queryset)})
