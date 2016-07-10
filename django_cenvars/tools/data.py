'''
Created on 4 Jul 2016

@author: martin
'''
import json
from io import StringIO
from django.core.management import call_command
from django.conf import settings
from ..__info__ import LABELS

TYPES = ['INSERT', 'UPDATE', 'DELETE', 'SELECT']

def add(instance, operation):
    tmp = {'model':None, # The database model of the change
           'action':None, # The operation performed
           'id':None, # The instance (None when insert)
           'data':{} #
           }
    


def db_get():
    "get all the data from the database."
    text = StringIO()
    call_command('dumpdata', LABELS['name'], stdout=text)
    items = json.loads(text.getvalue())
    for item in items:
        item['action'] = 'dump'
        item = json.dumps(item)
        
        print(item)
        yield item
            

    