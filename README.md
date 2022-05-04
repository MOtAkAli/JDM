# JDM (Japanese Domestic Market)
## Car Rental Web App

<hr>

## Clone repository
```bash
git clone https://github.com/MOtAkAli/JDM.git
```

<hr>

## Set up environment
### Install `virtualenv`
```bash
pip install virtualenv
```
### Change current directory to `JDM`
```bash
cd JDM
```
### Create python virtual environment
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
source /path/to/ENV/bin/activate
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

<hr>

# DB
- `LDM` (Logical Data Model)

![JDM-MLD](https://user-images.githubusercontent.com/79842485/166304950-ea016a99-ecd0-4664-a05d-025f62b81285.png)
