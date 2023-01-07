from django import forms
from .models import *

class Sudoku_input_imageForm(forms.ModelForm):
    class Meta:
        model = sudoku_model
        fields = ['sudoku_image_upload']