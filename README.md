# Decathlon Recruitment Task 

[TOC]

# setup
```
$ git clone git@github.com:mkopr/drt.git
$ cd drt
$ touch .env
Add enviroment variables - check bellow
$ docker-compose build
$ docker-compose run web python manage.py migrate
$ docker-compose up
```
API documentation URL: `0.0.0.0:8000`  
Base URL: `0.0.0.0:8000/api`  
Service logs in file `drt_logs.log`


# enviroment variables
set `SECRET_KEY`, `DEBUG` and `API_KEY` variables in `.env` file.  
get `API_KEY` from [omdbapi](http://www.omdbapi.com/apikey.aspx)
 
Example:
```
API_KEY=123qwerty!
SECRET_KEY=123qwerty!
DEBUG=True
```

# chosen third-party libraries
djangorestframework - for REST API implementation in Django;  
django-extensions - custom extensions for the Django Framework;  
django-filter - for filters in Movie ans Comment views;  
drf-yasg - for swagger documentation  
flake8 - for code validation;  
isort - for imports validation;  
psycopg2 - for connection with PostgreSQL db;  
python-decouple - for enviroment variables;  
requests - for fetch data from public movie database.  

# tests
```
$ docker-compose run web python manage.py test
```