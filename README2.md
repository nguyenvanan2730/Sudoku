# 20230119 Deploy DJANGO PROJECT TO EC2 Ubuntu
### I. Check version Python, Pip, git
python3 --version
--> 3.10.6

pip3 --version
--> not found

git --version
--> 2.34.1
------------------------
1.Install pip3
===> Install pip3
sudo apt install python3-pip

pip3 --version
--> pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)

2. Update git (no change)
sudo apt install git

git --version
--> 2.34.1

### II. Clone project from GitHUb
1. using git clone and token for clone the project
git clone https://nguyenvanan2730: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@github.com/nguyenvanan2730/sudoku.git

### III. Create a new Virual Environment
1, Get inside sudoku, create virual environment
sudo apt install python3-virtualenv

2. Activate environment
source .venv/bin/activate


### IV. Requierment tool, framework install
1. Django
pip3 install django

pip3 show Django
-->4.1.5

2. Numpy (1.21.6)
pip3 install numpy

pip3 show numpy
-->1.24.1

3. opencv
pip3 install opencv-python

pip3 show opencv-python
-->4.7.0.68

4. boto3 (1.26.50)
pip3 install boto3

pip3 show boto3 (in Mac is 1.26.45)
--> 1.26.52

5. Install Pillow for using ImageField
python3 -m pip install Pillow

6. Install django-environ
python3 -m pip install django-environ

### V. Create and update .env .gitignore
nano .env
---> Past enviroment variable in to the text
nano .gitignore
---> add .env in to the text

### VI. aws install and configure
1. install aws
sudo apt install awscli

2. aws configure

### VII. After run, there is a error message like below:
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
--> Install the missed library and everything is fixed. (ChatGPT)

sudo apt-get install libgl1-mesa-glx

### Result: Check the local server in here:


### VIII. Deploy on Production using uWSGI and Ngnix
https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

Please follow above guide
1. install uwsgi
pip3 install uwsgi

2. install nginx
sudo apt-get install nginx

2022/01/20: Below error message:
2023/01/19 23:14:24 [crit] 1939#1939: *51 connect() to unix:///home/ubuntu/sudoku/sudoku_project/mysite.sock failed (13: Permission denied) while connecting to upstream, client: 114.186.10.198, server: 3.114.77.145, request: "GET /favi>

-->sudo sed -i 's/user www-data;/user ubuntu;/' /etc/nginx/nginx.conf

Follow below thread:
sudo sed -i 's/user www-data;/user ubuntu;/' /etc/nginx/nginx.conf

Bug: Not application found
uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=664
-->uwsgi --socket mysite.sock --module sudoku_project.wsgi --chmod-socket=664


##-----------------------------------------------##
# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/ubuntu/sudoku/sudoku_project
# Django's wsgi file
module          = sudoku_project.wsgi
# the virtualenv (full path)
home            = /home/ubuntu/sudoku/.venv
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = /home/ubuntu/sudoku/sudoku_project/mysite.sock
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true


##-------------------------------------------##




