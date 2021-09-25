ATM
=========

# Installation

## Install OS (Ubuntu) Requirements

## Install Django

## Clone Project

    git clone <repository-url>

## Virtual Envirnoment and requirements

    virtualenv -p /path/to/python3.7 venv
    source venv/bin/activate
    pip install -r requirements.txt

## pip install -r requirements.txt

## Postgres setup

    pip install psycopg2
    sudo su - postgres
    psql
    CREATE USER your-username WITH PASSWORD your-password;
    ALTER USER your-username WITH SUPERUSER;
    CREATE DATABASE db_name;
    GRANT ALL PRIVILEGES ON DATABASE db_name TO your-username;
    \q
    psql -d mu_db -U your-username -h localhost


## run migrations
   python manage.py makemigrations
   python manage.py migrate

## Running Development Server

    python manage.py runserver

**Note:** Never forget to enable virtual environment (`source venv/bin/activate`) before running above command and use settings accordingly.



API collection is as -
https://www.getpostman.com/collections/6280bb0d5bd7b16bee10
