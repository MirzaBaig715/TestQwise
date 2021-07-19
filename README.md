# TestQwise

 Todo application apis.

## Getting Started

Kindly create virtual environment if you don't want to mess up libraries =)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9
- Django 3.2.1
- Django Rest Framework 3.12.4
- djangorestframework-simplejwt 4.7.2


### Installing

First clone the repo into your local directory.

```
git clone https://github.com/MirzaBaig715/TestQwise
```
### Setup

Create `Virtual environment` in project directory
```
$ python -m venv envname
$ source envname/bin/activate
```

Create User
```
python manage.py createsuperuser --username admin --email admin
```
Get Token to make authorized calls
```
Access token is required so we can get token from this endpoint `/api/token/` in order to create todos tasks.
```
Thats it! Now you can go to [localhost:8000/api/todo/](localhost:8000/api/todo/).

Postman documentation can be found [here](https://documenter.getpostman.com/view/5135674/TzmCiZHy)