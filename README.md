CCDB-content
============

## setup

1. copy settings_secret.py.template to settings_secret.py
1. set up virtual environment 

  ```
  mkvirtualenv ccdb
  workon ccdb
  ```
1. install Django 1.6 etc

  ```
  pip install -r requirements.txt
  ```
1. run server

  ``` 
  python manage.py runserver 
  ```
1. go to landing pages: 
  - http://127.0.0.1:8000/landing_pages/data-use-content/
  - http://127.0.0.1:8000/landing_pages/landing-page/
  - http://127.0.0.1:8000/landing_pages/technical-documentation/
