# -*- coding: utf-8 -*-

import os

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'evedemo')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
DEBUG = True


RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

X_DOMAINS = "*"

phones = {
    'item_title': 'phone',

    'schema': {
        'phone': { 'type': 'string' },
        'work_address': { 'type': 'string' },
        'work_address_geo': { 'type': 'point' },
        'home_address': { 'type': 'string' },
        'home_address_geo': { 'type': 'point' }
    }
}

routes = {
    'item_title': 'routes',

    'schema': {
        'phone': { 'type': 'string' },
        'location': { 'type': 'point' },
    }
}

DOMAIN = {
    'phones': phones,
    'routes': routes
}
