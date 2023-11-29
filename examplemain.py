from graph import Graph
from dataparser import *


def read_stream(stream_data):
    listlen = len(stream_data.recipes)

    print("\n" + str(listlen) + " results\n")

    for i, recipe in enumerate(stream_data):
        if i != 0 and i % 10 == 0:
            cont = input("Enter NEXT or exit with any character >> ").upper()

            if cont != "NEXT":
                break

        print(recipe.recipe)


s_data, n_data = DataParser.format_pair()

print("Welcome to RecipePantry!")

graph = Graph(s_data)

print("\nFor a list of commands, type HELP")

opt = ""

stream = None

while opt != "end":
    opt_all = input(">> ").lower().split()

    opt = opt_all[0]

    if opt == "end":
        break
    elif opt == "help":
        print("\nSEARCH      start a new recipe search\n"
              "FILTER      filter the results from a search\n"
              "VIEW        view a recipe\n"
              "--------------------------------------------\n"
              "Command Modifiers\n"
              "KEYWORDS    search using keywords\n"
              "PHRASE      search using a phrase\n"
              "INGREDIENTS search by ingredient (append -s with SEARCH to require the exact ingredients)\n")
    elif opt == "view":
        res = n_data.recipe_search_exact(' '.join(opt_all[1:]))

        if not res:
            print("\nRecipe not found\n")
        else:
            recipe_data = res[0].as_list()
            print("\n" + recipe_data[0], "\n" + recipe_data[3], "\n-------------\nIngredients\n")
            for ing in recipe_data[1][1:-1].replace("'", "").split(', '):
                print(ing)
            print("\nDirections\n")
            for item in recipe_data[2]:
                print(item)
            print("\n")
    elif opt == "search":
        mod = opt_all[1]

        if mod == "keywords":
            stream = Stream(n_data.recipe_search_keywords(' '.join(opt_all[2:])))

            read_stream(stream)
        elif mod == "phrase":
            stream = Stream(n_data.recipe_search_phrase(' '.join(opt_all[2:])))

            read_stream(stream)
        elif mod == "ingredients":
            if opt_all[2] == "-s":
                stream = Stream(graph.find_recipes(opt_all[3:]))

                read_stream(stream)
            else:
                stream = Stream(n_data.recipe_search_ingredients(opt_all[2:]))

                read_stream(stream)
    elif opt == "filter":
        if stream is None:
            print("\nThere are no recipes in your list to filter through")
            continue

        mod = opt_all[1]

        if mod == "keywords":
            stream = stream.filter("keywords", ' '.join(opt_all[2:]))

            read_stream(stream)
        elif mod == "phrase":
            stream = stream.filter('phrase', ' '.join(opt_all[2:]))

            read_stream(stream)
        elif mod == "ingredients":
            stream = stream.filter('ingredients', opt_all[2:])

            read_stream(stream)
