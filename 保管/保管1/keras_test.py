
import keras
from keras.models import load_model
model_mnist = load_model('C://Users/nguye/Desktop/VanAn/SUDOKU/model/mnist_handwritting.h5')
print("The version of keras: ", keras.__version__)
print("The number: ", 1+1)
