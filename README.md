# Task Management System
## Description
This is a task management system that allows users to create tasks, synchronize them with their calendar and View task locations in Google Maps.

## Technologies used
1. Django
2. Django Rest Framework
3. Celery
4. Redis
5. Postgres
6. Docker
7. Docker Compose
8. Javascript
9. HTML
10. CSS
11. Bootstrap
12. Python
13. GeoDjango
14. PostGIS

## Instructions
To start running the application, you need to have installed: docker and docker-compose.
make sure that docker is running on your machine. if on windows, make sure that you have enabled the linux subsystem.
Also, make sure that you have installed make.
## How to run the application
1. Clone the repository
2. Go to the root directory of the project
3. create a file called `.env` and copy the contents of `.env.example` into it and fill in the values
4. Run the command: `make build`
5. Run the command: `make migrate`
6. Run the command: `make superuser`

application will be running on `http://localhost:8000`

## How to login to the admin panel
1. Go to `http://localhost:8000/admin`
2. Enter the email and password that you have set during the `make superuser` command