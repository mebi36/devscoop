"""Setup for Celery.

We will pass off the period api fetch to Celery.

"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devscoop.settings")
app = Celery("devscoop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def api_call(self):
    from devscoop import server_job

    server_job.api_call()
