from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def sudoku_image_input_view(request):
    if request.method == 'POST':
        form = Sudoku_input_imageForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = Sudoku_input_imageForm()
        return render(request, 'sudoku_app/image_input.html', {'form': form})