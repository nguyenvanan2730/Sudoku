#ブランクcellを探す
def find_empty_location(arr,l):
    for row in range(0,9):
        for col in range(0,9):
            if arr[row][col]==0:
                l[0]=row
                l[1]=col
                return True
    return False

#この数値をここに入れるかどうか確認
def check_number_location(arr,row,col,num):
    #この数値はほかの行に使ったかどうか確認
    for i in range(0,9):
        if arr[i][col]== num: return False

    #この数値はほかの列に使ったかどうか確認
    for j in range(0,9):
        if arr[row][j]== num: return False
    
    #この数値はmatrix(3x3)に使ったかどうか確認
    matrix_row=(row//3)*3
    matrix_colum=(col//3)*3
    for m in range(matrix_row,matrix_row+3):
        for n in range (matrix_colum,matrix_colum+3):
            if arr[m][n]==num: return False
    return True

#Soduku Algorithm
def solve_sudoku(arr):
    #行列記録
    l= [0,0]
    # ブランクcellを探す、全部が入れられたら　終わりします。
    if(not find_empty_location(arr,l)):
        return True
    
    #データをcellに入れ
    row=l[0]
    col=l[1]

    #1から9まで順番にcellに入れ
    for num in range(1,10):
        #入れた値は正常するかどうか確認
        if(check_number_location(arr,row,col,num)):
            arr[row][col]=num

            #成功したら戻る, 失敗したら、0にする
            if(solve_sudoku(arr)):
                return True
            else:
                arr[row][col]=0
    return False

#Sudoku matrix 入力

# grid3 =[[7, 2, 3, 0, 0, 0, 1, 5, 9],
#         [6, 0, 0, 3, 0, 2, 0, 0, 8],
#         [8, 0, 0, 0, 1, 0, 0, 0, 2],
#         [0, 7, 0, 6, 5, 4, 0, 2, 0],
#         [0, 0, 4, 2, 0, 7, 3, 0, 0],
#         [0, 5, 0, 9, 3, 1, 0, 4, 0],
#         [5, 0, 0, 0, 7, 0, 0, 0, 3],
#         [4, 0, 0, 1, 0, 3, 0, 0, 6],
#         [9, 3, 2, 0, 0, 0, 7, 1, 4]]
     
# if(solve_sudoku(grid3)):
#     for i in range(0,9):
#         print(grid3[i][:])
# else:
#     print ("No solution")


def soduku_algorithm(number_matrix):
    if(solve_sudoku(number_matrix)):
        for i in range(0,9):
            print(number_matrix[i][:])
    else:
        print ("There are no solution for this Soduko")
        return 0,False
    return number_matrix,True