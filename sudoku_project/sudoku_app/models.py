from django.db import models
# Create your models here.
import os
import random
import string
import datetime
def content_file_name(instance, filename):
    s= random.choices(string.ascii_lowercase,k=5)
    listToStr = ' '.join(s)
    print(f'This is random string',listToStr)

    t = datetime.datetime.now()

    ext = filename.split('.')[-1]
    filename = str(t.year)+'/'+str(t.month) + '/' + str(t.day) + '/' + str(t.year)+ str(t.month)+ str(t.day)+listToStr + "." + ext
    return os.path.join('sudoku_input/',filename)

class sudoku_model(models.Model):
    #sudoku_image_upload=models.ImageField(upload_to='sudoku_input/')
    sudoku_image_upload=models.ImageField(upload_to=content_file_name)