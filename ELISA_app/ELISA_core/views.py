from django.http import HttpResponse
from django.shortcuts import  render, redirect

# Create your views here.
def Home(request):
    return render(request, 'Home.html')

def Input_data(request):
    if request.method == 'POST':
        data = request.FILES['my_file'].readlines()
        lines = list()
        for i in data[1:-1]:
            lines.append(i.strip().decode('utf-8'))
        formatted_data = list()
        for j in lines:
            line = j.split('\t')
            formatted_data.append(line)
        formatted_data[0].insert(0, '#')
        print(formatted_data)
        return render(request, 'Input_data.html')
    else:
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
