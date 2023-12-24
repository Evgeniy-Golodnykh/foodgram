# Foodgram

### Description
Foodgram is a website where users will publish recipes, add other people's recipes to their favorites, and subscribe to other authors' publications. The "Shopping List" service will allow users to create a list of products that need to be purchased to prepare selected dishes.

### Quick Start
1. Clone repo
```bash
git clone git@github.com:Evgeniy-Golodnykh/foodgram.git
```
2. Creates the virtual environment
```bash
python3 -m venv venv
```
3. Activates the virtual environment
```bash
source venv/bin/activate
```
4. Upgrade PIP and install the requirements packages into the virtual environment
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
5. To create the database use command
```bash
python3 manage.py migrate
```
6. To fill the database use command
```bash
python3 manage.py filldatabase
```
7. To run the application use command
```bash
python3 manage.py runserver
```

### API Documentation
http://127.0.0.1:8000/redoc/

### Technology
[Python](https://www.python.org), [Django REST framework](https://www.django-rest-framework.org), [PostgreSQL](https://www.postgresql.org/), [Docker](https://www.docker.com/), GitHub Actions

### Author
[Evgeniy Golodnykh](https://github.com/Evgeniy-Golodnykh)

### CI/CD pipeline status
![Foodgram workflow](https://github.com/Evgeniy-Golodnykh/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
