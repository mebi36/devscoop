# devscoop
A Django-based news service based on the HackerNews API

### Setup
Begin by cloning this repository:

    git clone https://github.com

Set up a virtual environment:

    virtualenv venv

Navigate to the project directory:

    cd devscoop

Install project dependencies from requirements.txt file located in the project root directory:

    pip install -r requirements.txt


Make migrations to initialize database

    (venv)> python manage.py makemigrations
    (venv)> python manage.py migrate

To add some initial data you could install the fixtures from the dump json file from the development database:
    
    (venv)> python manage.py loaddata dummydata.json


You can start app now and check open it up on a browser:

    (venv)> python manage.py runserver

You can go to http://localhost:8000 on your browser and view app.

### External API Synching
For the API synching, Celery was adopted. And Redis was used as the message broker. Setup for redis is as follows for UNIX OS's:

    sudo apt update
    sudo apt install redis


### Starting Synching job
After setting up redis and the django project. You can start the synching job by opening 3 terminal windows, 
2 will have the virtualenv active<br />
On the one without an activated virtualenv run:

        > redis-server --port 6380

On the second window, ensure you are in the project root (where the manage.py file lives) start sending of 
the synch task with:

        (venv)>  python -m celery -A devscoop beat -l info

On the third window, ensure you are in project root directory, then spin up a worker with:

        (venv)> python -m celery -A devscoop worker -l info 


### List News Item and create new News Items locally
To view news items and create new News items locally go to: 

    http://localhost:8000/api/v1/news/item/all/

This news items in this api endpoint also contain url attribute that can be used to 
update or delete locally created news items.
