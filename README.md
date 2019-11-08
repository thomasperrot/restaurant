# Restaurant

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Build Status](https://travis-ci.com/thomasperrot/restaurant.svg?branch=master)](https://travis-ci.org/thomasperrot/restaurant)
[![codecov](https://codecov.io/gh/thomasperrot/restaurant/branch/master/graph/badge.svg)](https://codecov.io/gh/thomasperrot/restaurant)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple Django REST API to CRUD restaurants

## Installation

```
$ pip3 install -r requirements/local.txt
$ cd app
$ python3 manage.py migrate
$ python3 manage.py runserver
```

## Testing

```
$ pip3 install -r requirements/test.txt
$ cd app
$ python3 manage.py test
```

## Documentation

Documentation is available at `<YOUR_URL>/swagger/`

## Improvements

- use env variables to store secrets
- deploy in production with docker or AppEgine
- use postgres