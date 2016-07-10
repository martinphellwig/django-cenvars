"""
Envar models.
"""
import json
import random
import hashlib
import base64
import rsa
from django.db import models
from django.conf import settings
from ..tools import codec

def is_empty(value):
    "Test if value is empty."
    if value is None or len(value) == 0:
        return True
    return False


# pylint:disable=no-member
class Environment(models.Model): # pylint: disable=too-many-instance-attributes
    "A single environment instance."
    label = models.CharField(max_length=64, default='', blank=True)
    store = models.URLField(blank=True)
    ident = models.CharField(max_length=56, unique=True, blank=True)
    envar = models.TextField(blank=True)

    def __str__(self):
        return self.ident + ' | ' + self.label

    def save(self, *args, **kwargs):
        "override save."
        if is_empty(self.store):
            self.store = settings.DEFAULT_SERVER

        if is_empty(self.envar):
            _, key = rsa.newkeys(settings.RSA_KEYSIZE)
            self.ident, self.envar = codec.encode_key(key, self.store)

        return models.Model.save(self, *args, **kwargs)

    def resolve_inheritance(self):
        "Resolve inheritance, break if there is a recursion."
        # First get a line of inheritance
        inheritance = list()
        workon = self
        while True:
            inheritance.append(workon)

            if not hasattr(workon, 'offspring'):
                break

            workon = workon.offspring.ascendant
            if workon in inheritance:
                break

        return inheritance
            
                
        


class Key(models.Model):
    "Key, well it is a key."
    key = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.key


class Variable(models.Model):
    "The variable."
    environment = models.ForeignKey(Environment)
    key = models.ForeignKey(Key)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        _ = self.environment.label + ' | ' + self.key.key + ' | ' + self.value
        return  _


class Inheritance(models.Model):
    "Inheritance of Environments."
    # No multiple inheritance, offspring can only have one parent (ascendant).
    offspring = models.OneToOneField(Environment, related_name='offspring')
    ascendant = models.ForeignKey(Environment, related_name='ascendant')

    def __str__(self):
        return self.offspring.label + '<' + self.ascendant.label

