from django.http import HttpResponse
from django.shortcuts import  render, redirect

# Create your views here.
def Home(request):
    return render(request, 'Home.html')

def Input_data(request):
    return render(request, 'Input_data.html')

def Plate_layout(request):
    return render(request, 'Plate_layout')

def Dilutions(request):
    return render(request, 'Dilutions')

def Visualize_data(request):
    return render(request, 'Visualize_data')

def Cut_off(request):
    return render(request, 'Cut_off')

def Intermediate_result(request):
    return render(request, 'Intermediate_result')

def End_results(request):
    return render(request, 'End_results')

