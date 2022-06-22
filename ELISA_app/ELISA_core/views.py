from django.shortcuts import render, redirect
from .models import Plates
import openpyxl
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimization
from matplotlib.ticker import ScalarFormatter
import statistics

def Home(request):
    return render(request, 'Home.html')


def Input_data(request):
    try:
        if request.method == 'POST':
            if request.POST.get('text_submit'):
                text_data(request)
            if request.POST.get('file_submit'):
                file_data(request)
            return render(request, 'Input_data.html', {
                'check': 'correct',
            })
        else:
            return render(request, 'Input_data.html')
    except:
        return render(request, 'Input_data.html', {
            'check': 'false',
        })


def text_data(request):
    data = request.POST.get('text_input')
    if data == '':
        return render(request, 'Input_data.html', {
            'check': 'text',
        })
    data = data.strip().split('\r\n')
    data_string = formatting_txt(data, 1)
    database(data_string)


def file_data(request):
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
            data_string = formatting_txt(data, 2)
            database(data_string)
        elif str(file).split('.')[1] == 'xlsx':
            data_string = formatting_xlsx(file)
            database(data_string)


def formatting_txt(data, counter):
    lines, data_string, formatted_data = list(), "", list()
    for i in data[:-1]:
        if counter == 1:
            lines.append(i.strip())
        elif counter == 2:
            lines.append(i.strip().decode('utf-8'))
    for j in lines:
        line = j.split('\t')
        formatted_data.append(line)
    formatted_data[1].insert(0, '#')
    for i in formatted_data:
        for j in i:
            data_string += j + "="
    return data_string


def formatting_xlsx(file_name):
    wb = openpyxl.load_workbook(file_name)
    active_sheet = wb.active
    excel_data, data_string = list(), ""
    for row in active_sheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    del excel_data[1][0]
    del excel_data[0][1:]
    excel_data[1].insert(0, '#')
    for i in excel_data:
        for j in i:
            data_string += j + "="
    return data_string


id = 1


def database(data_string):
    global id
    split = data_string.split('=')
    plates_instance = Plates.objects.create(
        id=str(id),
        name=str(split[0]),
        data=data_string
    )
    id += 1


totaal = []
check = ''


def Plate_layout(request):
    global check
    if request.method == 'POST':
        if request.POST.get('file_submit'):
            excel_data = Plate_layout_1(request)
            global totaal
            totaal = Plate_layout_2(excel_data)
            check = 'go'
            return render(request, 'Plate_layout.html', {
                'totaal': totaal,
                'check': check,
            })
        if request.POST.get('standaard_input'):
            Plate_layout_3(request)
            check = 'go'
            return render(request, 'Plate_layout.html', {
                'totaal': totaal, 'check': check, })
    else:
        return render(request, 'Plate_layout.html', {
            'totaal': totaal, 'check': check, })


def Plate_layout_1(request):
    if request.FILES.getlist("my_file") == []:
        check = 'error'
        return render(request, 'Plate_layout.html', {
            'check': check,
        })
    excel_file = request.FILES["my_file"]
    wb = openpyxl.load_workbook(excel_file)
    active_sheet = wb.active
    excel_data = list()
    for row in active_sheet.iter_rows():
        row_data = list()
        for cell in row:
            if type(cell.value) == float:
                row_data.append(str(round(cell.value)))
            else:
                row_data.append(str(cell.value))
        excel_data.append(row_data)
    return excel_data


def Plate_layout_2(excel_data):
    temp, counter = [], 0
    for i in excel_data:
        i = [e for e in i if e not in ('None')]
        if len(i) != 0:
            if counter == 1:
                i.insert(0, '#')
            temp.append(i)
            counter += 1
            if counter == 10:
                totaal.append(temp)
                counter = 0
                temp = []
    return totaal


def Plate_layout_3(request):
    values = request.POST.get('standaard')
    counter, counter2 = 0, 0
    for i in totaal:
        for j in i[2:]:
            if counter2 != 7:
                j[1] = float(values)
                j[2] = float(values)
                values = float(values) / 2
            elif counter2 == 7:
                j[1] = '#'
                j[2] = '#'
            counter2 += 1
        counter += 1
        values = request.POST.get('standaard')
        counter2 = 0


end_dilution = []

# je kan hier nog een enkele waarde aanpassen door per regel te checken
# wat voor letter is ingevoerd en dan de positie pakken
def Dilutions(request):
    global end_dilution
    if request.method == 'POST':
        if request.POST.get('dilution_submit'):
            dilution = request.POST.get('dilution')
            row_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            end_list = [["#", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "10", "11", "12"]]
            for i in range(9):
                temp = []
                temp = Dilutions_1(i, temp, row_names, dilution)
                end_list.append(temp)
            end_dilution = end_list
            return render(request, 'Dilutions.html', {
                "end_list": end_list
            })
    return render(request, 'Dilutions.html', {
        "end_list": end_dilution})


def Dilutions_1(i, temp, row_names, dilution):
    for x in range(13):
        if i == 0:
            if x == 0:
                temp.append(row_names[i])
            elif x == 1 or x == 2 or x == 3 or x == 8:
                temp.append("1")
            else:
                temp.append(dilution)
        else:
            if x == 0:
                temp.append(row_names[i])
            elif x == 1 or x == 2:
                temp.append("1")
            else:
                temp.append(dilution)
    return temp

dictionary = {}
HD = ''
delete = []
top = []
bottom = []


def Visualize_data(request):
    global dictionary
    global HD
    global delete
    global top
    global bottom
    if request.method == 'POST':
        HD = request.POST['HD']
        top = request.POST.getlist('top')
        bottom = request.POST.getlist('bottom')
        delete = request.POST.getlist('delete')
    data = Plates.objects.values()
    teller = 1
    counter = 0
    nested = []
    temp = []
    for i in data:
        lines = i['data'].split('=')[:-1]
        number1 = lines[106].replace(',', '.')
        number2 = lines[107].replace(',', '.')
        calculation = ((float(number1) + float(number2))/2)
        mean = round(calculation, 3)
        for j in lines[1:]:
            if ',' in j:
                new = float(j.replace(',', '.')) - mean
                temp.append(round(new, 3))
            else:
                temp.append(j)
            counter += 1
            if counter == 13:
                nested.append(temp)
                counter = 0
                temp = []
        dictionary[teller] = nested
        nested = []
        teller += 1
    if totaal != []:
        name_list = create_graph(dictionary)
    return render(request, 'Visualize_data.html', {
        'dictionary': dictionary,
        'name_list': name_list,
    })

def create_graph(dictionary):
    conc = totaal[0][2][1]
    x_list = [conc]
    for i in range(6):
        conc = float(conc)/2
        x_list.append(conc)
    y_list = []
    temp = []
    for values in dictionary.values():
        for elements in values[1:-1]:
            mean = (float(elements[1] + float(elements[2]))/2)
            temp.append(round(mean, 3))
        y_list.append(temp)
        temp = []
    name_list = []
    counter = 1
    for i in y_list:
        guess = [1, 1, 1, 1]
        params, params_coveriance = optimization.curve_fit(formula, x_list, i, guess)
        x_min, x_max = np.amin(x_list), np.amax(x_list)
        xs = np.linspace(x_min, x_max, 1000)
        plt.scatter(x_list, i)
        plt.plot(xs, formula(xs, *params))
        plt.xscale('log')
        plt.grid()
        ax = plt.gca()
        plt.xticks([1.0, 10, 100])
        ax.xaxis.set_major_formatter(ScalarFormatter())
        name = 'Plate_' + str(counter) + '.png'
        name_list.append(name)
        counter += 1
        plt.savefig('ELISA_core/static/images/' + str(name))
        plt.close()
    return name_list

def formula(x, A, B, C, D):
    E = 1
    return D + (A - D) / ((1.0 + ((x / C) ** (B) ** (E))))

mean = 0
std = 0
mean2 = 0
std2 = 0
check_cut_off = 'false'
cut_data = []

def Cut_off(request):
    global mean
    global std
    global mean2
    global std2
    global cut_data
    global check_cut_off
    cut_dict = {}
    if request.method == 'POST':
        input1 = request.POST.get('input1')
        input2 = request.POST.get('input2')
        outliers = (float(input1) * mean) + (float(input2) * std)
        outliers = round(outliers, 3)
        new_y_list = []
        for data in cut_data:
            if data < outliers:
                new_y_list.append(data)
        cut_dict['New_OD'] = new_y_list
        mean2 = round(statistics.mean(new_y_list), 3)
        std2 = round(statistics.stdev(new_y_list), 3)
        df = pd.DataFrame(data=cut_dict)
        ax = sns.swarmplot(data=df, y="New_OD")
        ax = sns.boxplot(data=df, y="New_OD", color='white')
        plt.savefig('ELISA_core/static/images/' + 'swarmplot2.png')
        plt.close()
        check_cut_off = 'true'
        return render(request, 'Cut_off.html', {
            'mean': mean,
            'std': std,
            'mean2': mean2,
            'std2': std2,
            'check': check_cut_off,
        })
    elif cut_data == []:
        for i in dictionary[int(HD)][1:]:
            for g in i[3:8]:
                cut_data.append(g)
        cut_data.pop(0)
        cut_dict["OD"] = cut_data
        mean = round(statistics.mean(cut_data), 3)
        std = round(statistics.stdev(cut_data), 3)
        df = pd.DataFrame(data=cut_dict)
        ax = sns.swarmplot(data=df, y="OD")
        ax = sns.boxplot(data=df, y="OD", color='white')
        plt.savefig('ELISA_core/static/images/' + 'swarmplot.png')
        plt.close()
        return render(request, 'Cut_off.html', {
            'mean': mean,
            'std': std,
            'check': check_cut_off,
        })
    return render(request, 'Cut_off.html', {
        'mean': mean,
        'std': std,
        'mean2': mean2,
        'std2': std2,
        'check': check_cut_off,
    })

def Intermediate_result(request):
    return render(request, 'Intermediate_result.html')

def End_results(request):
    return render(request, 'End_results.html')
