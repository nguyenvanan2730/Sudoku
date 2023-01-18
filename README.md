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

1.4 Create Django App
python manage.py startapp hello

1.5 To use ImageField, have to install Pillow
python -m pip install Pillow

# III. Algorithm Framework
1. Python (3.7.15)
sudo yum install python3

2. Numpy (1.21.6)
pip install numpy

3. opencv (4.7.0.68)
pip3 install opencv-python

Show opencv version
pip3 show opencv-python


4. boto3 (1.26.50)
pip install boto3

show boto3 version
pip3 show boto3

5. AWS configuration
aws configure
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region=us-east-1

II. Using Git to clone Django Project on the EC2 instance
1. Install git: (2.38.1)
// Update yum
sudo yum update

//install git on Amazon Linux 2
sudo yum install git

// check the version of git
git --version

2. Clone a private repository form GitHub on the EC2
https://rahulnpadalkar.medium.com/cloning-a-private-github-repo-to-your-ec2-instance-f40c4db6a395
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases

Using these step below to clone private repos from GitHub:
- Go to your GitHub account settings > Developer Settings > Personal access tokens.
- Click on generate token button, give the token a name and select the scope of repo and click on generate token button.
- Replace https://github.com/username/repo.git with https://username:<Token>@github.com/username/repo.git
- Run git clone command git clone https://username:<Token>@github.com/username/repo.git

3. Install the virtualenv package on your EC2 instance:
this tool that allow to create isolated Python environments.
sudo yum install python3-virtualenv

4. Navigate to the directory where want to create the virutal environment.
cd ~/sudoku

5. create a new virtual environment
virtualenv venv

6. Activeate the vitual environment:
source venv/bin/activate

7. (not done) Install the project's dependencies
pip install -r requirements.txt

8. Install Django 
python3 install Django

pip3 show Django

9. Run the Django project:
python manage.py runserver

### Bug1: Update version of sqlite to 3.31.1　(previous version: 3.7)
■Download the source code of SQLite 3.9.0 from the official website (https://www.sqlite.org/download.html) and extract the files.
wget https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz

■Extracted the downloaded file
tar -xzvf sqlite-autoconf-3310100.tar.gz

■Install the development tools and libraries required to build SQLite from source by running the following command:
sudo yum groupinstall "Development Tools"

■Navigate to the directory where you extracted the files and run the following commands to configure, build and install SQLite:
cd sqlite-autoconf-3310100
./configure
make
sudo make install

■Once the installation is complete, you can verify the installation by running the following command:
sqlite3 --version

■Update the library path by adding this line to your .bashrc file
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib


### Install again these library on the venv
1. Numpy (1.21.6)
pip install numpy

2. opencv (4.6.0.66) // using other version will make error
pip3 install opencv-python==4.6.0.66

Show opencv version
pip3 show opencv-python

3. boto3 (1.26.50)
pip install boto3

show boto3 version
pip3 show boto3

4. Install Pillow for using ImageField
python -m pip install Pillow

### Install Nginx(nginx/1.22.0) :
https://qiita.com/tamorieeeen/items/07743216a3662cfca890
1. install nginx by Amazon Linux Extras
sudo amazon-linux-extras install nginx1

2. Start the nginx
sudo systemctl start nginx

3. Confirm status of nginx
sudo systemctl status nginx

##### If successfully start nginx, will display below message
Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
Active: active (running) since Mon 2020-03-30 15:38:21 JST; 7s ago

4. Enable nginx
sudo systemctl enable nginx

5. Check Nginx is enabled
systemctl is-enabled nginx


### Run below command to start server
python3 manage.py runserver 0.0.0.0:8000

Have to add public IP to ALLOWED_HOSTS in settings.py
ALLOWED_HOSTS = ['54.65.38.242']


### Login Server
ssh -i pro-sudoku.pem ec2-user@54.65.38.242