#! /bin/bash
# run python unittests and coverage

export DJANGO_SETTINGS_MODULE=ccdb.settings
coverage run --rcfile=.coveragerc --source='.' manage.py test
coverage report -m
