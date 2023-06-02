# `JDM` (Japanese Domestic Market)

## `Demonstration`

https://github.com/voidnowhere/JDM/assets/79842485/0e803378-a75d-4b0f-aea2-2fcad36c071d

<hr>

## Car Rental Web App

<hr>

## `Clone repository`
```bash
git clone https://github.com/MOtAkAli/JDM.git
```

<hr>

## `Set up environment`
### Install `virtualenv`
```bash
pip install virtualenv
```
### Change current directory to `JDM`
```bash
cd JDM
```
### Create `.env` file and fill it
```bash
cat .env-example > .env
```
### Use the output of this python code to get random Django SECRET_KEY as your `SECRET_KEY` in `.env file` be aware this code needs Django to be installed use `pip install Django`
```python
from django.core.management import utils
print(utils.get_random_secret_key())
```
### Create python `virtual environment`
```bash
python -m venv venv
```
### Activate it
- `Command Prompt`
```bash
venv\Scripts\activate.bat
```
- `Linux`
```bash
source venv/Scripts/activate
```
- `PowerShell`
no scripts like the activate script are allowed to be executed so you need to run PowerShell as `admin` and change `ExecutionPolicy` to `AllSigned` then type `A` to `Always run` `the command is under` in the end use `the command above` to activate virtual environment
```bash
Set-ExecutionPolicy AllSigned
```
### Install `virtualenv requirements`
```bash
pip install -r requirements.txt
```
### Make `migrations`
```bash
python manage.py makemigrations
```
### Apply `migrations`
```bash
python manage.py migrate
```
### Populate `DB` with `cities`
```bash
python manage.py cities_light
```
### Create your `superuser` for `django admin site`
```bash
python manage.py createsuperuser
```
### Run server
```bash
python manage.py runserver
```

<hr>

# `Database`
- `LDM` (Logical Data Model)

![MLD](https://user-images.githubusercontent.com/79842485/170586342-046faf28-5a12-43ec-9c5d-6184c542a64d.png)

# `Needs to be done`
### Always check `requirements.txt` if there is some `new packages` to be `installed`
