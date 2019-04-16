import requests
import math
import os
import sys
import django
from django.core.paginator import Paginator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project_5.settings")
django.setup()
from purebeurre.models import Category, Product, Description, Substitution


def main():
    a = print('1 - Quel aliment souhaitez-vous remplacer ?')
    b = print('2 - Retrouvez vos aliments substitués.')
    x = input()

    if x == "1":
        choice_1()
    elif x == "2":
        choice_2()
        pass
    else:
        print('Vous devez choisir une proposition correct.')
        main()


def choice_product(category):
    a = 1
    print("Catégorie choisie: ", category, '\n')
    while True:
        result = requests.get(category.url + "/" + str(a) + ".json")
        response = result.json()
        nb_page = math.ceil(response["count"] / response["page_size"])
        for idx, product in enumerate(response['products']):
            nutrition_grades = ''
            if 'nutrition_grades' in product:
                nutrition_grades = product['nutrition_grades']
            print(idx + 1, product['product_name'], '\n' 
                 "Nutrition grades: ", nutrition_grades, '\n')
        print("Page {} / {}".format(a, nb_page), '\n'
              "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
              "Appuyez sur <<P>> pour revenir à la page précédente. "'\n'
              "Appuyez sur <<M>> pour revenir au menu. "'\n')

        input_user = input()
        if (input_user == "n") or (input_user == "N") and a < nb_page:
            a += 1
        elif (input_user == "p") or (input_user == "P") and a > 1:
            a -= 1
        elif (input_user == "m") or (input_user == "M"):
            main()
        elif input_user.isdigit():
            x = int(input_user) - 1
            if 20 >= int(input_user) >= 1:
                pass
            else:
                print('Vous devez choisir une proposition correct.')
                break

            old_product_api = response['products'][x]
            description_product(old_product_api)

            old_product_db = Product(image_url=old_product_api['image_url'],
                                     name=old_product_api['product_name'],
                                     code=old_product_api['code'],
                                     nutrition_grade=old_product_api['nutrition_grades'],
                                     ingredients=old_product_api['ingredients_text_fr'],
                                     category=category)

            if 'ingredients_text_fr' in old_product_api:
                old_product_db.ingredients = old_product_api['ingredients_text_fr']

            old_product_db.save()
            find_better_products(category, old_product_db)
            return


        else:
            print('Vous devez choisir une proposition correct.')


def find_better_products(category, old_product_db):
    a = 1
    while True:
        result = requests.get(category.url + "/" + str(a) + ".json")
        response = result.json()
        for idx, product in enumerate(response['products']):
            if 'nutrition_grades' in product and product['nutrition_grades'] == 'a':
                print("Produit Subsituable:" '\n' "Nom du produit:", product['product_name'], '\n' 
                      "Indice nutrionnel: ", product['nutrition_grades'])
                print('Appuyez sur <<N>> pour passer au produit suivant.', '\n'
                      'Appuyez sur <<Y>> pour sélectionner l\'aliment.')

                input_user = input()
                if (input_user == "n") or (input_user == "N"):
                    pass
                elif (input_user == "y") or (input_user == "Y"):
                    new_product_api = product
                    subsitution_product(new_product_api, category, old_product_db)
                    return
                else:
                    print('Vous devez choisir une proposition correct.')
        a += 1


def subsitution_product(new_product_api, category, old_product_db):
    description_product(new_product_api)
    print("Voulez-vous effectuer l'échange de votre ancien produit avec celui-ci ?"'\n'
          "Appuyez sur <<Y>> pour valider."'\n'
          "Appuyez sur <<N>> pour revenir au menu de séléction des catégories."'\n'
          "Appuyez sur <<M>> pour revenir au menu.")

    input_user = input()
    if (input_user == "n") or (input_user == "N"):
        return
    elif (input_user == "y") or (input_user == "Y"):

        new_product_db = Product(image_url=new_product_api['image_url'],
                                 name=new_product_api['product_name'],
                                 code=new_product_api['code'],
                                 nutrition_grade=new_product_api['nutrition_grades'],
                                 ingredients=new_product_api['ingredients_text_fr'],
                                 category=category)

        if 'ingredients_text_fr' in new_product_api:
            new_product_db.ingredients = new_product_api['ingredients_text_fr']
        new_product_db.save()

        subsitution = Substitution(old_product=old_product_db, new_product=new_product_db)
        subsitution.save()

    elif (input_user == "m") or (input_user == "M"):
        main()

    else:
        print('Vous devez choisir une proposition correct.')


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
          "Lien du produit :", description_to_product['url'],          '\n'
          "Indice nutritionnel:", description_to_product['nutrition_grades'], '\n'
          "Manufacture du produit: ", description_to_product['purchase_places'], '\n'
          "Pays ou le produit est disponible: ", description_to_product['countries'], '\n'
          "Magasin avec ce produit disponible: ", description_to_product['stores_tags'], '\n'
          "PS: Sachez que des informations de types déscriptifs supplémentaires apparaîtrons dans votre "
          "base de données à chaque séléction d'un produit permettant une mise à jour automatique."'\n')

    description = Description()
    if 'store_tags' in description_to_product:
        description.stores_tags = ','.join(description_to_product['stores_tags'])
    if 'purchase_places' in description_to_product:
        description.purchase_places = description_to_product['purchase_places']
    if 'product_quantity' in description_to_product:
        description.product_quantity = description_to_product['product_quantity']
    if 'labels_hierarchy' in description_to_product:
        description.labels_hierarchy = ','.join(description_to_product['labels_hierarchy'])
    if 'quality_tags' in description_to_product:
        description.quality_tags = ','.join(description_to_product['quality_tags'])
    if 'manufacturing_places' in description_to_product:
        description.manufacturing_places = description_to_product['manufacturing_places']
    if 'brands_tags' in description_to_product:
        description.brands_tags = ','.join(description_to_product['brands_tags'])
    if 'origins' in description_to_product:
        description.origins = description_to_product['origins']
    if 'serving_size' in description_to_product:
        description.serving_size = description_to_product['serving_size']

    description.save()


def choice_1():
    AllCategory = Category.objects.all()
    page = Paginator(AllCategory, 10)
    i = 1
    while True:
        categories = page.page(i)
        for idx, categorie in enumerate(categories):
            print(idx + 1, categorie, '\n')
        print(page.page(i), '\n'
              "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
              "Appuyez sur <<P>> pour revenir à la page précédente. "'\n'
              "Appuyez sur <<M>> pour revenir au menu. "'\n')

        input_user = input()
        if (input_user == "n") or (input_user == "N") and page.page(i).has_next() is True:
            i += 1
        elif (input_user == "p") or (input_user == "P") and page.page(i).has_previous() is True:
            i -= 1
        elif (input_user == "m") or (input_user == "M"):
            main()
        elif input_user.isdigit():
            if 10 >= int(input_user) >= 1:
                choice_product(categories[int(input_user) - 1])
            else:
                print('Vous devez choisir une proposition correct.')
        else:
            print('Vous devez choisir une proposition correct.')


def choice_2():
    AllSubstituion = list(Substitution.objects.all())
    for substitution in AllSubstituion:
        print("Voici vos produits substitués:" '\n'
              "Categroie :", substitution.old_product.category,'\n',
              substitution.old_product.name, "->", substitution.new_product.name, '\n'
              ""'\n'
              "Appuyez sur <<M>> pour revenir au menu." '\n'
              "Tapez <<Exit>> pour fermer le programme. ")

    input_user = input()
    if (input_user == "m") or (input_user == "M"):
        main()
    elif (input_user == "exit") or (input_user == "Exit"):
        print("Merci d'avoir utilisé se programme." '\n'
              "Bonne journée/Bonne soirée.")
        sys.exit()
    else:
        print('Vous devez choisir une proposition correct.')
        main()


if __name__ == '__main__':
    main()

# Description lié à un produit
