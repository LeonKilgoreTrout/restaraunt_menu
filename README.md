### Current project able to work locally and in Docker container, but testing part works only locally. I'm going to fix it asap.

# RestaurantApp

## Local case
1) Clone, then go to the root directory of this project

2) Create and activate your own virtual environment
```commandline
python -m venv create venv
```
3) Run:
```
pip install -r requirements.txt 
```

4) I kept my alembic files in case you won't spend your time for running the app :)
Otherwise, I recommend to drop alembic directory and alembic.ini file and run:

```
alembic init alembic
```
5) Then add lines below to alembic/env.py 

* from dotenv import load_dotenv

* import os

* from models import Base

* from models import Menu, Submenu, Dish

* load_dotenv()

* config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

6) Change .env file with respect to your local postgres
7) Run:
```
alembic revision --autogenerate -m "Added following tables: menus, submenus, dishes"
alembic upgrade head
```
8) Change directory to /app
```commandline
cd app
```
9) Run next command to start app on your localhost
```commandline
uvicorn main:app --reload
```
10) To run tests please use
```commandline
pytest -v 
```
from root directory

## Docker case

1) create networks:
``` 
docker network create restaurant
docker network create restaurant_test
```
2) run 
```commandline
docker-compose up
```
to get project and postgres in containers

3) run (currently I have problems with the sane postgres as perfectly works in app)
```commandline
docker-compose up -f docker-compose-test.yml
```
to run tests 
