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
            sloved_matrix = MainProgram.mainProgram(file_path)
            sloved_matrix1 =[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]
            return render(request,'sudoku_app/display_sudoku_result2.html', {'sloved_matrix': sloved_matrix})
            #return redirect("success", t1)          
    else:
        form = Sudoku_input_imageForm()
        return render(request, 'sudoku_app/image_input.html', {'form': form})

