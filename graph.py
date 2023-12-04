from dataparser_extra import RecipeData
from collections import defaultdict
import threading
import csv


class Graph:
    def __init__(self):
        self.thread = threading.Thread(target=self._make_graph, daemon=True)

        self.nodes = defaultdict(dict)

        self.thread.start()

    def _make_graph(self):
        with open("RAW_recipes.csv", 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                recipe = RecipeData(row[0], row[10][1:-1].replace("'", "").split(', '), row[8][1:-1].replace("'", "").split(', '), row[9])
                ingredients = recipe.ingredients
                for ingredient in ingredients:
                    remaining = ingredients[:]
                    remaining.remove(ingredient)
                    for ingredient_to in remaining:
                        self.nodes[ingredient].setdefault(ingredient_to, set()).add(recipe)

    def all_recipes_with(self, ingredient):
        links = self.nodes[ingredient]

        union = set()

        for item in links.items():
            union |= item[1]

        return union

    # Recipes that contain the given ingredients
    def find_recipes(self, ingredients, exclude=[]):
        if not ingredients:
            return []

        links = self.nodes[ingredients[0]]

        recipes = self.all_recipes_with(ingredients[0])

        for ingredient in ingredients[1:]:
            if ingredient in links:
                recipes &= links[ingredient]
            else:
                return []

        for item in exclude:
            intersection = self.nodes[item].keys() & ingredients
            for inter in intersection:
                recipes -= self.nodes[item][inter]

        return list(recipes)
