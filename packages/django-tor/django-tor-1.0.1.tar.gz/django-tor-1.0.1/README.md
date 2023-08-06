# django-tor

Run your django website on tor using django_tor.It doesn’t interfere with other tor processes on your computer, so you can use the Tor Browser or the system tor on their own.

 [![PyPI version](https://badge.fury.io/py/django-tor.svg)](https://badge.fury.io/py/django-tor)
 [![Downloads](https://pepy.tech/badge/django-tor/month)](https://pepy.tech/project/django-tor)
 [![Downloads](https://static.pepy.tech/personalized-badge/django-tor?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/django-tor)
 ![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)


### Disclaimer:-
Use it only for educational purpose.

## Features
- No need root permission
- Multiple instances

## Compatability
Python 3.6+ is required.

## Installation

```bash
pip install django-tor
```

## Uses

set ALLOWED_HOSTS to * in settings.py 
```
ALLOWED_HOSTS = ['*']
```

add this lines in manage.py in your django project.
```py
from django_tor import run_with_tor
from django.core.management.commands.runserver import Command as runserver

if sys.argv[1] == 'runserver':
    host, port = run_with_tor()
    runserver.default_port = str(port)
    from djangoTor.settings import ALLOWED_HOSTS
    ALLOWED_HOSTS.append(host)
```

Run django server with noreload argument.
```sh
python3 manage.py runserver --noreload
```

### Credit :- [onionshare](https://github.com/onionshare/onionshare)