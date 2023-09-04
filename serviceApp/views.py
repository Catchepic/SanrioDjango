from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse


def globalSanrio(request):
        return render(request, 'global.html')



