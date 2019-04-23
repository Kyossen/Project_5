# usr/env/bin Python3.4
# coding:utf-8


"""
Import these modules for a good use of the program
Requests module for that the can program "requests to servers"
Django for requests handler between servers and code, database, etc...
And The module "os" for good use
"""

# Import lib
import os

# Import module
import requests

# Import Django
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project_5.settings")
django.setup()

# Import file
from purebeurre.models import Category

"""This code is for save in database the totality
of the categories in API to use program correctly"""
result = requests.get("https://fr.openfoodfacts.org/categories.json")
response = result.json()

for search_category in response:
    i = 0
    for i in range(0, 13822):
        i += 1

        categories = Category(name=response["tags"][i]["name"],
                              id_off=response["tags"][i]["products"],
                              url=response["tags"][i]["url"])
        categories.save()
        print("Name: ", response["tags"][i]["name"], '\n',
              "Url: ", response["tags"][i]["url"], '\n',
              )
