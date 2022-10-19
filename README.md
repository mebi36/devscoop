# devscoop
A Django-based news service based on the HackerNews API







### API Synching
For the API synching, Celery was adopted. And Redis was used as the message broker. Setup for redis is as follows for UNIX OS's:

    sudo apt update
    sudo apt install redis