from django.shortcuts import render
from store.models import Collection, Product


# Create your views here.

def hello(request):
    # 1.>adding objects
    # collection = Collection()
    # collection.title="Hello"
    # collection.featured_product=Product(pk=1)
    # collection.save()
    # 2.>updating object
    # Collection.objects.filter(pk=11).update(featured_product=None)
    # 3.> deleting objects
    # single object delete >
    collection = Collection(pk=11)
    collection.delete()
    # multiple object delete >
    # Collection.objects.filter(id__gt=5).delete()
    return render(request, 'hello.html', {'name': 'Moktadir'})
