from django.shortcuts import render
from store.models import Collection, Product


# Create your views here.

def hello(request):

    return render(request, 'hello.html', {'name': 'Moktadir'})
