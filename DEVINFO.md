# Fogstream test task developer info

## What is it

This doument contains some instructions - what to install and how to configure it.

## Installation and configuration

Assuming you have Python 3.7 and it is needed to work with 3.6

- Install python 3.6 to separate folder (e.g. `C:\Python36`). Don't create any file associations and PATH variables
- Add python 3.6 path to the end of PATH environment variable
- Open console and `cd PYTHON_36_PATH`
- then `mklink py3.exe python.exe`
- Now you can run python 3.6 from cmd with `py3` command. Test is with `py3 -V` - output should be `Python 3.6.7` (patch-number might be different)

### Create django virtual environment

```bash
pip install virtualenvwrapper-win
mkvirtualenv -p=py3 django
# it is possible to replace py3 above with full path
# to disireable python version e.g C:\Python36\python.exe

pip install django

# checking installation
py -m django --version  # 2.1.5
```

## Configuration

### Basic project and `send_msg` application creation

```bash
mkdir django_projects
cd django_projects
django-admin startproject fogsite
cd fogsite

# this must be run in the same folder as project's manage.py
django-admin startapp sen_dmsg
```

### Register sen_dmsg app

- goto `fogsite` folder where settings.py is present (`cd fogsite is enough`)
- add a new line `'sendmsg.apps.SendmsgConfig'` at the end of `INSTALLED_APPS` list

NOTE: similar actions for `site_auth` application must be made

### Register model in admin site

- Open `admin.py` in yo`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` settingur application's folder
- import your models e.g. `from myapp.models import MyModel`
- register it with `admin.site.register(MyModel)`

### Logging to console

Add this to settings

```py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': "DEBUG",
        },
    }
}
```

Use logger in code:

```py
import logging

logger = logging.getLogger(__name__)
logger.info('hello there')
```

### Email backend

For testing email sending there is a built-in functionality in Django.
Anyway, I configure console email backend

- open `settings.py`
- add `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` setting

## Unit testing

```bash
cd send_msg
mkdir tests
# create an empty file (tells Python that dir is a package)
copy NUL __init__.py
```

- write your test in files like `test_something.py`
- run tests with `py manage.py test`
