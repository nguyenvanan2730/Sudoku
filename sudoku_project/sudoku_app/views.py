from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from algorithm_app import MainProgram
from algorithm_app import SudokuAlgorithm
import numpy as np

# Create your views here.
def sudoku_image_input_view(request):
    if request.method == 'POST':
        if 'input_image_upload' in request.POST:
            form = Sudoku_input_imageForm(request.POST, request.FILES)
    
            if form.is_valid():
                a = form.save()
                file_path= a.sudoku_image_upload.file.name
                print(f'The file_path name is:', file_path)
                reg_matrix = MainProgram.mainProgram(file_path)
                return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix})
                #return redirect("success", t1)

        elif 'Slove' in request.POST:
            matrix_input =  np.zeros((9,9), dtype=int)
            for row in range(0,9):
                for col in range(0,9):
                    element = str(row)+str(col)
                    if request.POST.get(element) != "":
                        matrix_input[row][col] = request.POST.get(element)
            
            matrix_result=SudokuAlgorithm.soduku_algorithm(matrix_input)
            matrix_result=matrix_result.tolist()
            print(f'matrix_result',matrix_result)

            return render(request,'sudoku_app/display_sloved_result.html', {'matrix_result': matrix_result})

        else: print("Do not recognize the POST")
    else:
        form = Sudoku_input_imageForm()
        return render(request, 'sudoku_app/image_input.html', {'form': form})