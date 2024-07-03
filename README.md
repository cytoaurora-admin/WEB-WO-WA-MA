# Work Order System

`Editor： Wallace Chiu`  
`Last update： 2024/ 7/ 3 16:30`

## Information

-   Build Environment

    -   Window OS / Ubuntu 22.04
    -   PostgreSQL 16.3
    -   Python 3.10.12
    -   Django 5.04
    -   Git 2.45.1

-   Github Repository
    -   [WEB_WO_WA_MA](https://github.com/cytoaurora-admin/WEB-WO-WA-MA.git)

## Deployment

### Window OS

-   Install [PostgreSQL 16.3](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259019)

    -   When you are installing, pay attention to the following points
    -   Set the password for `postgres` as `cytoaurora`
    -   Uncheck the box for `Stack Builder` then finish

-   Install [Python 3.10.12](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)

    -   When you are installing, pay attention to the following points
    -   Check the box for `Install launcher for all users (recommended)`
    -   Check the box for `Add the Python 3.10.12 to PATH`

-   Install Django 5.04

    -   Open the terminal
    -   Enter `pip install django==5.0.4`
    -   Enter `pip show django` to check version
    -   Install the necessary django packages
    -   Enter `pip install django-filter==2.4.0`
    -   Enter `pip show django-filter` to check version
    -   Enter `pip install openpyxl==3.1.3`
    -   Enter `pip show openpyxl` to check version
    -   Enter `pip install bs4==0.0.2`
    -   Enter `pip show bs4` to check version

-   Install [Git 2.45.1](https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe)

    -   Open the Git Bash
    -   Enter `git config --global user.name "wallacechiu"`
    -   Enter `git config --global user.email wallace.chiu@cytoaurora.com`

-   Map network drive

    -   Enter the network path of the drive
    -   Enter `Z:/CytoAurora TIFF Images`

-   Set up PostgreSQL

    -   Open the terminal
    -   Enter `cd "c:\Program Files\PostgreSQL\16\bin"`
    -   Enter `psql -U postgres`
    -   Enter the password `cytoautota`
    -   Enter `create database clinical`
    -   Enter `\q`
    -   Enter `psql -U postgres clinical < .../your/path/clinical.sql`
    -   Enter `psql -U postgres clinical`
    -   Enter `\d` to check database tables

-   Set up WEB_WO_WA

    -   Clone the WEB_WO_WA from GitHub
    -   Open the terminal
    -   Enter `cd .../your/path`
    -   Enter `git clone https://github.com/wallacechiu/WEB_WO_WA.git`
    -   Enter `cd WEB_WO_WA`
    -   Enter `python .\manage.py makemigrations`
    -   Enter `python .\manage.py migrate`
    -   Enter `python .\manage.py runserver` (It will run on localhost)

-   Set up Skyeyes

    -   Open the task scheduler
    -   Create task work
    -   Configure the system to start task at boot
    -   Set the execution path for skyeyes.py
    -   Start the task after configuration is complete

-   Set up database backup

    -   Open the db_backup.bat
    -   Set the path for BACKUP_FILE
    -   Open the task scheduler
    -   Create task work
    -   Schedule to run every day at 12 PM and 5 PM
    -   Set the execution path for db_backup.bat
    -   Start the task after configuration is complete

-   Set up spider

    -   Open the spider.py
    -   Set the path for file_path
    -   Open the task scheduler
    -   Create task work
    -   Schedule for the last day of December each year
    -   Set the execution path for spider.py
    -   Start the task after configuration is complete

-   Deployment is completed successfully

---

### Ubuntu 22.04

-   Update Ubuntu Packages

    -   Open the terminal
    -   Enter `sudo apt update && sudo apt upgrade`

-   Install PostgreSQL 16.3 ([Detail guide](https://www.youtube.com/watch?v=tducLYZzElo))

    -   Open the terminal
    -   Enter `sudo apt install -y postgresql-common`
    -   Enter `sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh`
    -   Import the repository signing key
    -   Enter `apt install curl ca-certificates`
    -   Enter `install -d /usr/share/postgresql-common/pgdg`
    -   Enter `sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc`
    -   Create the repository configuration file
    -   Enter `sudo sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'`
    -   Update the package lists
    -   Enter `sudo apt update`
    -   Enter `sudo apt -y install postgresql-16`
    -   Enter `sudo -u postgres psql`
    -   Enter `\q`

-   Install Python 3.10.12

    -   Open the terminal
    -   Enter `sudo apt install python3-pip`
    -   Enter `python3 --version` to check version
    -   Enter `pip3 --version` to check version

-   Install Django 5.04 ([Detail guide](https://ultahost.com/knowledge-base/install-django-ubuntu/))

    -   Open the terminal
    -   Enter `sudo pip3 install django==5.0.4`
    -   Enter `django-admin --version` to check version
    -   Install the necessary django packages
    -   Enter `sudo pip3 install django-filter==2.4.0`
    -   Enter `pip3 show django-filter` to check version
    -   Enter `sudo pip3 install openpyxl==3.1.3`
    -   Enter `pip3 show openpyxl` to check version
    -   Enter `sudo pip3 install bs4==0.0.2`
    -   Enter `pip3 show bs4` to check version

-   Install Git 2.45.1

    -   Open the terminal
    -   Enter `sudo add-apt-repository ppa:git-core/ppa`
    -   Enter `sudo apt update`
    -   Enter `sudo apt install git`
    -   Enter `git --version` to check version

-   Map network drive

    -   Enter `smb://10.0.0.45/cytoaurora tiff images`

-   Set up PostgreSQL

    -   Open the terminal
    -   Enter `sudo su`
    -   Enter `su postgres`
    -   Enter `psql`
    -   Enter `create database clinical`
    -   Enter `\q`
    -   Enter `psql clinical < .../your/path/clinical.sql`
    -   Enter `psql clinical`
    -   Enter `\d` to check database tables

-   Set up WEB_WO_WA

    -   Clone the WEB_WO_WA from GitHub
    -   Open the terminal
    -   Enter `cd .../your/path`
    -   Enter `git clone https://github.com/wallacechiu/WEB_WO_WA.git`
    -   Enter Username for 'https://github.com': `wallacechiu`
    -   Enter Password for 'https://wallacechiu@github.com': personal access token (request from github account holder)
    -   Open the setting.py file in the WEB_WO_WA directory with editor
    -   Set `ALLOWED_HOSTS` to your IP address
    -   Open views.py and locate the `wo_ab_gen` function
    -   Change the path of `nas_path` to the directory used for Linux
    -   Back to the terminal
    -   Enter `cd WEB_WO_WA`
    -   Enter `python3 .\manage.py makemigrations`
    -   Enter `python3 .\manage.py migrate`
    -   Enter `python3 .\manage.py runserver IP:8000`

-   Set up Skyeyes

    -   Open the terminal
    -   Enter `sudo su`
    -   Enter the configured password
    -   Enter `crontab -e` to edit crontab
    -   Enter `* * * * * python3 .../your/path/WEB_WO_WA/add-on/skyeyes.py`
    -   Press `Ctrl + O` to save
    -   Press `Ctrl + X` to exit

-   Set up database backup

    -   Open the terminal
    -   Enter `sudo su`
    -   Enter the configured password
    -   Enter `crontab -e` to edit crontab
    -   Enter `0 12 * * * PGPASSWORD='cytoaurora' pg_dump -U postgres -h localhost -F p clinical > ".../your/path/$(date +\%Y\%m\%d_\%H\%M)_backup.sql.tar"\`
    -   Enter `0 17 * * * PGPASSWORD='cytoaurora' pg_dump -U postgres -h localhost -F p clinical > ".../your/path/$(date +\%Y\%m\%d_\%H\%M)_backup.sql.tar"\`
    -   Press `Ctrl + O` to save
    -   Press `Ctrl + X` to exit

-   Set up OneDrive backup ([Detail guide](https://ubuntuhandbook.org/index.php/2024/02/install-onedrive-ubuntu/))

    -   Open the terminal
    -   Enter `sudo apt install onedrive`
    -   Enter `onedrive`
    -   Click `Accept` to grant permissions to access your OneDrive account
    -   After that, the web page will be redirect to a blank page. Just copy the url of that blank page, and paste into the terminal window and hit Enter
    -   If done successfully, the terminal will output somethings says `Application has been successfully authorized`
    -   Enter `onedrive --dry-run --synchronize`
    -   This command will run the client to test, A OneDrive folder will be created (if not exist) in your user home directory for syncing files.
    -   To start syncing files, enter `onedrive --synchronize`
    -   For choice, you may sync only single folder only, for example “Pictures” sub-folder under OneDrive directory, by enter `onedrive --synchronize --single-directory 'Pictures'`
    -   Or, do uploading local files only via enter `onedrive --synchronize --upload-only`
    -   Enter `systemctl enable --user onedrive` to enable the service
    -   Enter `systemctl start --user onedrive` to start it
    -   Finally, check the service status by entering `systemctl status --user onedrive`

-   Set up spider
    -   Open the spider.py
    -   Set `file_path = f"your/path/WEB_WO_WA/add-on/calendar/{title}.csv"`
    -   Open the terminal
    -   Enter `sudo su`
    -   Enter the configured password
    -   Enter `crontab -e` to edit crontab
    -   Enter `0 18 31 12 * python3 .../your/path/WEB_WO_WA/add-on/spider.py`
    -   Press `Ctrl + O` to save
    -   Press `Ctrl + X` to exit
-   Deployment is completed successfully
