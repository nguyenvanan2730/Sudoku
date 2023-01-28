# Recognize the image have been saved in S3.
import boto3


def recognize_number(s3path):
    budget = "sudoku-user-upload-image-3033"
    name = s3path
    client = boto3.client('textract',region_name='ap-southeast-1')
    response = client.detect_document_text(
        Document ={
            #'Bytes' : b'bytes',
            'S3Object': {
                'Bucket': budget,
                'Name' : name,
            }
        }
    )
    print(f"The value of respone is: {response}")

    blocks=response["Blocks"]
    #print(f"The length of the blocks is: {len(blocks)}")
    #print(blocks)

    # Create a empty matrix
    import numpy
    matrix = numpy.zeros(shape=(9,9),dtype=int)
    print(f"The matrix of sudoku is: {matrix}")

    #Create a matrix for sudoku image
    left_list =[]
    top_list=[]
    recognize_list=[]
    count=int(0)
    for each in blocks: # Each element in these list (total 67 elements)
        for key in each:# In each element is a dict, there is 33 element is "WORD"
            if each[key]=="WORD" and each["Text"].isnumeric()==True:
                Geometry_value=each["Geometry"]
                BoundingBox_value=Geometry_value["BoundingBox"]
                left_value = BoundingBox_value["Left"] # Get the list of left
                top_value = BoundingBox_value["Top"] # Get the list of the top
                left_list.append(left_value)
                top_list.append(top_value)
                
                #Save text in a list
                recognize_value=each["Text"]
                recognize_list.append(recognize_value)
                
                # Coutn the word block (for test)
                count=count+1
    print(f"Total of the number is:{count}")
    #print(matrix)
    print("The left_list is: ",left_list)
    print("The top_list is: ",top_list)
    print("The recognize_list is", recognize_list)

    # Array the number to the appriate cell by depend on left, top value.
    import numpy
    an_array_left = numpy.array(left_list)
    left=((an_array_left*10/1.111)+1).astype(int) # Convert float to int
    print(f"Left position is:  ",left)

    an_array_top = numpy.array(top_list)
    top=((an_array_top*10/1.111)+1).astype(int) # Convert float to int
    print(f"Top position is:   ", top)

    # Convert left and top to list
    left=list(left)
    top=list(top)

    #Fix1: recognize_list in case there are more number in a element
    for index,item in enumerate(recognize_list):
        if len(item)>1:
            temp_lst=list(item)
            recognize_list[index:index+1]=temp_lst

        # Add element to left and top
            left_a= list(range(left[index]+1,left[index]+len(item),1))
            top_a= list([top[index]]*(len(item)-1))
            
            left[index+1:index+1]=left_a
            top[index+1:index+1]=top_a
    print(f"The recoginze_list after fix: {recognize_list}")

    #Fix2: receive wrong the left possition (sudoku-image-example-6.png)
    for index,item in enumerate(left):
        if index<(len(left)-1):
            if (left[index]==left[index+1]):
                if(top[index]==top[index+1]):
                    left[index+1]=left[index+1]+1

    #Export the result of matrix
    for x in range(0,len(recognize_list)):
        matrix[top[x]-1][left[x]-1]=recognize_list[x]
    print(f"The matrix is: \n{matrix}") 

    return matrix


########################################################################################
#                                                                                       #
#                               TESTCASE                                                #
#                                                                                       #
########################################################################################

#sudoku-image-example-1.png --->Test fail-->Test Ok
""" [[ 53   0   0   0   7   0   0   0   0]
 [  6   0   0 195   0   0   0   0   0]
 [  0  98   0   0   0   0   0   6   0]
 [  8   0   0   0   6   0   0   0   3]
 [  4   0   0   8   0   3   0   0   1]
 [  7   0   0   0   2   0   0   0   6]
 [  0   6   0   0   0   0  28   0   0]
 [  0   0   0 419   0   0   0   0   5]
 [  0   0   0   0   8   0   0  79   0]] """

#sudoku-image-example-2.png --->Test ok

#sudoku-image-example-3.png --->未実行

#sudoku-image-example-4.png --->Test Ok

#sudoku-image-example-5.png --->Test fail ---> Test OK (The same image as sudoku-image-example-1.png)
""" [[ 53   0   0   0   7   0   0   0   0]
 [  6   0   0 195   0   0   0   0   0]
 [  0  98   0   0   0   0   0   6   0]
 [  8   0   0   0   6   0   0   0   3]
 [  4   0   0   8   0   3   0   0   1]
 [  7   0   0   0   2   0   0   0   6]
 [  0   6   0   0   0   0  28   0   0]
 [  0   0   0 419   0   0   0   0   5]
 [  0   0   0   0   8   0   0  79   0]] """

 #sudoku-image-example-6.png --->Test fail　ーーー＞Test OK (#Fix2: receive wrong the left possition (sudoku-image-example-6.png)）
""" 8,6 was be attached together (caculated position wrong)
[[0 5 0 8 4 0 0 0 3]
 [8 0 0 6 1 9 0 0 2]
 [0 0 9 2 5 0 1 4 0]
 [3 7 0 0 2 1 4 5 6]
 [0 1 2 0 6 4 3 0 7]
 [6 0 0 0 3 0 2 1 0]
 [5 9 3 4 0 0 7 2 0]
 [1 0 0 3 0 5 0 6 4]
 [4 6 0 1 7 2 9 3 5]] """

#sudoku-image-example-7.png --->Test Ok
#sudoku-image-example-8.png --->Test Ok
#sudoku-image-example-9.png --->Test fail --->Test Ok
""" [[    0     0     0     0     0     0     0     0     0]
 [    0    12     0     0 34567     0     0     0     0]
 [    0   345     0     0     0  6182     0     0     0]
 [    0     0     1     0   582     0     0     0     6]
 [    0     0    86     0     0     0     0     0     1]
 [    0     2     0     0     0    75     0     0     0]
 [    0     0    37     0     0     5     0    28     0]
 [    0     8     0     0     6     0     7     0     0]
 [    2     0     7     0 83615     0     0     0     0]] """

#sudoku-image-example-10.png --->Test Ok
#sudoku-image-example-11.png --->Test Ok

#sudoku-image-example-12.png ---> 未実行

#sudoku-image-example-13.png ---> test fail
""" Possition of number 3 was wrong :[6][6]
[[8 0 0 0 0 0 0 0 0]
 [0 0 3 6 0 0 0 0 0]
 [0 7 0 0 9 0 2 0 0]
 [0 5 0 0 0 7 0 0 0]
 [0 0 0 0 4 5 7 0 0]
 [0 0 0 1 0 0 3 0 0]
 [0 0 1 0 0 0 6 8 0]
 [0 0 8 5 0 0 0 1 0]
 [0 9 0 0 0 0 4 0 0]] """


#sudoku-image-example-14.png ---> test ok

#sudoku-image-example-15.png ---> test fail (true on console)
""" 
Font word wrong, can not regonize
[[4 0 6 3 0 0 2 0 0]
 [5 0 3 7 0 4 0 0 0]
 [0 0 0 9 0 0 8 4 3]
 [2 3 0 0 0 0 9 0 0]
 [0 5 0 6 4 7 5 7 1]
 [9 0 1 4 0 8 3 0 0]
 [0 6 4 0 0 0 0 7 0]
 [8 0 5 0 0 3 9 2 0]
 [0 0 0 0 0 0 0 0 0]]
 """

#sudoku-image-example-16.png ---> 未実行

#sudoku-image-example-17.png ---> 未実行

#sudoku-image-example-18.png ---> test ok

#sudoku-image-example-19.png ---> test ok

#sudoku-image-example-20.png ---> test ok

# Cân nhắc phương án ko sử dụng openCV mà chỉ sử dụng toạ độ nhận được tử textract để dựng lại sudoku