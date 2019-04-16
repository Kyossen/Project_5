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
        print("Work")
        pass
    else:
        exit()


def choice_product(category):
    a = 1
    print("Catégorie choisie: ", category, '\n')
    while True:
        resultat = requests.get(category.url + "/" + str(a) + ".json")
        response = resultat.json()
        nb_page = math.ceil(response["count"] / response["page_size"])
        for idx, product in enumerate(response['products']):
            nutrition_grades = ''
            if 'nutrition_grades' in product:
                nutrition_grades = product['nutrition_grades']
            print(idx + 1, product['product_name'], '\n' "Nutrition grades: ",
                  nutrition_grades, '\n')
        print("Page {} / {}".format(a, nb_page), '\n'
                                                 "Appuyez sur <<N>> pour passer à la page suivante. "'\n'
                                                 "Appuyez sur <<P>> pour revenir à la page précédente. "'\n')
        input_user = input()
        if input_user == "n" and a < nb_page:
            a += 1
        elif input_user == "p" and a > 1:
            a -= 1
        elif input_user.isdigit():
            x = int(input_user) - 1
            if 'purchase_places' not in response['products'][x]:
                response['products'][x]['purchase_places'] = ''
            if 'nutrition_grades' not in response['products'][x]:
                response['products'][x]['nutrition_grades'] = ''
            if 'url' not in response['products'][x]:
                response['products'][x]['url'] = ''
            if 'countries' not in response['products'][x]:
                response['products'][x]['countries'] = ''
            if 'stores_tags' not in response['products'][x]:
                response['products'][x]['stores_tags'] = ''
            print("Voici la description du produit séléctionné:"'\n'
                  "Nom du produit:", response['products'][x]['product_name'], '\n'
                  "Lien du produit :", response['products'][x]['url'], '\n'
                  "Indice nutritionnel:", response['products'][x]['nutrition_grades'], '\n'
                  "Manufacture du produit: ", response['products'][x]['purchase_places'], '\n'
                  "Pays ou le produit est disponible: ", response['products'][x]['countries'], '\n'
                  "Magasin avec ce produit disponible: ", response['products'][x]['stores_tags'], '\n'
                                                                                      "PS: Sachez que des informations de types déscriptifs supplémentaires apparaîtrons dans votre "
                                                                                      "base de données à chaque séléction d'un produit permettant une mise à jour automatique."'\n')
            # Ouvrir la new fonction description
            product_old = response['products'][x]
            find_better_products(category, product_old)
            return


def find_better_products(category, product_old):
    a = 1
    while True:
        resultat = requests.get(category.url + "/" + str(a) + ".json")
        response = resultat.json()
        for idx, indice in enumerate(response['products']):
            if 'nutrition_grades' in indice and indice['nutrition_grades'] == 'a':
                print("Produit Subsituable:", indice['product_name'], '\n' "Indice nutrionnel: ",
                      indice['nutrition_grades'])
                print('Appuyez sur <<N>> pour passer au produit suivant.', '\n'
                      'Appuyez sur <<Y>> pour sélectionner l\'aliment.')
                input_user = input()
                if input_user == "n":
                    pass
                elif input_user == "y":
                    product_new = indice
                    subsitution_product(product_old, product_new, category)
                    return
        a += 1


def subsitution_product(product_old, product_new, category):
    description_product(product_new)
    if 'purchase_places' not in product_new:
        product_new['purchase_places'] = ''
    if 'nutrition_grades' not in product_new:
        product_new['nutrition_grades'] = ''
    if 'url' not in product_new:
        product_new['url'] = ''
    if 'countries' not in product_new:
        product_new['countries'] = ''
    if 'stores_tags' not in product_new:
        product_new['stores_tags'] = ''

    print("Voici la description du produit séléctionné:"'\n'
          "Nom du produit: ", product_new['product_name'], '\n'
           "Indice nutritionnel: ", product_new['nutrition_grades'],'\n'
          "Lien du produit: ", product_new['url'], '\n'
           "Manufacture du produit: ", product_new['purchase_places'], '\n'
          "Pays ou le produit est disponible: ",product_new['countries'], '\n'
          "Magasin avec ce produit disponible: ", product_new['stores_tags'], '\n'
          "PS: Sachez que des informations de types déscriptifs supplémentaires apparaîtrons dans votre "
          "base de données à chaque séléction d'un produit permettant une mise à jour automatique."'\n')

    description = Description()
    if 'store_tags' in product_new:
        description.stores_tags = ','.join(product_new['stores_tags'])
    if 'purchase_places' in product_new:
        description.purchase_places = product_new['purchase_places']
    if 'product_quantity' in product_new:
        description.product_quantity = product_new['product_quantity']
    if 'labels_hierarchy' in product_new:
        description.labels_hierarchy = ','.join(product_new['labels_hierarchy'])
    if 'quality_tags' in product_new:
        description.quality_tags = ','.join(product_new['quality_tags'])
    if 'manufacturing_places' in product_new:
        description.manufacturing_places = product_new['manufacturing_places']
    if 'brands_tags' in product_new:
        description.brands_tags = ','.join(product_new['brands_tags'])
    if 'origins' in product_new:
        description.origins = product_new['origins']
    if 'serving_size' in product_new:
        description.serving_size = product_new['serving_size']

    description.save()

    print("Voulez-vous effectuer l'échange de votre ancien produit avec celui-ci ?"'\n'
          "Appuyez sur <<Y>> pour valider"'\n'
          "Appuyez sur <<N>> pour revenir au menu de séléction des catégories")
    input_user = input()
    if input_user == "n":
        return
    elif input_user == "y":
        old_product = Product(image_url=product_old['image_url'], name=product_old['product_name'],
                              code=product_old['code'], nutrition_grade=product_old['nutrition_grades'],
                              ingredients=product_old['ingredients_text_fr'], category=category)
        if 'ingredients_text_fr' in product_old:
            old_product.ingredients = product_old['ingredients_text_fr']
        old_product.save()

        new_product = Product(image_url=product_new['image_url'], name=product_new['product_name'],
                              code=product_new['code'], nutrition_grade=product_new['nutrition_grades'],
                              ingredients=product_new['ingredients_text_fr'], category=category)
        if 'ingredients_text_fr' in product_new:
            new_product.ingredients = product_new['ingredients_text_fr']
        new_product.save()

        subsitution = Substitution(old_product=old_product, new_product=new_product)
        subsitution.save()



def description_product(description):
    pass

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
                            "Appuyez sur <<P>> pour revenir à la page précédente. "'\n')
        input_user = input()

        if input_user == "n" and page.page(i).has_next() is True:
            i += 1
        elif input_user == "p" and page.page(i).has_previous() is True:
            i -= 1
        elif input_user.isdigit():
            choice_product(categories[int(input_user) - 1])


if __name__ == '__main__':
    main()

#Description ancien produit
#Description lié à un produit
#Choice_2, listez les substitutions

            product_old = response['products'][x]  # ['product_name']
            find_better_products(category, product_old)


def find_better_products(category, product_old):
    a = 1
    x = 1
    print('Produit Subsituable: ')
    while True:
        resultat = requests.get(category.url + "/" + str(a) + ".json")
        response = resultat.json()
        for idx, indice in enumerate(response['products']):
            idx = 0
            if indice['nutrition_grades_tags'] == ['a']:
                print(idx + x, indice['product_name'], '\n' "Indice nutrionnel: ",
                      indice['nutrition_grades_tags'])
                print('Appuyez sur <<N>> pour passer au produit suivant.')
                x += 1
                input_user = input()
                if input_user == "n":
                    pass
                elif input_user.isdigit():
                    product_new = indice
                    subsitution_product(product_old, product_new, category)
            else:
                a += 1


# Corriger le bug selction chiffre


def subsitution_product(product_old, product_new, category):
    print("Voici la description du produit séléctionné:"'\n',
          "Nom du produit: ", product_new['product_name'], '\n',
          "Indice nutritionnel: ", product_new['nutrition_grades_tags'], '\n',
          "Lien du produit: ", product_new['url'], '\n',
          "Manufacture du produit: ", product_new['purchase_places'], '\n',
          "Pays ou le produit est disponible: ", product_new['countries'], '\n',
          "Magasin avec ce produit disponible: ", product_new['stores_tags'], '\n'
                                                                              "PS: Sachez que des informations de types déscriptifs supplémentaires apparaîtrons dans votre "
                                                                              "base de données à chaque séléction d'un produit permettant une mise à jour automatique."'\n')
    description = Description(purchase_places=product_new['purchase_places'],
                              # categories_prev_hierarchy=product_new['categories_prev_hierarchy'],
                              product_quantity=product_new['product_quantity'],
                              labels_hierarchy=product_new['labels_hierarchy'],
                              quality_tags=product_new['quality_tags'],
                              manufacturing_places=product_new['manufacturing_places'],
                              brands_tags=product_new['brands_tags'],
                              origins=product_new['origins'],
                              additives_prev_original_tags=product_new['additives_prev_original_tags'],
                              stores_tags=product_new['stores_tags'], emb_codes_tags=product_new['emb_codes_tags'],
                              nova_group=product_new['nova_group'], serving_size=product_new['serving_size'])
    # description.save
    print("Voulez-vous effectuer l'échange de votre ancien produit avec celui-ci ?"'\n'
          "Appuyez sur <<Y>> pour valider"'\n'
          "Appuyez sur <<N>> pour revenir au menu de séléction des catégories")
    input_user = input()
    if input_user == "n":
        choice_1()
    elif input_user == "y":
        old_product = Product(image_url=product_old['image_url'], name=product_old['product_name'],
                              code=product_old['code'], nutrition_grade=product_old['nutrition_grades_tags'],
                              ingredients=product_old['ingredients_text_fr'], category=category)
       # old_product.save()

        new_product = Product(image_url=product_new['image_url'], name=product_new['product_name'],
                              code=product_new['code'], nutrition_grade=product_new['nutrition_grades_tags'],
                              ingredients=product_new['ingredients_text_fr'], category=category)
        # new_product.save()

        subsitution = Substitution(old_product=old_product, new_product=new_product)
        # subsitution.save()
        print(subsitution)


# Corriger le bug de save


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
                            "Appuyez sur <<P>> pour revenir à la page précédente. "'\n')
        input_user = input()

        if input_user == "n" and page.page(i).has_next() is True:
            i += 1
        elif input_user == "p" and page.page(i).has_previous() is True:
            i -= 1
        elif input_user.isdigit():
            choice_product(categories[int(input_user) - 1])


if __name__ == '__main__':
    main()

# Afficher sur deux colonnes
# Classe product avec save de substitution
