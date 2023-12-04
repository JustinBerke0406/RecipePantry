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