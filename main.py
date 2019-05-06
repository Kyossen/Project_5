# usr/env/bin Python3.4
# coding:utf-8

"""
Import these modules for a good use of the program
Requests module for that the can program "requests to servers"
Django for requests handler between servers and code, database, etc...
And others modules such "os" for good use
"""
# Import lib
import os
import sys
import math

# Import module
import requests

# Import Django
import django
from django.core.paginator import Paginator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project_5.settings")
django.setup()

# Import file
from purebeurre.models import Category, Product, Description, Substitution


"""This function is the main for run the program and open choice to user"""


def main():
    while True:
        # Display the proposals of the user
        print('1 - Quel aliment souhaitez-vous remplacer ?''\n'
              '2 - Retrouvez vos aliments substitués.')
        x = input()

        # Create a input() for user choice a proposal and check inptu()
        if x == "1":
            choice_1()
        elif x == "2":
            choice_2()
        else:
            print('Vous devez choisir une proposition correct.''\n')


"""
Choice Product is the function that allow a user of choice
a product in list that generate with API OpenFoodFact
The product will are save in database with that description
"""


def choice_product(category):
    # Init has a counter
    a = 1

    # create a infinite loop
    while True:

        # Request to servers for take the data in API
        result = requests.get(category + "/" + str(a) + ".json")
        response = result.json()
        nb_page = math.ceil(response["count"] / response["page_size"])

        # Enumerate the data (products)
        for idx, product in enumerate(response['products']):
            nutrition_grades = ''
            if 'nutrition_grades' in product:
                nutrition_grades = product['nutrition_grades']
            print(idx + 1, product['product_name'], '\n'
                  "Nutrition grades: ", nutrition_grades, '\n')
        print("Page {} / {}".format(a, nb_page), '\n'
              "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
              "Appuyez sur <<P>> pour revenir à la page précédente. "'\n'
              "Appuyez sur <<R>> pour revenir à la sélection "
                                                 "des catégories. "'\n'
              "Appuyez sur <<M>> pour revenir au menu. "'\n')

        # Allow the user do a choice for continue to run and check user choice
        input_user = input()
        if input_user.lower() == "n" and a < nb_page:
            a += 1
        elif input_user.lower() == "p" and a > 1:
            a -= 1
        elif input_user.lower() == "m":
            return -1
        elif input_user.lower() == "r":
            return
        elif input_user.isdigit():
            x = int(input_user) - 1
            if 20 >= int(input_user) >= 1:
                pass
            else:
                print('Vous devez choisir une proposition correct.''\n')
                continue

            # Save product and that description in database
            categories = Category(name=response['products'][x]['product_name'],
                                  url=response['products'][x]['url'])
            categories.save()

            old_product_api = response['products'][x]
            description = description_product(old_product_api)

            old_product_db = Product(image_url=old_product_api['image_url'],
                                     name=old_product_api['product_name'],
                                     code=old_product_api['code'],
                                     nutrition_grade=old_product_api
                                     ['nutrition_grades'],
                                     ingredients=old_product_api
                                     ['ingredients_text_fr'],
                                     description=description,
                                     category=categories)

            if 'ingredients_text_fr' in \
                    old_product_api:
                old_product_db.ingredients = \
                    old_product_api['ingredients_text_fr']

            old_product_db.save()
            return_value = find_better_products(category, old_product_db)
            if return_value == -1:
                return -1
            return


"""
Find better product is the function that displays the bests
products selected by the program and offers it to the user.
It displays the choices one after the other if the user does not want precedent
"""


def find_better_products(category, old_product_db):
    # Init has a counter
    a = 1

    # create a infinite loop
    while True:

        # Request to servers for take the data in API
        result = requests.get(category + "/" + str(a) + ".json")
        response = result.json()

        # Enumerate the data (better products)
        for idx, product in enumerate(response['products']):
            if 'nutrition_grades' in product and \
                    product['nutrition_grades'] == 'a':
                print("Produit Substituable:" '\n' "Nom du produit:",
                      product['product_name'], '\n'
                      "Indice nutrionnel: ",
                      product['nutrition_grades'])
                print(""'\n'
                      'Appuyez sur <<N>> pour passer au produit suivant.', '\n'
                      'Appuyez sur <<Y>> pour sélectionner l\'aliment.')

                """Allow the user do a choice for continue
                to run and check user choice"""
                while True:
                    input_user = input()
                    if input_user.lower() == "n":
                        break
                    elif input_user.lower() == "y":
                        new_product_api = product
                        return_value = substitution_product(new_product_api,
                                                            old_product_db)
                        if return_value == -1:
                            return -1
                        return
                    else:
                        print('Vous devez choisir une proposition correct.'
                              '\n')
        a += 1


"""
The function below records the new product and its description
Then saving in the substitute table the choice of the user
which subsequently allows to find and display
the substituted products (old_product -> new_product)
"""


def substitution_product(new_product_api, old_product_db):

    print("Voulez-vous effectuer l'échange de votre "
          "ancien produit avec celui-ci ?"'\n'
          "Appuyez sur <<Y>> pour valider."'\n'
          ""'\n'
          "Appuyez sur <<R>> pour revenir à la sélection des catégories."
          "de séléction des catégories."'\n'
          "Appuyez sur <<M>> pour revenir au menu.")

    # Allow the user do a choice for continue to run and check user choice
    input_user = input()
    if input_user.lower() == "r":
        return
    elif input_user.lower() == "y":

        # Save product and that description in database
        categories = Category(name=new_product_api['product_name'],
                              url=new_product_api['url'])
        categories.save()

        description = description_product(new_product_api)

        new_product_db = Product(image_url=new_product_api['image_url'],
                                 name=new_product_api['product_name'],
                                 code=new_product_api['code'],
                                 nutrition_grade=new_product_api
                                 ['nutrition_grades'],
                                 ingredients=new_product_api
                                 ['ingredients_text_fr'],
                                 description=description,
                                 category=categories)

        if 'ingredients_text_fr' in new_product_api:
            new_product_db.ingredients = new_product_api['ingredients_text_fr']
        new_product_db.save()

        # Save the substitution in database
        substitution = Substitution(old_product=old_product_db,
                                    new_product=new_product_db)
        substitution.save()

    elif input_user.lower() == "m":
        return -1

    else:
        print('Vous devez choisir une proposition correct.''\n')

    """
    The product description function will save
    the product descriptions selected by the user in the database.
    It will save the old and the new product
    by checking some tags related to the API in which case it will
    create the missing tags with default values added.
    """


def description_product(description_to_product):
    if 'purchase_places' not in description_to_product:
        description_to_product['purchase_places'] = ''
    if 'nutrition_grades' not in description_to_product:
        description_to_product['nutrition_grades'] = ''
    if 'url' not in description_to_product:
        description_to_product['url'] = ''
    if 'countries' not in description_to_product:
        description_to_product['countries'] = ''
    if 'stores_tags' not in description_to_product:
        description_to_product['stores_tags'] = ''
    if 'ingredients_text_fr' not in description_to_product:
        description_to_product['ingredients_text_fr'] = ''

    print("Voici la description du produit séléctionné:"'\n'
          "Nom du produit:", description_to_product['product_name'], '\n'
          "Lien du produit :", description_to_product['url'], '\n'
          "Indice nutritionnel:",
          description_to_product['nutrition_grades'], '\n'
          "Manufacture du produit: ",
          description_to_product['purchase_places'], '\n'
          "Pays ou le produit est disponible: ",
          description_to_product['countries'], '\n'
          "Magasin avec ce produit disponible: ",
          description_to_product['stores_tags'], '\n'
          "PS: Sachez que des informations de types "
          "déscriptifs supplémentaires apparaîtrons dans votre "
          "base de données à chaque séléction d'un"
          "produit permettant une mise à jour automatique."'\n')

    description = Description()
    if 'store_tags' in description_to_product:
        description.stores_tags =\
            ','.join(description_to_product['stores_tags'])
    if 'purchase_places' in description_to_product:
        description.purchase_places = description_to_product['purchase_places']
    if 'product_quantity' in description_to_product:
        description.product_quantity =\
            description_to_product['product_quantity']
    if 'labels_hierarchy' in description_to_product:
        description.labels_hierarchy =\
            ','.join(description_to_product['labels_hierarchy'])
    if 'quality_tags' in description_to_product:
        description.quality_tags =\
            ','.join(description_to_product['quality_tags'])
    if 'manufacturing_places' in description_to_product:
        description.manufacturing_places =\
            description_to_product['manufacturing_places']
    if 'brands_tags' in description_to_product:
        description.brands_tags =\
            ','.join(description_to_product['brands_tags'])
    if 'origins' in description_to_product:
        description.origins = description_to_product['origins']
    if 'serving_size' in description_to_product:
        description.serving_size = description_to_product['serving_size']

    description.save()
    return description


"""
Choice 1 is the function proposed at the beginning
by the program to replace a product with a new product.
This function will search the API database for all categories and display them,
then the user will select a category then using the program it will be saved
to the confirmation of the selection of the substitution
"""


def choice_1():
    # Init has a counter
    a = 1
    i = 0

    # Request to API for a search in category
    result = requests.get("https://fr.openfoodfacts.org/categories.json")
    response = result.json()

    # Init a number pages
    nb_page = math.ceil(response["count"] / 10)

    # Init a number choice for user
    nb_choice = 1

    # create a infinite loop
    while True:

        # Create a loop for browse the categories of the API and display
        e = 0
        while e != 10:

            # Create column variable for that the display is better readable
            column1 = response["tags"][i]["products"],\
                      response["tags"][i]["url"]

            print(nb_choice, response["tags"][i]["name"])
            for c1 in zip(column1):
                print('{}'.format(*c1))
            nb_choice += 1
            if nb_choice > 10:
                nb_choice = 1

            # Make sure that the counter is correct
            i += 1
            e += 1

        print("Page {} / {}".format(a, nb_page), '\n'
              "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
              "Appuyez sur <<P>> pour revenir à la page précédente. "'\n'
              "Appuyez sur <<M>> pour revenir au menu. "'\n')

        # Allow the user do a choice for continue to run and check user choice
        input_user = input()
        if input_user.lower() == "n" and a < nb_page:
            a += 1
        elif input_user.lower() == "p" and a > 1:
            a -= 1
        elif input_user.lower() == "m":
            return -1
        elif input_user.isdigit() and 10 >= int(input_user) >= 1:
            real_index = (a - 1) * 10 + int(input_user) - 1
            print("Catégorie choisie: ",
                  response["tags"][real_index]["name"], '\n'
                  "URL de la catégorie: ",
                  response["tags"][real_index]["url"], '\n')
            return_value = choice_product(response
                                          ["tags"][real_index]["url"])
            if return_value == -1:
                return
            i -= 10

        else:
            print('Vous devez choisir une proposition correct.''\n')
            i -= 10


"""The function below will allow the user to see his substitutions
done and saved in database."""


def choice_2():
    # Create a object for all substitutions
    all_substituion = list(Substitution.objects.all())
    all_substituion_2 = Substitution.objects.all()

    # Create a pagination
    page = Paginator(all_substituion_2, 10)

    # Init has a counter
    i = 1

    # create a infinite loop
    while True:
        """Count the pages and display then
        create a loop for browse the substitutions and display"""
        for substitution in all_substituion:
            print("Voici vos produits substitués:" '\n'
                  "Categroie :", substitution.old_product.category, '\n',
                  substitution.old_product.name, "->",
                  substitution.new_product.name, '\n'
                  ""'\n'
                  "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
                  "Appuyez sur <<P>> pour revenir à la page précédente. "'\n'
                  "Appuyez sur <<M>> pour revenir au menu." '\n'
                  "Tapez <<Exit>> pour fermer le programme. ")
            print(page.page(i))

            """Allow the user do a choice
            for continue to run and check user choice"""
            input_user = input()
            if input_user.lower() == "n" and page.page(i).has_next() is True:
                i += 1
            elif input_user.lower() == "p" and\
                    page.page(i).has_previous() is True:
                i -= 1
            elif input_user.lower() == "m":
                return -1
            elif input_user.lower() == "exit":
                print("Merci d'avoir utilisé se programme." '\n'
                      "Bonne journée/Bonne soirée.")
                sys.exit()
            else:
                print('Il n\'y a pas de page suivante'
                      'ou de page précedente, merci.')


# Start point to execute this program
if __name__ == '__main__':
    main()
