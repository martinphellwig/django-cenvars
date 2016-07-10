"""
Then main unit tests.
"""
import os
if __name__ == '__main__':
    import django
    from django.core.management import call_command
    django.setup()

from django.conf import settings
from django.test import TestCase
from django_cenvars import models
from django_cenvars.management.commands import envar_newkey

from django_cenvars.tools import codec

settings.RSA_KEYSIZE = 512 # For testing purposes, make it a bit faster.
settings.SERVER_KEY = envar_newkey.create()

# pylint: disable=no-member
class TestMain(TestCase):
    "Main testing."
    def _create_data(self):
        "Create some data"
        environ_1 = models.Environment.objects.create(label='test 1')
        environ_2 = models.Environment.objects.create(label='test 2')
        key_one = models.Key.objects.create(key='One')
        key_two = models.Key.objects.create(key='Two')
        models.Inheritance.objects.create(offspring=environ_2,
                                          ascendant=environ_1)
        models.Variable.objects.create(environment=environ_1, key=key_one,
                                       value='value_1')
        models.Variable.objects.create(environment=environ_2, key=key_two,
                                       value='value_2')
        self.assertTrue(environ_1.id is not None)

    def test_001_smoke(self):
        "models.environment"
        environ = models.Environment.objects.create(label='test')
        self.assertTrue(environ.envar is not None)
        data = os.environ.copy()
        _, rsa_key = codec.decode_key(environ.envar)
        encrypted = codec.encrypt(rsa_key, data)
        decrypted = codec.decrypt(rsa_key, encrypted)
        self.assertEqual(data, decrypted)

    def test_002_inheritance(self):
        "Test the inheritance"
        ev1 = models.Environment.objects.create(label='ev1')
        ev2 = models.Environment.objects.create(label='ev2')
        ev3 = models.Environment.objects.create(label='ev3')
        ev4 = models.Environment.objects.create(label='ev4')
        models.Inheritance.objects.create(offspring=ev1, ascendant=ev2)
        models.Inheritance.objects.create(offspring=ev2, ascendant=ev3)
        models.Inheritance.objects.create(offspring=ev3, ascendant=ev4)
        # Add a recursion in it
        models.Inheritance.objects.create(offspring=ev4, ascendant=ev1)

        expected = [ev1, ev2, ev3, ev4]
        expected = [str(item) for item in expected]
        returned = ev1.resolve_inheritance()
        returned = [str(item) for item in returned]

        self.assertEqual(expected, returned)


if __name__ == '__main__':
    call_command('test')

