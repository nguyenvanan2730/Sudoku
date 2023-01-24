from django.urls import path
from sudoku_app import views

urlpatterns = [
path('introduction',views.sudoku_introduction, name="sudoku_introduction"),
path('home',views.sudoku_image_input_view, name="home"),
path('imageuploadrule',views.sudoku_imageuploadrule, name="imageuploadrule"),
path('systemarchitect',views.sudoku_systemarchitect, name="sudoku_systemarchitect"),
path('resultandimprovement',views.sudoku_resultandimprovement, name="resultandimprovement"),
path('',views.sudoku_image_input_view, name="sudoku_image_input_view"),
]