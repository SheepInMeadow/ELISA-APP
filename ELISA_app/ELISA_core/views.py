from django.http import HttpResponse
from django.shortcuts import  render, redirect

# Create your views here.
def hi_mom(request):
    return HttpResponse("<h1>hi mom</h1>")