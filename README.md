Work Order System
===
`Editor： Wallace Chiu`  
`Last update： 2024/ 7/ 3 16:30`  

Information
---
- Build Environment 
    - Window OS
    - PostgreSQL 16.3
    - Python 3.10.12 
    - Django 5.04 
    - Git 2.45.1

- Github Repository
    - [WEB_WO_WA_MA]([https://github.com/wallacechiu/WEB_WO_WA](https://github.com/cytoaurora-admin/WEB-WO-WA-MA.git))

Deployment
---
### Window OS
- Install [PostgreSQL 16.3](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259019)
    - When you are installing, pay attention to the following points
    - Set the password for ```postgres``` as ```cytoaurora```
    - Uncheck the box for ```Stack Builder``` then finish

- Install [Python 3.10.12](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)
    - When you are installing, pay attention to the following points
    - Check the box for ```Install launcher for all users (recommended)```
    - Check the box for ```Add the Python 3.10.12 to PATH```

- Install Django 5.04
    - Open the terminal
    - Enter ```pip install django==5.0.4``` 
    - Enter ```pip show django``` to check version
    - Install the necessary django packages
    - Enter ```pip install django-filter==2.4.0```
    - Enter ```pip show django-filter``` to check version
    - Enter ```pip install openpyxl==3.1.3```
    - Enter ```pip show openpyxl``` to check version
    - Enter ```pip install bs4==0.0.2```
    - Enter ```pip show bs4``` to check version


- Install [Git 2.45.1](https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe)
    - Open the Git Bash
    - Enter ```git config --global user.name "wallacechiu"```
    - Enter ```git config --global user.email wallace.chiu@cytoaurora.com```

- Set up PostgreSQL
    - Open the terminal
    - Enter ```cd "c:\Program Files\PostgreSQL\16\bin"```
    - Enter ```psql -U postgres```
    - Enter the password ```cytoautota```
    - Enter ```create database clinical```
    - Enter ```\q```
    - Enter ```psql -U postgres clinical < .../your/path/clinical.sql``` 
    - Enter ```psql -U postgres clinical```
    - Enter ```\d``` to check database tables

- Set up WEB_WO_WA
    - Clone the WEB_WO_WA from GitHub
    - Open the terminal
    - Enter ```cd .../your/path```
    - Enter ```git clone https://github.com/wallacechiu/WEB_WO_WA.git```
    - Enter ```cd WEB_WO_WA```
    - Enter ```python .\manage.py makemigrations```
    - Enter ```python .\manage.py migrate```
    - Enter ```python .\manage.py runserver``` (It will run on localhost)

- Set up Skyeyes
    - Open the task scheduler
    - Create task work
    - Configure the system to start task at boot
    - Set the execution path for skyeyes.py
    - Start the task after configuration is complete 

- Set up database backup
    - Open the db_backup.bat
    - Set the path for BACKUP_FILE
    - Open the task scheduler
    - Create task work
    - Schedule to run every day at 12 PM and 5 PM
    - Set the execution path for db_backup.bat
    - Start the task after configuration is complete 

- Set up spider
    - Open the spider.py
    - Set the path for file_path
    - Open the task scheduler
    - Create task work
    - Schedule for the last day of December each year
    - Set the execution path for spider.py
    - Start the task after configuration is complete

- Deployment is completed successfully
