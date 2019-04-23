# usr/env/bin Python3.4
# coding:utf-8

"""
Import these modules for a good use of the program
"""

# Import lib
import os
import sys

"""The code below is base code,
he not need is touch except to add the settings file"""
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_5.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
