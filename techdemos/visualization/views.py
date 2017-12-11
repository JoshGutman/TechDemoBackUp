from django.shortcuts import render, redirect
from django.conf import settings

from .graph import single_graph, make_content_dict
from .multiple_graph import graph_average_distances

import os
# Create your views here.

file = ""

def index(request):
    if request.method == 'POST':
        global file
        file = handle_uploaded_file(request.FILES['myfile'])
        return redirect('single.html')

    return render(request, 'visualization/home.html')


def single(request):
    global file
    names = single_graph(file)
    #location = os.getcwd()
    content_dict = make_content_dict(names, os.getcwd())
    print("\n\n\n" + str(content_dict) + "\n\n\n")
    return render(request, 'visualization/single.html', content_dict)


def handle_uploaded_file(f):
    with open('user_input.gdat', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #return 'C:\\Users\\Josh\\Desktop\\BioNetWeb\\UIFit-Tech-Demos\\techdemos\\user_input.bngl'
    return os.path.join(os.getcwd(), 'user_input.gdat')


def average(request):
    names = graph_average_distances(os.path.join(os.path.abspath(os.getcwd()), "media", "example5"), os.path.join(os.path.abspath(os.getcwd()), "media", "example5.exp")) 
    return render(request, 'visualization/average.html', {'combobox': list(names), 'images': list(names)})
