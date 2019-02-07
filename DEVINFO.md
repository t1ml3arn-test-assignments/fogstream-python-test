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

- Open `admin.py` in your application's folder
- import your models e.g. `from myapp.models import MyModel`
- register it with `admin.site.register(MyModel)`

### Logging to console

TODO

### Email backend

TODO

## Unit testing

TODO