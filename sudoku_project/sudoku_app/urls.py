from django.urls import path
from sudoku_app import views

urlpatterns = [
path('introduction',views.sudoku_introduction, name="sudoku_introduction"),
path('home',views.sudoku_image_input_view, name="home"),
path('ec2deployguide',views.sudoku_EC2deployguide, name="EC2deployguide"),
path('systemarchitect',views.sudoku_systemarchitect, name="sudoku_systemarchitect"),
path('resultandimprovement',views.sudoku_resultandimprovement, name="resultandimprovement"),
path('',views.sudoku_image_input_view, name="sudoku_image_input_view"),
]