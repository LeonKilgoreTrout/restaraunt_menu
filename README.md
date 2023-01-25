# RestaurantApp

## Docker containers case

1) Create 2 different networks e.g.:
``` 
docker network create restaurant
docker network create restaurant_test
```
2) Check in .env file -> DB_HOST variable is set "postgres"
3) run 
```commandline
docker-compose up
```
to get project and postgres in containers

4) run
```commandline
docker-compose up -f docker-compose-test.yml
```
to run tests 

## Local case
1) Clone, then go to the root directory of this project
2) Create and activate your own virtual environment e.g.:
```commandline
python -m venv create venv
```
3) Run:
```
pip install -r requirements.txt 
```
4) Check in .env file -> DB_HOST variable is set "localhost"
5) Change .env file with respect to your local postgres server
6) Run:
```
alembic revision --autogenerate -m "Added following tables: menus, submenus, dishes"
alembic upgrade head
```
7) Run next command to start app on your localhost
```commandline
uvicorn app.backend.main:app --reload
```
8) To run tests please use
```commandline
pytest -v 
```
from root directory

