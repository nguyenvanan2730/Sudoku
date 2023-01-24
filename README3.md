# I.20230121 Deploy DJANGO PROJECT TO EC2 Ubuntu
Connectserver: ssh -i /Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku-info/pro-sudoku/pro-sudoku.pem ubuntu@ec2-52-68-221-167.ap-northeast-1.compute.amazonaws.com

### 1. Update apt
sudo apt update

### 2. Install pip
===> Install pip3
sudo apt install python3-pip

# II.Create a new Virual Environment
### 1. Get inside sudoku, install virual environment
sudo apt install python3-virtualenv

### 2. Create virtual environment
virtualenv venv

### 3. Activate environment
source .venv/bin/activate

--> Make sure the virtual environment is activated
# III.Clone project from GitHUb
### 1. Update git (no change)
sudo apt install git

git --version
--> 2.34.1
### 2. using git clone and token for clone the project
git clone https://nguyenvanan2730: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@github.com/nguyenvanan2730/sudoku.git

# IV.Install Python library
In virtual enviroment, Python library packages is location at:
venv/lib/python3.10/site-packages 

In Ubution enviroment, Python library packages is location at:
/usr/local/lib/python3.10/dist-packages

### 1. Django
pip3 install django==4.1.4

pip3 show Django
-->4.1.4

### 2. Numpy
pip3 install numpy==1.23.5

pip3 show numpy
-->=1.23.5

### 3. opencv
pip3 install opencv-python==4.6.0.66

pip3 show opencv-python
-->4.6.0.66

### 4. boto3
pip3 install boto3==1.26.30

pip3 show boto3 (in Mac is 1.26.45)
--> 1.26.30

### 5. Install Pillow for using ImageField
python3 -m pip install Pillow


### 6. Install django-environ
python3 -m pip install django-environ

# V.Setting Variable Enviroment
### 1. Create a .env file in the /home/ubuntu/venv/sudoku/sudoku_project
sudo nano .env

Past the below variable enviroment:
-----------------------------------------------------------------
MEDIA_ROOT=/home/ubuntu/venv/sudoku/sudoku_project/sudoku_app/media
MEDIA_URL=/image/
IMAGE_UPLOAD_PATH=/home/ubuntu/venv/sudoku/Images/crop-input-image
IMAGE_TRANSFORM_CROP=/home/ubuntu/venv/sudoku/Images/crop-input-image
STATIC_ROOT=/home/ubuntu/venv/sudoku/sudoku_project/static
DEBUG=FALSE
ALLOWED_HOSTS=52.68.221.167
-----------------------------------------------------------------

### 2. Create a .gitignore file in the /home/ubuntu/venv/sudoku/sudoku_project
sudo nano .gitignore

Add .env in the file

# VI. aws install and configure
### 1. install aws
sudo apt install awscli

### 2. aws configure
AKIAURRDTZ7AO6D6WO4G,oXm9zUl50/93caEwAs/vkmxAC083H3vOUfCN9N2g
AWS Access Key ID = AKIAURRDTZ7AO6D6WO4G
AWS Secret Access Key = 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
Default region name : ap-southeast-1
Default output format: json

---> Test access: aws s3 ls


# VII. After run, there is a error message like below:
### 1. ImportError: libGL.so.1: cannot open shared object file: No such file or directory
--> Install the missed library and everything is fixed. (ChatGPT)

sudo apt-get install libgl1-mesa-glx

### 2. Update Allow Host
ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]

### 3. Wrong path in .env (edited)
MEDIA_ROOT=/home/ubuntu/venv/sudoku/sudoku_project/sudoku_app/media
MEDIA_URL=/image/
IMAGE_UPLOAD_PATH=/home/ubuntu/venv/sudoku/Images/crop-input-image
IMAGE_TRANSFORM_CROP=/home/ubuntu/venv/sudoku/Images/crop-input-image
STATIC_ROOT=/home/ubuntu/venv/sudoku/sudoku_project/static
DEBUG=FALSE
ALLOWED_HOSTS=52.68.221.167

##Launch successfully in local
--> python manage.py runserver 0.0.0.0:8000

# VIII. Deploy on Production using uWSGI and Ngnix
https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

Please follow above guide
### 1. install uwsgi
pip3 install uwsgi

### 2. Run uwsgi --http :8000 --module sudoku_project.wsgi
This command have to be run in the same direction of manage.py

### 3. Install and start nginx 
sudo apt-get install nginx

sudo /etc/init.d/nginx start    # start nginx
Also, can start nginx by below command:
sudo service nginx start
sudo service nginx status


### 4. The upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

mysite_nginx.conf
# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 52.68.221.167; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /home/ubuntu/venv/sudoku/sudoku_project/sudoku_app/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /home/ubuntu/venv/sudoku/sudoku_project/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/ubuntu/venv/sudoku/sudoku_project/uwsgi_params; # the uwsgi_params file you installed
    }
}

Test connect nginx and uwsgi
uwsgi --socket mysite.sock --module sudoku_project.wsgi --chmod-socket=664

### 5. mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/ubuntu/venv/sudoku/sudoku_project
# Django's wsgi file
module          = sudoku_project.wsgi
# the virtualenv (full path)
home            = /home/ubuntu/venv

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = /home/ubuntu/venv/sudoku/sudoku_project/mysite.sock
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true

# IX. Using Port 80 instead port 8000
1. In /etc/nginx/sites-enabled/
edit mysite_nginx.conf file:

server{
listen: 80;
......................
}

2. There is a default file in sites-enabled,
comment the port: 80 in line:
listen: 80

# X. Run server even when turnoff terminal using systemd
----------------------------------------------------------------------------------------------------------
#### 1. create a directory for the vassals
sudo mkdir -p /home/ubuntu/venv/vassals
#### 2. symlink from the default config directory to your config file
sudo ln -s /home/ubuntu/mysite_uwsgi.ini /home/ubuntu/venv/vassals
#### 3. run the emperor
uwsgi --emperor /home/ubuntu/venv/vassals --uid www-data --gid www-data

----> The browser will be run

#### 4. Startup uWSGI when the system boots. Create file "emperor.uwsgi.service" a systemd service at: etc/systemd/system/
----------------------------------------------------------------------------------------------------------
[Unit]
Description=uwsgi emperor for micro domains website
After=network.target
[Service]
User=ubuntu
Restart=always
ExecStart=/home/ubuntu/venv/bin/uwsgi --emperor /home/ubuntu/venv/vassals --uid www-data --gid www-data
[Install]
WantedBy=multi-user.target
----------------------------------------------------------------------------------------------------------

### 5. Command
systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service

systemctl status emperor.uwsgi.service
systemctl stop emperor.uwsgi.service
systemctl restart emperor.uwsgi.service

Follow the instruction at:
https://tonyteaches.tech/django-nginx-uwsgi-tutorial/

# XI. Operation command

1. Login to EC2
 ssh -i /Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku-info/pro-sudoku/pro-sudoku.pem ubuntu@ec2-52-68-221-167.ap-northeast-1.compute.amazonaws.com

 2. active virtual enviroment
 source venv/bin/activate

 3. Pull code from master
 git pull origin master

 4. Restart uWSGI
 sudo systemctl restart emperor.uwsgi.service

 5. Restart Nginx
 sudo service nginx restart

