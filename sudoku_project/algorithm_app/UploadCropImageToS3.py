import boto3
import os
import environ

# Initialise environment variables
env = environ.Env()

# #Set the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MEDIA_ROOT = env('MEDIA_ROOT')

def upload_file(file_name):
    # Upload image to S3
    #path='/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/crop-input-image/'
    path = env('IMAGE_UPLOAD_PATH')
    # path = os.getenv('IMAGE_UPLOAD_PATH')
    # print(f'getenv1',os.getenv('IMAGE_UPLOAD_PATH'))
    # print(f'list-all',os.environ)
    #print(f'getenv2',os.getenv['IMAGE_UPLOAD_PATH'])
    #print(f'getenv1',os.getenv('IMAGE_UPLOAD_PATH'))
    local_file_url=path+file_name+'.png'
    s3 = boto3.resource('s3')

    #Count the number of object in 'sudoku-user-upload-image-3033' budget
    my_bucket = s3.Bucket('sudoku-user-upload-image-3033')
    count_obj=int(0)
    for my_bucket_object in my_bucket.objects.all():
        count_obj+=1   
    print ("Numbers of the object is: ",count_obj)

    #File name of the image in budget
    obj_name='user-input-image-'+str(count_obj+1)+'.png'
    try:
        s3.meta.client.upload_file(local_file_url, 'sudoku-user-upload-image-3033', obj_name)
        print("Successfully upload the image to S3:",file_name)
        return obj_name
    except:
        print("Can not upload the image to S3")
        return 0