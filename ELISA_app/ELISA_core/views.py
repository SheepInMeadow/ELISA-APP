from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Plates
import openpyxl

# Create your views here.
def Home(request):
    return render(request, 'Home.html')

def Input_data(request):
    try:
        if request.method == 'POST':
            if request.POST.get('text_submit'):
                data = request.POST.get('text_input')
                if data == '':
                    return render(request, 'Input_data.html', {
                        'check': 'text',
                    })
                data = data.strip().split('\r\n')
                formatted_data = formatting_txt(data, 1)
                database(formatted_data)
            if request.POST.get('file_submit'):
                if request.FILES.getlist('my_file') == []:
                    return render(request, 'Input_data.html', {
                        'check': 'file',
                    })
                for file in request.FILES.getlist('my_file'):
                    if str(file).split('.')[1] not in ['txt', 'xlsx']:
                        return render(request, 'Input_data.html', {
                            'check': 'extension',
                        })
                for file in request.FILES.getlist('my_file'):
                    if str(file).split('.')[1] == 'txt':
                        data = file.readlines()
                        formatted_data = formatting_txt(data, 2)
                        database(formatted_data)
                    elif str(file).split('.')[1] == 'xlsx':
                        formatted_data = formatting_xlsx(file)
                        database(formatted_data)
            return render(request, 'Input_data.html', {
                'check': 'correct',
            })
        else:
            return render(request, 'Input_data.html')
    except:
        return render(request, 'Input_data.html', {
            'check': 'false',
        })

def formatting_txt(data, counter):
    lines = list()
    for i in data[:-1]:
        if counter == 1:
            lines.append(i.strip())
        elif counter == 2:
            lines.append(i.strip().decode('utf-8'))
    formatted_data = list()
    for j in lines:
        line = j.split('\t')
        formatted_data.append(line)
    formatted_data[1].insert(0, '#')
    return formatted_data

def formatting_xlsx(file_name):
    wb = openpyxl.load_workbook(file_name)
    active_sheet = wb.active
    excel_data = list()
    for row in active_sheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    formatted_data = excel_data
    del formatted_data[1][0]
    del formatted_data[0][1:]
    formatted_data[1].insert(0, '#')
    return formatted_data

id = 1

def database(formatted_data):
    global id
    print(formatted_data[0])
    plates_instance = Plates.objects.create(
        id=id,
        name=str(formatted_data[0]),
        data=str(formatted_data[1:])
    )
    id += 1


def Plate_layout(request):
    return render(request, 'Plate_layout.html')

def Dilutions(request):
    return render(request, 'Dilutions.html')

def Visualize_data(request):
    return render(request, 'Visualize_data.html')

def Cut_off(request):
    return render(request, 'Cut_off.html')

def Intermediate_result(request):
    return render(request, 'Intermediate_result.html')

def End_results(request):
    return render(request, 'End_results.html')
