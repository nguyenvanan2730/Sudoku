# Sudoku
## I. Processing the Image
1.1 Get the image by computer's camera

1.2 Preprocessing the image

1.3 Find the the sudoku's frame

1.4 Crop and transform the image

1.5 Create image's matrix 9x9

1.6 Extract the number from the cell

## II. Predict the number
1.1 Load the model

1.2 Load the image data

1.3 Reshape the image data

1.4 Predict the number for each image

1.5 Print the data

## III. Solve Sudoku (Backtracking)
1.1 Using the Backtracking algorithms to slove the soduku

1.2 Print the result to the screen

This was add to check the push command.


# GIT command
1.1 Create a branch
git branch feature/annv/add-django

1.2 Switch to a branch
git switch feature/annv/add-django

1.3 Add file before commit
git add file_name
git add -A (add all)

1.4 Commit
git commit -m "message"

1.5 Push commit to remote respo
git push origin branch_name


# Django create project
I. Setup Virtual Enviroment
1.1 Create a project environment
python3 -m venv .venv
source .venv/bin/activate

1.2 Update pip in the virtual environment
python -m pip install --upgrade pip

1.3 Install Django in the virtual environment
python -m pip install django

II. Create the Django Project
1.1 Create the project
django-admin startproject project_name

1.2 Create an empty development databas
python manage.py migrate

1.3 Run Server
python manage.py runserver