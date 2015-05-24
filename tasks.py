from celery import Celery
from celery.decorators import periodic_task
from celery.schedules import crontab
import datetime
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

LAST_INCIDENT = datetime.datetime.utcnow().isoformat()

@periodic_task(run_every=crontab(hour='*', minute="*/2", day_of_week="*"))
def crawl_hi_traffic():
    LAST_INCIDENT = datetime.datetime.utcnow().isoformat()
    headers = {'Content-Type': 'application/json'}
    route_endpoint = 'http://api.hitraffic.org/v1/incidents?from=' + LAST_INCIDENT
    logger.info(route_endpoint)
    incidents = requests.get(route_endpoint, headers=headers).json()
    LAST_INCIDENT = datetime.datetime.utcnow().isoformat()
    notify_numbers = {}
    for incident in incidents:
        try:
            if incident != LAST_INCIDENT:
                if 'MOTOR VEHICLE' in incident["type"]:
                    if incident['geometry']:
                        latitude = incident['geometry']['latitude']
                        longitude = incident['geometry']['longitude']
                        if latitude and longitude:
                            endpoint = 'http://127.0.0.1:5000/routes?where={"location": {"$near": {"$geometry": {"type":"Point", "coordinates": [' + str(longitude) + ',' + str(latitude) + ']}, "$maxDistance": 10000}}}'
                            response = requests.get(endpoint, headers=headers)
                            affected = response.json()
                            for a in affected["_items"]:
                                if a["phone"] in notify_numbers:
                                    notify_numbers[a["phone"]].push(incident)
                                else:
                                    notify_numbers[a["phone"]] = [incident]
        except Exception as e:
            pass

    if notify_numbers:
        for k,v in notify_numbers.iteritems():
            logger.info(notify_numbers[k])
