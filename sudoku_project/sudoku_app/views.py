from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from algorithm_app import MainProgram
from algorithm_app import SudokuAlgorithm
import numpy as np
from django.contrib import messages

# Create your views here.
def sudoku_image_input_view(request):

    if request.method == 'POST':
        if 'input_image_upload' in request.POST:
            form = Sudoku_input_imageForm(request.POST, request.FILES)
    
            if form.is_valid():
                a = form.save()
                file_path= a.sudoku_image_upload.file.name
                print(f'The file_path name is:', file_path)
                check,reg_matrix = MainProgram.mainProgram(file_path)

                if check!=False:
                    messages.info(request,"Please check the recognized result again")
                    return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})
                else:
                    reg_matrix=[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    messages.error(request, "Cannot recognize the uploaded image")
                    #return(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})
                    return render(request, 'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix,'form': form})

        elif 'Solve' in request.POST:
            # matrix = np.zeros((9,9), dtype=int)
            # matrix_input =  matrix.tolist()
            matrix_input=np.zeros((9,9), dtype=int)
            validate=["1","2","3","4","5","6","7","8","9"]
            #register a form
            form = Sudoku_input_imageForm()

            #Check validation for Input
            #Just accept number from 1 to 9
            inputfail=False
            for row in range(0,9):
                for col in range(0,9):
                    element = str(row) + str(col)
                    if request.POST.get(element) != "":
                        if (request.POST.get(element) in validate):
                            matrix_input[row][col] = request.POST.get(element)
                        else:    
                            inputfail =True

            #Input matrix not follow the rule (colom, row, box)
            matrix_valid=matrix_input.copy()
            for row in range(0,9):
                for col in range(0,9):
                    if matrix_valid[row][col] != 0:
                        number=matrix_valid[row][col]
                        matrix_valid[row][col]=0
                        check= SudokuAlgorithm.check_number_location(matrix_valid,row,col,number)            
                        if check==False:
                            inputfail =True

            print('matrix_input',matrix_input)
            if(inputfail):
                reg_matrix= [[0 for j in range(9)] for i in range(9)]

                for row in range(0,9):
                    for col in range(0,9):
                        element = str(row) + str(col)
                        if request.POST.get(element) != "":
                            reg_matrix[row][col] = request.POST.get(element)
                        else:
                            reg_matrix[row][col]=0

                messages.error(request, "The input sudoku is not correct.")
                print(f'reg_matrix is: ',reg_matrix)
                return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})

            matrix_input_copy = matrix_input.copy()
            # Slove sudoku
            print(f'matrix_input_before:',matrix_input)
            result,matrix_result=SudokuAlgorithm.soduku_algorithm(matrix_input_copy)
            print(f'matrix_input_after:',matrix_input)
            # matrix_result=matrix_result.tolist()
            print(f'matrix_result',matrix_result)

            # Check the solution for sudoku
            if(result==False):
                messages.error(request, "Can not find a solution for this Sudoku")
                reg_matrix = matrix_input.copy()
                return render(request,'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix, 'form': form})
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
            else:
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

       #return render(request, 'sudoku_app/display_sudoku_result2.html', {'reg_matrix': reg_matrix,'form': form})
        return render(request, 'sudoku_app/index.html')