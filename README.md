# Banking Django App

This is a web application for online banking.

## Running project in development

**Requirements**
- python 3.11
- [poetry](https://python-poetry.org/docs/#installation) dependency management tool

**Setup**

1. Clone the repository
    - `git clone git@github.com:kea-devops/exam_project.git`
    - `cd exam_project`

2. Install dependencies and initiate virtual environment
    - `poetry install`
    - `poetry shell`

3. Run database migrations and seed data
    - `python manage.py migrate`
    - `python manage.py provision`
        - creates a default admin account with staff and superuser privileges. 
        - Admin credentials:
            - username: `admin`
            - password: `123456`

4. Run the development server
    - `python manage.py runserver` 

