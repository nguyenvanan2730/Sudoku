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
                return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})
                #return redirect("success", t1)

        elif 'Solve' in request.POST:
            matrix_input =  np.zeros((9,9), dtype=int)
            for row in range(0,9):
                for col in range(0,9):
                    element = str(row)+str(col)
                    if request.POST.get(element) != "":
                        matrix_input[row][col] = request.POST.get(element)
            matrix_input_copy = matrix_input.copy()

            # Slove sudoku
            print(f'matrix_input_before:',matrix_input)
            matrix_result=SudokuAlgorithm.soduku_algorithm(matrix_input_copy)
            print(f'matrix_input_after:',matrix_input)
            matrix_result=matrix_result.tolist()
            print(f'matrix_result',matrix_result)
            
            # Edit datatype before pass:
            # matrix_test= [[{'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}],
            #   [{'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}],
            #   [{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False},{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}, {'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}],
            #   [{'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}],
            #   [{'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}],
            #   [{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False},{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}, {'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}],
            #   [{'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}, {'value': 1, 'input': True}, {'value': 2, 'input': False}, {'value': 3, 'input': False}],
            #   [{'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False}, {'value': 4, 'input': True}, {'value': 5, 'input': False}, {'value': 6, 'input': False} ],
            #   [{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False},{'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}, {'value': 7, 'input': True}, {'value': 8, 'input': False}, {'value': 9, 'input': False}]
            #   ]
            matrix_result_ls=[]
            for row,tvalue in enumerate(matrix_input):
                new_row =[]
                for col,cvalue in enumerate(tvalue):
                    if cvalue == 0:
                        new_row.append({'value':matrix_result[row][col],'input':True})
                    else: new_row.append({'value':matrix_result[row][col],'input':False})
                matrix_result_ls.append(new_row)
            print(f'matrix_result_ls',matrix_result_ls)

            matrix_result = matrix_result_ls.copy()

            form = Sudoku_input_imageForm()
            return render(request,'sudoku_app/display_sloved_result.html', {'matrix_result': matrix_result, 'form': form})

        elif 'NewInput' in request.POST:
            reg_matrix =  np.zeros((9,9), dtype=int)
            form = Sudoku_input_imageForm()
            return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})

        else: print("Do not recognize the POST")
    else:
        form = Sudoku_input_imageForm()
        reg_matrix=[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        return render(request, 'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix,'form': form})