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
1. install Gulp

  ``` 
  npm install --global gulp
  ``` 
1. install [Autoenv](https://github.com/kennethreitz/autoenv) 

  ```
  $ pip install autoenv
  ```
1. copy `.env_SAMPLE` to `.env` and cd into root directory to execute `.env`.

1. run front end build

  ``` 
  sh ./setup.sh
  ``` 
1. go to landing pages: 
  - http://127.0.0.1:8000/ccdb_content/data-use-content/
  - http://127.0.0.1:8000/ccdb_content/landing-page/
  - http://127.0.0.1:8000/ccdb_content/technical-documentation/
