import csv


# Split a recipe name into a list of words
def recipe_words(recipe_name):
    return recipe_name.lower().split()


# Format a name correctly
def format_recipe_name(recipe_name):
    return ' '.join(recipe_words(recipe_name))


class RecipeData:
    def __init__(self, recipe, ingredients, steps, desc):
        self.recipe_words = recipe_words(recipe)
        self.recipe = ' '.join(self.recipe_words)
        self.ingredients = ingredients
        self.steps = steps
        self.desc = desc

    def as_list(self):
        return [self.recipe, self.ingredients, self.steps, self.desc]


class SearchFunctions:
    # Returns row of recipe
    @staticmethod
    def exact(recipes, recipe_name):
        recipe = format_recipe_name(recipe_name)

        try:
            return [datapoint for datapoint in recipes if (datapoint.recipe == recipe)]
        except IndexError:
            return []

    # Returns rows of recipes containing the given keywords
    @staticmethod
    def keywords(recipes, word_string):
        recipe = recipe_words(word_string)

        try:
            return [datapoint for datapoint in recipes if all(x in datapoint.recipe_words for x in recipe)]
        except IndexError:
            return []

    # Returns rows of recipes containing the given substring
    @staticmethod
    def phrase(recipes, phrase):
        recipe = format_recipe_name(phrase)

        try:
            return [datapoint for datapoint in recipes if recipe in datapoint.recipe]
        except IndexError:
            return []

    # Returns rows of recipes containing the ingredients list
    # The miss parameter is the number of missing ingredients
    # The exact parameter is if the recipe must miss some number of ingredients rather than a max
    @staticmethod
    def ingredients(recipes, ingredients, miss=0, exact=False):
        result = []

        for recipe in recipes:
            miss_counter = 0
            append = True
            for ingredient in ingredients:
                if ingredient not in recipe.ingredients:
                    miss_counter += 1
                    if miss_counter > miss:
                        append = False
                        break
            if append and (not exact or (miss == miss_counter)):
                result.append(recipe)

        return result

    search_functions = {
        "exact": exact,
        "keywords": keywords,
        "phrase": phrase,
        "ingredients": ingredients
    }


class Stream:
    def __init__(self, recipes):
        self.recipes = recipes
        self._counter = -1

    def __getitem__(self, key):
        return self.recipes[key]

    def __rshift__(self, packet):
        return self.filter(packet[0], *packet[1])

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self._counter += 1
            return self.recipes[self._counter]
        except IndexError:
            self._counter = -1
            raise StopIteration

    def filter(self, search_function, *args):
        self.recipes = SearchFunctions.search_functions[search_function](self.recipes, *args)
        return self


class DataParser:
    filename = "RAW_recipes.csv"

    def __init__(self, strict, recipe_list = None):
        self.recipes = []

        if recipe_list is None:
            self._read(strict)
        else:
            self.recipes = recipe_list

    def _read(self, strict):
        with open(DataParser.filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)

            next(reader)

            # Get rows
            if strict:
                for row in reader:
                    self.recipes.append(RecipeData(row[0], row[10][1:-1].replace("'", "").split(', '), row[8][1:-1].replace("'", "").split(', '), row[9]))
            else:
                for row in reader:
                    self.recipes.append(RecipeData(row[0], row[10], row[8][1:-1].replace("'", "").split(', '), row[9]))

    def recipe_search_exact(self, recipe_name):
        return SearchFunctions.exact(self.recipes, recipe_name)

    def recipe_search_keywords(self, word_string):
        return SearchFunctions.keywords(self.recipes, word_string)

    def recipe_search_phrase(self, phrase):
        return SearchFunctions.phrase(self.recipes, phrase)

    def recipe_search_ingredients(self, ingredients, miss=0, exact=False):
        return SearchFunctions.ingredients(self.recipes, ingredients, miss, exact)

    # Gets all recipes as a Stream
    def stream(self):
        return Stream(self.recipes)

    # Turns list of recipes into usable data
    @staticmethod
    def read_recipe_list_data(recipes):
        return [recipe.as_list() for recipe in recipes]

    # Turns list of recipes into a list of recipe names
    @staticmethod
    def read_recipe_list_names(recipes):
        return [recipe.recipe for recipe in recipes]
