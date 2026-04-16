# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:21:18 2026

@author: kevin
"""

# Sandwich Maker - INFO233 Group Project



#Ingredient Options
INGREDIENTS = {
    "Bread": [
        "White Bread",       
        "Whole Wheat Bread",   
        "Sour Dough Bread",     
        "Rye Bread",           
        "Multigrain Bread",    
        "Pita Bread",          
        "Potato Bread",        
        "Ciabatta",
        "Whole Wheat Tortilla"
    ],
    "Protein": [
        "Turkey",              
        "Deli Sliced Ham",     
        "Roast Beef",          
        "Tuna",               
        "Chicken Breast",    
        "Salami",            
        "Pepperoni",            
        "Bacon",               
        "Egg",                
        "Turkey Bacon"        
    ],
    "Cheese": [
        "American Cheese",      
        "Cheddar Cheese",
        "Swiss Cheese",
        "Provolone Cheese",
        "Mozzarella Cheese",
        "Pepper Jack Cheese",
        "Brie Cheese",
        "Gouda Cheese",
        "Muenster Cheese",     
        "Feta Cheese"
    ],
    "Vegetables": [
        "Lettuce",
        "Tomato",
        "Onion",
        "Pickles",
        "Cucumber",
        "Spinach",
        "Bell Pepper",
        "Avocado",
        "Jalapeno Pepper",     
        "Banana Pepper"
    ],
    "Condiments": [
        "Mayonnaise",
        "Mustard",
        "Ketchup",
        "Ranch Dressing",
        "Hot Sauce",
        "Honey Mustard",
        "BBQ Sauce",
        "Sriracha Sauce",
        "Olive Oil",
        "Vinegar"
    ]
}

#Display Function

def display_options(category, items): #Displays numbered options for a given ingredient category.
    print(f"\n--- {category} Options ---")
    for i, item in enumerate(items, start=1):
        print(f"  {i}. {item}")
    print("  Type the NUMBER to select, or 'skip' to skip this category.")

#Get Ingredient Choice Function

def get_ingredient_choice(category, items): #Lets the user pick one item from a category by number. Returns the selected item name as a string, or None if skipped.
    display_options(category, items)

    while True:
        user_input = input(f"\nYour choice for {category}: ").strip().lower()

        if user_input == "skip":
            print(f"  Skipping {category}.")
            return None

        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(items):
                selected = items[index]
                print(f"  Added: {selected}")
                return selected
            else:
                print(f"  Please enter a number between 1 and {len(items)}.")
        else:
            print("  Invalid input. Enter a number or 'skip'.")

#Get Extras (Repeating Category)

def get_extras(category, items): #For categories like Vegetables/Condiments, this lets the user keep picking items until they type 'done'. Returns a list of selected item names.
    selected = []
    display_options(category, items)
    print("  Type numbers one at a time. Type 'done' when finished.")

    while True:
        user_input = input(f"  Add a {category} (or 'done'): ").strip().lower()

        if user_input == "done":
            break
        elif user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(items):
                item = items[index]
                if item not in selected:
                    selected.append(item)
                    print(f"  Added: {item}")
                else:
                    print(f"  {item} is already in your sandwich!")
            else:
                print(f"  Please enter a number between 1 and {len(items)}.")
        else:
            print("  Invalid input. Enter a number or 'done'.")

    return selected

#Main Input Function

def get_sandwich_ingredients(): #Walks the user through building their sandwich step by step.
   
    print("       Welcome to the Sandwich Maker!   ")

    selected_ingredients = []

    #Single-choice categories (pick one)
    for category in ["Bread", "Protein", "Cheese"]:
        choice = get_ingredient_choice(category, INGREDIENTS[category])
        if choice:
            selected_ingredients.append({"name": choice, "category": category})

    #Multi-choice categories (pick many)
    for category in ["Vegetables", "Condiments"]:
        choices = get_extras(category, INGREDIENTS[category])
        for item in choices:
            selected_ingredients.append({"name": item, "category": category})

    #Summary of selections
    print("         Your Sandwich Ingredients:     ")
    if selected_ingredients:
        for ingredient in selected_ingredients:
            print(f"  - {ingredient['name']} ({ingredient['category']})")
    else:
        print("  No ingredients selected!")

    print("\nIngredient selection complete!\n")
    return selected_ingredients