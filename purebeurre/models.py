# usr/env/bin Python3.4
# coding:utf-8

"""
Import this module of the Django for create "model" to create database with the code below
"""

# Import Django
from django.db import models

""""
Description" class to create a description table in the Database
This table can handler of the descriptions to products
"""


class Description(models.Model):
    purchase_places = models.CharField(max_length=255, null=True, blank=True, default='')
    product_quantity = models.IntegerField(null=True, blank=True, default=None)
    labels_hierarchy = models.CharField(max_length=255, null=True, blank=True, default='')
    quality_tags = models.CharField(max_length=255, null=True, blank=True, default='')
    manufacturing_places = models.CharField(max_length=255, null=True, blank=True, default='')
    brands_tags = models.CharField(max_length=255, null=True, blank=True, default='')
    origins = models.CharField(max_length=255, null=True, blank=True, default='')
    stores_tags = models.CharField(max_length=255, null=True, blank=True, default='')
    serving_size = models.CharField(max_length=255, null=True, blank=True, default='')

    class Meta:
        managed = True
        db_table = "Description"
        ordering = ['id']


"""
"Category" to create a category table in the database
This table is manager of the category
This table allows of group all table in databse and manage of the categories in databse. 
This table allow as well of a user mange in program run
She regroup all categorie in API
"""


class Category(models.Model):
    name = models.CharField(max_length=255)
    id_off = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return "{0} {1}".format(self.name, self.url)

    class Meta:
        managed = True
        db_table = "Categories"
        ordering = ['id']


"""
"Product" class to create a product table in Database
This table can handler of the descriptions and data to products
Descriptions can be manipulated extensively since the link between "Description" and "Product"
"""
class Product(models.Model):
    image_url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    nutrition_grade = models.CharField(max_length=255)
    ingredients = models.TextField(default='')
    description = models.OneToOneField(Description, on_delete=models.CASCADE, related_name="product", default=None,
                                       null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    class Meta:
        managed = True
        db_table = "Products"
        ordering = ['id']


"""
"Substituion" class to create a substitution table in Database
This table allow print the substituions that the user do and of the saves in Database 
"""


class Substitution(models.Model):
    old_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="old_products")
    new_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="new_products")

    class Meta:
        managed = True
        db_table = "Substitutions"
        ordering = ['id']
