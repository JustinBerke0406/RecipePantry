from tkinter import *
from ttkbootstrap.constants import *
from splaytree import *
from ttkbootstrap import ScrolledText
import ttkbootstrap as ttkb
from graph import Graph
import time


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
        # set icon and dimensions
        recipe_root.iconbitmap('images/favicon.ico')
        recipe_root.geometry(f"{recipe_window_width}x{recipe_window_height}")
        # find and display recipe
        for recipe in recipe_list:
            if recipe.recipe == selected_item:
                # create new window
                my_recipe_name = Label(recipe_root, text=f"{recipe.recipe}", wraplength=600,
                                       font=("helvetica", text_28), fg="grey")
                my_recipe_name.place(relx=.5, rely=.1, anchor=ttkb.CENTER)

                my_recipe_desc = Label(recipe_root, text="Recipe Description:",
                                       font=("helvetica", text_18), fg="grey")
                my_recipe_desc.place(relx=.205, rely=.23, anchor=ttkb.CENTER)

                my_recipe_ingr = Label(recipe_root, text="Recipe Ingredients:",
                                       font=("helvetica", text_18), fg="grey")
                my_recipe_ingr.place(relx=.705, rely=.23, anchor=ttkb.CENTER)

                my_recipe_steps = Label(recipe_root, text="Steps:",
                                       font=("helvetica", text_18), fg="grey")
                my_recipe_steps.place(relx=.11, rely=.565, anchor=ttkb.CENTER)

                scroll_ingr = ScrolledText(recipe_root, wrap=WORD, width=20, height=5,
                                           font=("Helvetica", text_18))
                scroll_ingr.place(rely=.39, relx=.75, anchor=ttkb.CENTER)

                scroll_desc = ScrolledText(recipe_root, wrap=WORD, width=20, height=5,
                                           font=("Helvetica", text_18))
                scroll_desc.place(rely=.39, relx=.25, anchor=ttkb.CENTER)

                scroll_steps = ScrolledText(recipe_root, wrap=WORD, width=47, height=7,
                                           font=("Helvetica", text_18))
                scroll_steps.place(rely=.775, relx=.5, anchor=ttkb.CENTER)

                # recipe description
                paragraph = f"{recipe.desc}"

                ingredients = f"{recipe.ingredients}"
                ingredients = ingredients[1:-1]

                steps = f"{recipe.steps}"
                steps = steps[1:-1]

                # Add paragraph text
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
    # grab what was typed by user
    typed = my_entry.get()
    # typed_length = len(typed)
    new_list = list(ingredients)
    if typed == '':
        data = new_list
    else:
        data = []
        for ingredient in new_list:
            if typed.lower() in ingredient.lower():
                data.append(ingredient)
    update(data)

# add input to input and remove from exclude if present
def add_input():
    # Get the content of the entry
    input_text = my_entry.get()
    ingredients_data = list(ingredients)
    if input_text.lower() in ingredients_data:
        if input_text.lower() not in my_list_input.get(0, END):
            my_list_input.insert(0, input_text)
            if input_text.lower() in my_list_exclude.get(0, END):
                idx = my_list_exclude.get(0, ttkb.END).index(input_text)
                my_list_exclude.delete(idx)

# remove input from either input or exclude if present
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

# add to exclude
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

# find and update recipes based on user input
def find_recipies():
    global recipe_list
    ingredient_data = []
    for ingredient in my_list_input.get(0, END):
        ingredient_data.append(ingredient)
    history_include.insert(0, ingredient_data)
    exclude_data = []
    for ingredient in my_list_exclude.get(0, END):
        exclude_data.append(ingredient)
    history_exclude.insert(0, exclude_data)
    # if graph
    if structure_type:
        start = time.time_ns()
        recipe_list = graph.find_recipes(ingredient_data, exclude_data)
        end = time.time_ns()
        total_time = end-start
        display_time(total_time)
    # if splay tree
    else:
        start = time.time_ns()
        recipe_list = splay_tree.find_recipes(ingredient_data, exclude_data)
        end = time.time_ns()
        total_time = end - start
        display_time(total_time)
    update_recipes(recipe_list)

# display recipe loading time in ns
def display_time(total_time):
    my_time.config(text=f"Time: {total_time}ns")

# create history window
def show_history():
    history_root = ttkb.Window(themename="superhero")
    history_root.title("History")
    # Set the window size as a fraction of the screen size
    recipe_window_width = int(screen_width * 0.45)
    recipe_window_height = int(recipe_window_width * .8)

    history_root.iconbitmap('images/favicon.ico')
    history_root.geometry(f"{recipe_window_width}x{recipe_window_height}")

    my_history_label = Label(history_root, text="History",
                           font=("helvetica", text_28), fg="grey")
    my_history_label.place(relx=.5, rely=.1, anchor=ttkb.CENTER)

    scroll_history = ScrolledText(history_root, wrap=WORD, width=50, height=15, state=DISABLED,
                               font=("Helvetica", text_18))
    scroll_history.place(rely=.55, relx=.5, anchor=ttkb.CENTER)
    # get and store history
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
    scroll_history.insert(ttkb.END, paragraph)

# change structure type
def change_type(e):
    global structure_type
    if my_combo_type.get() == "Graph":
        structure_type = True
    elif my_combo_type.get() == "SplayTree":
        structure_type = False

# create main window
root = ttkb.Window(themename="superhero")
root.title("Recipe Pantry")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size as a fraction of the screen size
window_height = int(screen_height*0.75)
window_width = int(window_height*1.25)
root.iconbitmap('images/favicon.ico')
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

structure_type = True
recipe_list = []
history_include = []
history_exclude = []

graph = Graph()
splay_tree = SplayTree()
ingredients = graph.nodes.keys()

my_frame = ttkb.Frame(root, bootstyle="light")
my_frame.place(x=0, y=0)

# ratios to account for different screen resolutions
text_28 = int(window_height*(28/768))
text_20 = int(window_height*(20/768))
text_18 = int(window_height*(18/768))
text_14 = int(window_height*(14/768))
button_add_scale = int(window_height*(8/768))
button_remove_scale = int(window_height*(12/768))
button_exclude_scale = int(window_height*(12/768))
button_search_scale = int(window_height*(14/768))

# Create a button to add ingredient
add_button = ttkb.Button(root, text="Add Ingr.", width=button_add_scale, command=add_input)
add_button.place(relx=.545, rely=.15, anchor=ttkb.CENTER)

# Create a button to remove ingredient
remove_button = ttkb.Button(root, text="Remove Ingr.", width=button_remove_scale, command=remove_input)
remove_button.place(relx=.645, rely=.15, anchor=ttkb.CENTER)

# Create a button to exclude ingredient
remove_button = ttkb.Button(root, text="Exclude Ingr.", width=button_exclude_scale, command=exclude_input)
remove_button.place(relx=.755, rely=.15, anchor=ttkb.CENTER)

# Create a button to find recipes
remove_button = ttkb.Button(root, text="Search Recipes", width=button_search_scale, command=find_recipies)
remove_button.place(relx=.915, rely=.15, anchor=ttkb.CENTER)

# Create a button to show history
remove_button = ttkb.Button(root, text="History", command=show_history)
remove_button.place(relx=.06, rely=.05, anchor=ttkb.CENTER)

# create a label for project name
my_label = Label(root, text="Recipe Pantry", font=("helvetica", text_28), fg="grey")
my_label.place(relx=.5, rely=.05, anchor=ttkb.CENTER)

# create a label for "Search"
my_label = Label(root, text="Search Pantry:", font=("helvetica", text_14), fg="grey")
my_label.place(relx=.09, rely=.15, anchor=ttkb.CENTER)

# create a label for "Exclude"
my_label = Label(root, text="Exclude:", font=("helvetica", text_14), fg="grey")
my_label.place(relx=.55, rely=.35, anchor=ttkb.CENTER)

# create a label for time
my_time = Label(root, text=f"Time: 0.0ns", font=("helvetica", text_14), fg="grey")
my_time.place(relx=.975, rely=.52, anchor=ttkb.E)

# create an entry box
my_entry = Entry(root, font=("helvetica", text_20))
my_entry.place(relx=.33, rely=.15, anchor=ttkb.CENTER)

# create an ingredient list box
my_list_ingredients = Listbox(root, width=40, font=("helvetica", text_14))
my_list_ingredients.place(relx=.26, rely=.35, anchor=ttkb.CENTER)

# create an input list box
my_list_input = Listbox(root, width=40, font=("helvetica", text_14), height=4)
my_list_input.place(relx=.74, rely=.261, anchor=ttkb.CENTER)

# create an exclude list box
my_list_exclude = Listbox(root, width=40, font=("helvetica", text_14), height=4)
my_list_exclude.place(relx=.74, rely=.44, anchor=ttkb.CENTER)

# create a recipe list box
my_list_recipes = Listbox(root, width=60, font=("helvetica", text_20))
my_list_recipes.place(relx=.5, rely=.75, anchor=ttkb.CENTER)

# Create combo box
structures = ["Graph", "Splaytree"]
my_combo_type = ttkb.Combobox(root, bootstyle="success", values=structures, state="readonly")
my_combo_type.place(relx=.9, rely=.05, anchor=ttkb.CENTER)

# Set combo default
my_combo_type.current(0)

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

# create a binding on the type box
my_combo_type.bind("<<ComboboxSelected>>", change_type)

root.mainloop()
