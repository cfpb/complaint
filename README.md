# :warning: THIS REPO IS DEPRECATED (12/3/2018) :warning:
Please migrate to using [cfgov-refresh](https://github.com/cfpb/cfgov-refresh).

[![Build Status](https://travis-ci.org/cfpb/complaint.png)](https://travis-ci.org/cfpb/complaint) [![Coverage Status](https://coveralls.io/repos/github/cfpb/complaint/badge.svg?branch=master)](https://coveralls.io/github/cfpb/complaint?branch=master)

complaint
============
Standalone Django project that runs the [Consumer Complaint Database](http://www.consumerfinance.gov/complaintdatabase) application.

![Consumer Complaint Database website screenshot](https://raw.githubusercontent.com/cfpb/complaint/master/screenshot-complaintdatabase.png)


## Dependencies

- Unix-based OS (including Macs). Windows is not supported at this time.
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/#), Python modules that keep dependencies  project specific and in their own virtual environments.
- [Autoenv](https://github.com/kennethreitz/autoenv)
- [Node](http://nodejs.org/)
- [Gulp](http://gulpjs.com/)
- [Capital Framework](http://cfpb.github.io/capital-framework/)
- [LESS](http://lesscss.org/)

## Setup

1. Set up virtual environment:

  ```bash
  mkvirtualenv ccdb
  workon ccdb
  ```
1. Install Django 1.8.14 and Python dependencies:

  ```bash
  pip install -r requirements.txt
  ```
1. Run server locally:

  ```bash
  python manage.py runserver
  ```
1. To set up the front end, first install Gulp if you don't have it:

  ```bash
  npm install --global gulp
  ```
1. Install [Autoenv](https://github.com/kennethreitz/autoenv) if needed:

  ```bash
  $ pip install autoenv
  ```
1. Copy `.env_SAMPLE` to `.env` and cd into root directory to execute `.env`.

  ```bash
  cp .env_SAMPLE .env
  cd ../complaint
  ```
1. Run the front end build script to compile JavaScript, CSS, and image assets:

  ```bash
  sh ./setup.sh
  ```
1. Go to landing pages:
  - http://127.0.0.1:8000/complaintdatabase/
  - http://127.0.0.1:8000/complaint/data-use/
  - http://127.0.0.1:8000/complaint/process/
  - http://127.0.0.1:8000/complaint/


### Installing app to your project
The Complaint Database and Complaint apps can be installed into other Django projects by doing the following:

In your Django project `url.py`, you will need to include the following in your `urlpatterns` list for each app:
```python
url(r'^complaint/', include('complaint.urls')),
url(r'^complaintdatabase/', include('complaintdatabase.urls')),
```

In your Django project `settings.py`, you will need to include the following in your `INSTALLED_APPS` tuple:
```python
'complaint_common',
'complaint',
'complaintdatabase',
```

Add this to your `requirements.txt` file:
```
-e git+https://github.com/cfpb/complaint.git#egg=complaintdatabase
```

Then run the `requirements.txt` file in your terminal your virtual environment:
```
pip install -r requirements.txt
```


## Testing
For Python/Django tests, in the base directory, run the following:

```shell
pip install -r test_requirements.txt
./pytest.sh
```
