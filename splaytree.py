from collections import defaultdict

import threading
import dataparser_extra
import csv


class Node:
    def __init__(self, ingredient="", recipes=[]):
        self.left = None
        self.right = None
        self.parent = None
        self.data = (ingredient, recipes)

    def __getitem__(self, item):
        return self.data[item]


class SplayTree:

    def __init__(self):
        self.root = Node()

        self.preOrderList = []
        self.inOrderList = []
        self.postOrderList = []

        self.ingredients = defaultdict(list)

        self.thread = threading.Thread(target=self.createSplayTree, daemon=True)
        self.thread.start()

    def generate_ingredients(self):
        with open("RAW_recipes.csv", 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                recipe = dataparser_extra.RecipeData(row[0], row[10][1:-1].replace("'", "").split(', '),
                                                     row[8][1:-1].replace("'", "").split(', '), row[9])
                ingredients = recipe.ingredients

                for ingredient in ingredients:
                    self.ingredients[ingredient].append(recipe)

    # called in insertion and search features to raise accessed node to root
    def splay(self, child):
        while child.parent:
            head = child.parent
            # completes one rotation if parent is root
            if head == self.root:
                if child.parent.right == child:
                    self.leftzag_rotate(head)
                elif child.parent.left == child:
                    self.rightzig_rotate(head)
            else:
                grandp = head.parent

                # zigzig
                if head.left == child and grandp.left == head:
                    self.rightzig_rotate(grandp)
                    self.rightzig_rotate(head)
                # zagzag
                elif head.right == child and grandp.right == head:
                    self.leftzag_rotate(grandp)
                    self.leftzag_rotate(head)
                # zagzig
                elif head.right == child and grandp.left == head:
                    self.leftzag_rotate(head)
                    self.rightzig_rotate(grandp)
                # zigzag
                elif head.left == child and grandp.right == head:
                    self.rightzig_rotate(head)
                    self.leftzag_rotate(grandp)

    # takes in node whose right child will end up the head of the substree
    def rightzig_rotate(self, head):
        parent = head.left
        head.left = parent.right

        if parent.right:
            parent.right.parent = head

        parent.parent = head.parent

        if head.parent is None:
            self.root = parent
        elif head == head.parent.right:
            head.parent.right = parent
        else:
            head.parent.left = parent

        parent.right = head
        head.parent = parent

    # takes in node whose left child will end up the head of the subtree
    def leftzag_rotate(self, head):
        parent = head.right
        head.right = parent.left

        if parent.left:
            parent.left.parent = head

        parent.parent = head.parent

        if head.parent is None:  # x is root
            self.root = parent
        elif head == head.parent.left:  # x is left child
            head.parent.left = parent
        else:  # x is right child
            head.parent.right = parent

        parent.left = head
        head.parent = parent

    def insert(self, head, ingredientData):
        if head[0] == "":
            head.left = ingredientData.left
            head.right = ingredientData.right
            head.parent = ingredientData.parent
            head.data = ingredientData.data

        else:
            if head.left is None and ingredientData[0] < head[0]:
                head.left = ingredientData
                head.left.parent = head
            elif head.right is None and ingredientData[0] > head[0]:
                head.right = ingredientData
                head.right.parent = head
            elif head.left and ingredientData[0] < head[0]:
                self.insert(head.left, ingredientData)
            elif head.right:
                self.insert(head.right, ingredientData)

        self.splay(ingredientData)

    def pre_order(self, head):
        if head is None:
            return

        self.preOrderList.append(head)
        if head.left is not None:
            self.pre_order(head.left)
        if head.right is not None:
            self.pre_order(head.right)

    def in_order(self, head):
        if head is None:
            return

        if head.left is not None:
            self.in_order(head.left)
        self.inOrderList.append(head)
        if head.right is not None:
            self.in_order(head.right)

    def post_order(self, head):
        if head is None:
            return

        if head.left is not None:
            self.post_order(head.left)
        if head.right is not None:
            self.post_order(head.right)
        self.postOrderList.append(head)

    def get_ingredient(self, ingredientName):
        head = self.root
        while head.data[0] != ingredientName:
            if head.left and head.right:
                if ingredientName > head.data[0]:
                    head = head.right
                elif ingredientName < head.data[0]:
                    head = head.left
            elif head.left:
                head = head.left
            elif head.right:
                head = head.right
            else:
                return "", []
        return head.data

    # tree creation
    def createSplayTree(self):
        with open("RAW_recipes.csv", 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                recipe = dataparser_extra.RecipeData(row[0], row[10][1:-1].replace("'", "").split(', '),
                                                     row[8][1:-1].replace("'", "").split(', '), row[9])
                ingredients = recipe.ingredients
                for ingredient in ingredients:
                    self.ingredients[ingredient].append(recipe)

                    if len(self.ingredients[ingredient]) == 1:
                        self.insert(self.root, Node(ingredient, self.ingredients[ingredient]))
                    else:
                        self.get_ingredient(ingredient)[1].append(recipe)

    def all_recipes_with(self, ingredient):
        return self.get_ingredient(ingredient)[1]

    def find_recipes(self, ingredients, exclude=[]):
        common_recipes = []

        if len(ingredients) > 0:
            common_recipes.extend(self.get_ingredient(ingredients[0])[1])

        if len(ingredients) > 1:  # removes recipes that aren't
            for ingredient in ingredients[1:]:
                recipes = self.get_ingredient(ingredient)[1]
                for item in common_recipes:
                    if item not in recipes:
                        common_recipes.remove(item)

        if len(exclude) > 0:  # removes excluded recipes with excluded ingredients
            for ingredient in exclude:
                recipes = self.get_ingredient(ingredient)[1]
                for item in common_recipes:
                    if item in recipes:
                        common_recipes.remove(item)

        return common_recipes
