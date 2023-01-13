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
            matrix_input=matrix_input.tolist()

            matrix_input1 = [[5, 7, 0, 3, 6, 4, 2, 9, 8], 
                            [6, 3, 0, 7, 9, 2, 4, 1, 5], 
                            [9, 4, 2, 0, 1, 5, 3, 0, 7], 
                            [3, 2, 4, 0, 5, 8, 6, 7, 9], 
                            [8, 6, 9, 2, 0, 7, 5, 0, 1], 
                            [7, 1, 5, 6, 0, 9, 8, 3, 2], 
                            [1, 8, 6, 9, 2, 0, 7, 5, 4], 
                            [2, 5, 3, 4, 7, 0, 9, 8, 6], 
                            [4, 9, 7, 5, 8, 6, 1, 0, 3]]

            matrix_result1 = [[5, 3, 7, 1, 6, 4, 2, 9, 8], 
                            [6, 3, 4, 7, 9, 2, 4, 1, 5], 
                            [9, 4, 2, 7, 1, 5, 3, 0, 7], 
                            [3, 2, 4, 9, 5, 8, 6, 7, 9], 
                            [8, 6, 9, 2, 4, 7, 5, 0, 1], 
                            [7, 1, 5, 6, 2, 9, 8, 3, 2], 
                            [1, 8, 6, 9, 2, 8, 7, 5, 4], 
                            [2, 5, 3, 4, 7, 9, 9, 8, 6], 
                            [4, 9, 7, 5, 8, 6, 1, 2, 3]]

            print(f'Maxtrix input1', matrix_input1)
            print(f'Maxtrix result', matrix_result)
            return render(request,'sudoku_app/display_sloved_result.html', {'matrix_result1': matrix_result1, 'matrix_input1': matrix_input1})

        else: print("Do not recognize the POST")
    else:
        form = Sudoku_input_imageForm()
        return render(request, 'sudoku_app/image_input.html', {'form': form})