# RangoApplication
An application that allows people to view, add, and update categories. Categories represent containers for pages. Users can view their own profiles as well as other users' profiles.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
In a folder of your choice execute the following commands in terminal:

```
mkvirtualenv --python=python3.5 rango
pip install -U django==1.9.10
pip install pillow
pip install django-registration-redux
pip install django-bootstrap-toolkit
git clone https://github.com/vtaskow/RangoApplication.git
```

In the main folder in which manage.py resides, execute the following commands:

```
python manage.py makemigrations rango
python manage.py migrate
python populate_rango.py
```

To run the web application on your localhost:

```
python manage.py runserver
```
## Built With
* [Django](https://www.djangoproject.com/) - The web framework used
