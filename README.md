# JDM (Japanese Domestic Market)
## Car Rental Web App

<hr>

## Clone repository
```bash
  git clone https://github.com/MOtAkAli/JDM.git
```

<hr>

## Set up environment (Use `Git Bash` terminal):
### Change current directory to `JDM`
```bash
  cd JDM
```
### Create python virtual environment
```bash
  python -m venv venv
```
### Activate it
```bash
  source venv/Scripts/activate
```
### Install `Django`
```bash
  pip install django
```
### Apply `migrations`
```bash
  python manage.py migrate
```
### Create your `superuser` for `django admin panel`
```bash
  python manage.py createsuperuser
```
### Run server
```bash
    python manage.py runserver
```
