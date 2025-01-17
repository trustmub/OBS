# OBS
Open Banking system

This is an open source banking system, developed using Flask  python framework

Create The database

    python3 build_database.py

Create the prerequisite system defaults

    python3 create_entries.py

Create system defaults

     chmod -R 777 /src

Notes:
 - database environment path
 - secret environment path

Docker:

if database does not exist follow instructions below

1. get into the mysql container using the following commands
    - `docker exec -it <Container_ID> bash`
    - `mysql -uroot -p<root_password>`
    - `CREATE DATABASE bank_base`
    - `exit`
    - `exit`
2. Get into the flask application container using the following commands
    - `docker exec -it <Container_ID> bash`
    - `python build_database.py`
    - `python create_entries.py`
    - `exit`


removing volumes:

docker volume rm obs_mysql-flask-app-volume

docker volume ls                                
DRIVER    VOLUME NAME
local     obs_mysql-flask-app-volume
local     obs_mysql-flask-app-volume-config

