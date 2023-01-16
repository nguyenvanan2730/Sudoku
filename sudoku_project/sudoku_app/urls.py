from django.urls import path
from sudoku_app import views

urlpatterns = [
path('',views.sudoku_image_input_view, name="sudoku_image_input_view"),
]