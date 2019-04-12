from django.db import models

# Create your models here.
from django.db import models


class Description(models.Model):
    purchase_places = models.CharField(max_length=255)
    categories_prev_hierarchy = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    labels_hierarchy = models.CharField(max_length=255)
    quality_tags = models.IntegerField()
    manufacturing_places = models.CharField(max_length=255)
    brands_tags = models.CharField(max_length=255)
    origins = models.CharField(max_length=255)
    additives_prev_original_tags = models.CharField(max_length=255)
    stores_tags = models.CharField(max_length=255)
    emb_codes_tags = models.IntegerField()
    nova_group = models.IntegerField()
    serving_size = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "Description"
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=255)
    id_off = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return "{0} {1} {2}".format(self.name, self.id_off, self.url)

    class Meta:
        managed = True
        db_table = "Categories"
        ordering = ['id']


class Product(models.Model):
    image_url = models.CharField(max_length=255, default="Pics")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    nutrition_grade = models.IntegerField()
    ingredients = models.TextField()
    #description = models.OneToOneField(Description, on_delete=models.CASCADE, related_name="product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    class Meta:
        managed = True
        db_table = "Products"
        ordering = ['id']


class Substitution(models.Model):
    old_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="old_products")
    new_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="new_products")

    class Meta:
        managed = True
        db_table = "Substitutions"
        ordering = ['id']