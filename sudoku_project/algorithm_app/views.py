from django.shortcuts import render
from django.http import HttpResponse
from algorithm_app import MainProgram

# Create your views here.
def success(request):
    data = request.session.get('data')
    return render(request,'display_sudoku_result.html')