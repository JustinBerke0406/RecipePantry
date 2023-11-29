from dataparser import DataParser

data = DataParser(False)

# These are the same
print(data.read_recipe_list_names(data.recipe_search_ingredients(["chocolate", "orange", "walnut"])))

print(data.read_recipe_list_names(
    data.stream() >> ("ingredients", [["chocolate", "walnut", "orange"]])
))

# Format: stream >> (search_type, [arg1, arg2, arg3,...])
# Or: stream.filter(search_type, arg1, arg2, arg3,...)

# Pipelines allow for the use of multiple filters
# This searches for spicy recipes that include chicken and at least one of beans or rice
print(data.read_recipe_list_names(
    data.stream() >> ("keywords", ["spicy"]) >> ("ingredients", [["chicken"]]) >> ("ingredients", [["beans", "rice"], 1, False])
))

# If the second parameter were true, then the search would give recipes with chicken and only one of beans or rice, but not both, as it requires 1 ingredient to be missing

# All search types:
# exact - finds an exact match given a name
# keywords - looks for keywords in a recipe's name
# phrase - looks for a substring in a recipe's name
# ingredients - looks for ingredients in a recipe

# Example: Print the ingredients to "ham summer squash gorgonzola over pasta"
print(data.recipe_search_exact("a bit different breakfast pizza")[0].ingredients)
# or
print((data.stream() >> ("exact", ["a bit different breakfast pizza"]))[0].ingredients)
# Note: exact should only return 1 recipe, so it's safe to get it from the first index

# Example: Find all recipes that include the phrase "ice cream" and include vanilla and only 2 of the following options: chocolate, caramel, cherries
print(data.read_recipe_list_names(
    data.stream() >> ("phrase", ["ice cream"]) >> ("ingredients", [["vanilla"]]) >> ("ingredients", [["chocolate", "caramel", "cherries"], 1, True])
))

# Can also do (I think this way is cleaner/less likely to bug, but I think both ways are useful so thats why I included both)
print(data.read_recipe_list_names(data.stream()
                                  .filter("phrase", "ice cream")
                                  .filter("ingredients", ["vanilla"])
                                  .filter("ingredients", ["chocolate", "caramel", "cherries"], 1, True)))
