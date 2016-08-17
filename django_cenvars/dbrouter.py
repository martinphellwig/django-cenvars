'''
Created on 11 Aug 2016

@author: martin
'''
from django.conf import settings
from .__info__ import LABELS

DEFAULT = 'default'

def get_db(model):
    "Return db depending on model"
    if isinstance(model, dict):
        if 'model' in model:
            model = model['model']
        else:
            return DEFAULT

    meta = getattr(model, '_meta')
    if meta.app_label == LABELS['name']:
        return settings.CENVARS_DATABASE
    else:
        return DEFAULT


# pylint: disable=no-self-use, unused-argument, invalid-name
class Cenvars(object):
    "Database router for cenvars"
    def db_for_read(self, model, **hints):
        """
        Which read
        """
        return get_db(model)

    def db_for_write(self, model, **hints):
        """
        Which write
        """
        return get_db(model)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations
        """
        return get_db(hints) == db

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations
        """
        return None



