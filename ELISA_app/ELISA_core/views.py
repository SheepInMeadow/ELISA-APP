from django.http import HttpResponse
from django.shortcuts import  render, redirect

# Create your views here.
def placeholder(request):
    return render(request, "placeholder.html")