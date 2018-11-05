#!venv/bin/python2

import os

if __name__ == '__main__' and __package__ is None:
    os.sys.path.append(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NakshatraVeda.settings")

import django

django.setup()

from api.models import ItemType


def main():
    """
    This script will be used to create following records after database setup.
    """
    ItemType.objects.create(type="product").save()
    ItemType.objects.create(role_name="service").save()

main()
