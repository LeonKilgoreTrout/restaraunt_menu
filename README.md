# RestaurantApp

### 10 steps to become awesome
1) Go to the root directory for this project
2) Create and activate your own virtual environment
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

and set such thing in alembic.ini file

* prepend_sys_path = ./app

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
10) You're awesome!

### Two more things to save your time: logs directory & postman results

![alt text](https://github.com/LeonKilgoreTrout/restaraunt_menu/blob/main/postman_results.png)

### Feedback
There is one mistake in postman tests: Проверка кол-ва блюд и подменю в меню -> Просматривает список блюд

It returns empty list, but supposed to throw 404, because such target_menu_id doesn't exist.
