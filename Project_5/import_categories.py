import requests
import os
import sys
import django
from django.core.paginator import Paginator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project_5.settings")
django.setup()
from purebeurre.models import Category

result = requests.get("https://fr.openfoodfacts.org/categories.json")
response = result.json()

for search_category in response:
    i = 0
    for i in range(0, 13822):
        i += 1

        categories = Category(name=response["tags"][i]["name"], id_off=response["tags"][i]["products"],
                        url=response["tags"][i]["url"])
        categories.save()
        print("Name: ", response["tags"][i]["name"], '\n',
              "Url: ", response["tags"][i]["url"], '\n',
              )
