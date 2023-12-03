from tkinter import *
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as ttkb
from graph import Graph
from dataparser_extra import *

# Colors
# Default, primary, secondary, success, info, warning, danger, light, dark


# update list box
def update(ingredients_in_list):
    # clear the list box
    my_list_ingredients.delete(0, END)
    # add toppings to list box
    for item in ingredients_in_list:
        my_list_ingredients.insert(END, item)


# update input box
def update_recipes(recipes):
    # clear the list box
    my_list_recipes.delete(0, END)
    if not recipes:
        my_list_recipes.insert(0, "No Recipes Found")
    for recipe in recipes:
        my_list_recipes.insert(0, recipe.recipe)


# update entry box with listbox clicked
def fillout(e):
    # delete what is in entry box
    my_entry.delete(0, END)
    # add clicked list item to entry box
    curs_location = my_list_ingredients.curselection()
    if curs_location:
        selected_item = my_list_ingredients.get(curs_location)
        my_entry.insert(0, selected_item)


# update entry box with listbox clicked
def fillout_input(e):
    # delete what is in entry box
    my_entry.delete(0, END)
    # add clicked list item to entry box
    curs_location = my_list_input.curselection()
    if curs_location:
        selected_item = my_list_input.get(curs_location)
        my_entry.insert(0, selected_item)


# update entry box with listbox clicked
def show_recipe(e):
    recipe_box = Messagebox


# create function to check entry vs. list box
def check(e):
    # grab what was typed
    typed = my_entry.get()
    # typed_length = len(typed)
    new_list = list(ingredients)
    if typed == '':
        data = new_list
    else:
        data = []
        for ingredient in new_list:
            if typed.lower() in ingredient.lower():
                # if typed.lower() in ingredient.lower()[0:typed_length]:
                data.append(ingredient)
    update(data)


def add_input():
    # Get the content of the entry
    input_text = my_entry.get()
    # typed_length = len(typed)
    ingredients_data = list(ingredients)
    if input_text.lower() in ingredients_data:
        if input_text.lower() not in my_list_input.get(0, END):
            my_list_input.insert(0, input_text)


def remove_input():
    # Get the content of the entry
    input_text = my_entry.get()
    # typed_length = len(typed)
    ingredients_data = list(ingredients)
    if input_text.lower() in ingredients_data:
        if input_text.lower() in my_list_input.get(0, END):
            idx = my_list_input.get(0, ttkb.END).index(input_text)
            my_list_input.delete(idx)


def find_recipies():
    # typed_length = len(typed)
    data = []
    for ingredient in my_list_input.get(0, END):
        data.append(ingredient)
    recipe_list = graph.find_recipes(data)
    for recipe in recipe_list:
        print(recipe.recipe)
    update_recipes(recipe_list)


root = ttkb.Window(themename="superhero")
root.title("Recipe Pantry")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size as a fraction of the screen size
window_width = int(screen_width * 0.65)
window_height = int(window_width * 0.8)

root.iconbitmap('images/favicon.ico')
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

graph = Graph()

ingredients = graph.nodes.keys()

my_frame = ttkb.Frame(root, bootstyle="light")
my_frame.place(x=0, y=0)

# Create a button to add ingredient
add_button = ttkb.Button(root, text="Add Ingredient", command=add_input)
add_button.place(relx=.56, rely=.15, anchor=ttkb.CENTER)

# Create a button to remove ingredient
remove_button = ttkb.Button(root, text="Remove Ingredient", command=remove_input)
remove_button.place(relx=.685, rely=.15, anchor=ttkb.CENTER)

# Create a button to find recipes
remove_button = ttkb.Button(root, text="Find Recipes", command=find_recipies)
remove_button.place(relx=.925, rely=.15, anchor=ttkb.CENTER)

# create a label for project name
my_label = Label(root, text="Recipe Pantry", font=("helvetica", 28), fg="grey")
my_label.place(relx=.5, rely=.05, anchor=ttkb.CENTER)

# create a label for "Search"
my_label = Label(root, text="Search Pantry:", font=("helvetica", 14), fg="grey")
my_label.place(relx=.09, rely=.15, anchor=ttkb.CENTER)

# create an entry box
my_entry = Entry(root, font=("helvetica", 20), relief=SUNKEN)
my_entry.place(relx=.33, rely=.15, anchor=ttkb.CENTER)

# create an ingredient list box
my_list_ingredients = Listbox(root, width=40, font=("helvetica", 14))
my_list_ingredients.place(relx=.26, rely=.35, anchor=ttkb.CENTER)

# create an input list box
my_list_input = Listbox(root, width=40, font=("helvetica", 14))
my_list_input.place(relx=.74, rely=.35, anchor=ttkb.CENTER)

# create a recipe list box
my_list_recipes = Listbox(root, width=60, font=("helvetica", 20))
my_list_recipes.place(relx=.5, rely=.75, anchor=ttkb.CENTER)

# Create combo box
structures = ["Graph", "Tree"]
my_comboBox = ttkb.Combobox(root, bootstyle="success", values=structures)
my_comboBox.pack(pady=10)

# Set combo default
my_comboBox.current(0)

# create a list of ingredients
ingredients_list = list(ingredients)

# add ingredients to list
update(ingredients_list)

# create binding on list box on click
my_list_ingredients.bind("<<ListboxSelect>>", fillout)

# create binding on list box on click
my_list_input.bind("<<ListboxSelect>>", fillout_input)

# create binding on list box on click
my_list_recipes.bind("<<ListboxSelect>>", show_recipe)

# create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

root.mainloop()
