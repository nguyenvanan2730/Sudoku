from django.db import models

# Create your models here.
class sudoku_model(models.Model):
    sudoku_image_upload=models.ImageField(upload_to='sudoku_input/')
    