from tkinter import *
from ttkbootstrap.constants import *
from splaytree import *
from ttkbootstrap import ScrolledText
import ttkbootstrap as ttkb
from graph import Graph

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
def fillout_exclude(e):
    # delete what is in entry box
    my_entry.delete(0, END)
    # add clicked list item to entry box
    curs_location = my_list_exclude.curselection()
    if curs_location:
        selected_item = my_list_exclude.get(curs_location)
        my_entry.insert(0, selected_item)


# update entry box with listbox clicked
def show_recipe(e):
    curs_location = my_list_recipes.curselection()
    if curs_location:
        selected_item = my_list_recipes.get(curs_location)
        recipe_root = ttkb.Window(themename="superhero")
        recipe_root.title(selected_item)
        # Set the window size as a fraction of the screen size
        recipe_window_width = int(screen_width * 0.45)
        recipe_window_height = int(recipe_window_width * .8)

        recipe_root.iconbitmap('images/favicon.ico')
        recipe_root.geometry(f"{recipe_window_width}x{recipe_window_height}")

        for recipe in recipe_list:
            if recipe.recipe == selected_item:
                my_recipe_name = Label(recipe_root, text=f"{recipe.recipe}", wraplength=600,
                                       font=("helvetica", 28), fg="grey")
                my_recipe_name.place(relx=.5, rely=.1, anchor=ttkb.CENTER)

                my_recipe_desc = Label(recipe_root, text="Recipe Description:",
                                       font=("helvetica", 18), fg="grey")
                my_recipe_desc.place(relx=.205, rely=.24, anchor=ttkb.CENTER)

                my_recipe_ingr = Label(recipe_root, text="Recipe Ingredients:",
                                       font=("helvetica", 18), fg="grey")
                my_recipe_ingr.place(relx=.705, rely=.24, anchor=ttkb.CENTER)

                my_recipe_steps = Label(recipe_root, text="Steps:",
                                       font=("helvetica", 18), fg="grey")
                my_recipe_steps.place(relx=.11, rely=.575, anchor=ttkb.CENTER)

                scroll_ingr = ScrolledText(recipe_root, wrap=WORD, width=20, height=5,
                                           font=("Helvetica", 16))
                scroll_ingr.place(rely=.4, relx=.75, anchor=ttkb.CENTER)

                scroll_desc = ScrolledText(recipe_root, wrap=WORD, width=20, height=5,
                                           font=("Helvetica", 16))
                scroll_desc.place(rely=.4, relx=.25, anchor=ttkb.CENTER)

                scroll_steps = ScrolledText(recipe_root, wrap=WORD, width=49, height=7,
                                           font=("Helvetica", 16))
                scroll_steps.place(rely=.775, relx=.5, anchor=ttkb.CENTER)

                # Your paragraph text
                paragraph = f"{recipe.desc}"

                ingredients = f"{recipe.ingredients}"
                ingredients = ingredients[1:-1]

                steps = f"{recipe.steps}"
                steps = steps[1:-1]

                # Insert the paragraph text into the scrolled text widget
                if paragraph:
                    scroll_desc.insert(ttkb.END, paragraph)
                else:
                    scroll_desc.insert(ttkb.END, "This Recipe Has no Description")
                scroll_desc.config(state=DISABLED)

                if ingredients:
                    scroll_ingr.insert(ttkb.END, ingredients)
                else:
                    scroll_ingr.insert(ttkb.END, "This Recipe Has no Listed Ingredients")
                scroll_ingr.config(state=DISABLED)

                if steps:
                    scroll_steps.insert(ttkb.END, steps)
                else:
                    scroll_steps.insert(ttkb.END, "This Recipe Has no Listed Steps")
                scroll_steps.config(state=DISABLED)


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
            if input_text.lower() in my_list_exclude.get(0, END):
                idx = my_list_exclude.get(0, ttkb.END).index(input_text)
                my_list_exclude.delete(idx)


def remove_input():
    # Get the content of the entry
    input_text = my_entry.get()
    ingredients_data = list(ingredients)
    if input_text.lower() in ingredients_data:
        if input_text.lower() in my_list_input.get(0, END):
            idx = my_list_input.get(0, ttkb.END).index(input_text)
            my_list_input.delete(idx)
        elif input_text.lower() in my_list_exclude.get(0, END):
            idx = my_list_exclude.get(0, ttkb.END).index(input_text)
            my_list_exclude.delete(idx)

def exclude_input():
    # Get the content of the entry
    input_text = my_entry.get()
    ingredients_data = list(ingredients)
    if input_text.lower() in ingredients_data:
        if input_text.lower() not in my_list_exclude.get(0, END):
            my_list_exclude.insert(0, input_text)
        if input_text.lower() in my_list_input.get(0, END):
            idx = my_list_input.get(0, ttkb.END).index(input_text)
            my_list_input.delete(idx)

def find_recipies():
    # typed_length = len(typed)
    global recipe_list
    ingredient_data = []
    for ingredient in my_list_input.get(0, END):
        ingredient_data.append(ingredient)
    history_include.insert(0, ingredient_data)
    exclude_data = []
    for ingredient in my_list_exclude.get(0, END):
        exclude_data.append(ingredient)
    history_exclude.insert(0, exclude_data)
    recipe_list = graph.find_recipes(ingredient_data, exclude_data)
    update_recipes(recipe_list)

def show_history():
    history_root = ttkb.Window(themename="superhero")
    history_root.title("History")
    # Set the window size as a fraction of the screen size
    recipe_window_width = int(screen_width * 0.45)
    recipe_window_height = int(recipe_window_width * .8)

    history_root.iconbitmap('images/favicon.ico')
    history_root.geometry(f"{recipe_window_width}x{recipe_window_height}")

    my_recipe_name = Label(history_root, text="History",
                           font=("helvetica", 28), fg="grey")
    my_recipe_name.place(relx=.5, rely=.1, anchor=ttkb.CENTER)

    scroll_ingr = ScrolledText(history_root, wrap=WORD, width=50, height=15,
                               font=("Helvetica", 16))
    scroll_ingr.place(rely=.5, relx=.5, anchor=ttkb.CENTER)

    paragraph = ""
    history_log = 0
    for search in history_include:
        history_log += 1
        paragraph += f"Insert Log {history_log}: "
        for ingr in search:
            paragraph += ingr
            paragraph += ", "
        paragraph = paragraph[:-2]
        paragraph += "\n"
    history_log = 0
    for search in history_exclude:
        history_log += 1
        paragraph += f"Exclude Log {history_log}: "
        if search:
            for ingr in search:
                paragraph += ingr
                paragraph += ", "
            paragraph = paragraph[:-2]
            paragraph += "\n"
        else:
            paragraph += "No Ingredient Exclusions"
            paragraph += "\n"
    scroll_ingr.insert(ttkb.END, paragraph)



root = ttkb.Window(themename="superhero")
root.title("Recipe Pantry")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size as a fraction of the screen size
window_width = 960
window_height = int(window_width/1.25)

root.iconbitmap('images/favicon.ico')
root.geometry(f"{window_width}x{window_height}")
print(window_width)
print(window_height)
root.resizable(False, False)

recipe_list = []
history_include = []
history_exclude = []

graph = Graph()

#tree = SplayTree()

ingredients = graph.nodes.keys()

my_frame = ttkb.Frame(root, bootstyle="light")
my_frame.place(x=0, y=0)

# Create a button to add ingredient
add_button = ttkb.Button(root, text="Add Ingr.", command=add_input)
add_button.place(relx=.545, rely=.15, anchor=ttkb.CENTER)

# Create a button to remove ingredient
remove_button = ttkb.Button(root, text="Remove Ingr.", command=remove_input)
remove_button.place(relx=.645, rely=.15, anchor=ttkb.CENTER)

# Create a button to remove ingredient
remove_button = ttkb.Button(root, text="Exclude Ingr.", command=exclude_input)
remove_button.place(relx=.755, rely=.15, anchor=ttkb.CENTER)

# Create a button to find recipes
remove_button = ttkb.Button(root, text="Search Recipes", command=find_recipies)
remove_button.place(relx=.915, rely=.15, anchor=ttkb.CENTER)

# Create a button to show history
remove_button = ttkb.Button(root, text="History", command=show_history)
remove_button.place(relx=.06, rely=.05, anchor=ttkb.CENTER)

# create a label for project name
my_label = Label(root, text="Recipe Pantry", font=("helvetica", 28), fg="grey")
my_label.place(relx=.5, rely=.05, anchor=ttkb.CENTER)

# create a label for "Search"
my_label = Label(root, text="Search Pantry:", font=("helvetica", 14), fg="grey")
my_label.place(relx=.09, rely=.15, anchor=ttkb.CENTER)

# create a label for "Exclude"
my_label = Label(root, text="Exclude:", font=("helvetica", 14), fg="grey")
my_label.place(relx=.55, rely=.39, anchor=ttkb.CENTER)

# create an entry box
my_entry = Entry(root, font=("helvetica", 20), relief=SUNKEN)
my_entry.place(relx=.33, rely=.15, anchor=ttkb.CENTER)

# create an ingredient list box
my_list_ingredients = Listbox(root, width=40, font=("helvetica", 14))
my_list_ingredients.place(relx=.26, rely=.35, anchor=ttkb.CENTER)

# create an input list box
my_list_input = Listbox(root, width=40, font=("helvetica", 14), height=4)
my_list_input.place(relx=.74, rely=.3, anchor=ttkb.CENTER)

# create an exclude list box
my_list_exclude = Listbox(root, width=40, font=("helvetica", 14), height=3)
my_list_exclude.place(relx=.74, rely=.455, anchor=ttkb.CENTER)

# create a recipe list box
my_list_recipes = Listbox(root, width=60, font=("helvetica", 20))
my_list_recipes.place(relx=.5, rely=.75, anchor=ttkb.CENTER)

# Create combo box
structures = ["Graph", "Tree"]
my_comboBox = ttkb.Combobox(root, bootstyle="success", values=structures)
my_comboBox.place(relx=.9, rely=.05, anchor=ttkb.CENTER)

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
my_list_exclude.bind("<<ListboxSelect>>", fillout_exclude)

# create binding on list box on click
my_list_recipes.bind("<<ListboxSelect>>", show_recipe)

# create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

root.mainloop()
