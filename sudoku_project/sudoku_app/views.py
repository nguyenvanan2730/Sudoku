from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from algorithm_app import MainProgram

# Create your views here.
def sudoku_image_input_view(request):
    if request.method == 'POST':
        form = Sudoku_input_imageForm(request.POST, request.FILES)
 
        if form.is_valid():
            a = form.save()
            file_path= a.sudoku_image_upload.file.name
            print(f'The file_path name is:', file_path)
            MainProgram.mainProgram(file_path)
            return redirect("success")          
    else:
        form = Sudoku_input_imageForm()
        return render(request, 'sudoku_app/image_input.html', {'form': form})