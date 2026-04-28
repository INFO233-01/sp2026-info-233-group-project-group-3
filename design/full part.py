# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:12:21 2026

@author: katat
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:21:18 2026

@author: kevin
"""

# Sandwich Maker - INFO233 Group Project


import requests
from config import CLIENT_ID, CLIENT_SECRET
import urllib.parse
import webbrowser
import json




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
    print(f"\n{category} Options")
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
    print("- Here you are allowed to create the sandwich of your dreams! Simply choose anything you'd like in your sandwich; from the bread, protein, cheese, vegetables, and even the condiments! continue through each section, and at the very end we will give you a summary of the macros inside your sandwich. Have fun!")

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


    
#######################################
   
def get_token():
    url = "https://oauth.fatsecret.com/connect/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials", "scope": "basic"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    token = response.json()["access_token"]
    print("Connected to FatSecret successfully!")
    return token

def search_food(query, token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json",
        "max_results": 10
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()



#######################################################

# Get Food Details Function
def get_food_details(food_id, token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "method": "food.get",
        "food_id": food_id,
        "format": "json"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


# Extract Macros Function
def extract_macros(food_data):
    try:
        servings = food_data["food"]["servings"]["serving"]

        if isinstance(servings, list):
            serving = next(
                (s for s in servings if "100" in s.get("serving_description", "")),
                servings[0]
            )
        else:
            serving = servings

        return {
            "calories": float(serving.get("calories", 0) or 0),
            "protein": float(serving.get("protein", 0) or 0),
            "carbs": float(serving.get("carbohydrate", 0) or 0),
            "fat": float(serving.get("fat", 0) or 0)
        }

    except Exception as e:
        print("Error extracting macros:", e)
        return None


# Get Macros for One Food
def get_macros_for_food(food_name, token):
    try:
        search_results = search_food(food_name, token)

        foods = search_results.get("foods", {}).get("food")
        if not foods:
            print(f"No results found for {food_name}")
            return None

        if isinstance(foods, list):
            food = foods[0]
        else:
            food = foods

        food_id = food["food_id"]
        food_details = get_food_details(food_id, token)
        macros = extract_macros(food_details)

        if macros is None:
            return None

        return {
            "name": food_name,
            "food_id": food_id,
            "macros": macros
        }

    except Exception as e:
        print(f"Could not find macros for {food_name}: {e}")
        return None


# Person 3 Main Function
def calculate_total_macros(ingredients, token):
    total = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    per_item = []
    errors = []

    for item in ingredients:
        name = item["name"]
        category = item.get("category", "Unknown")

        print(f"\nGetting macros for {name}...")

        result = get_macros_for_food(name, token)

        if result and result["macros"]:
            macros = result["macros"]

            per_item.append({
                "name": name,
                "category": category,
                "calories": macros["calories"],
                "protein": macros["protein"],
                "carbs": macros["carbs"],
                "fat": macros["fat"]
            })

            total["calories"] += macros["calories"]
            total["protein"] += macros["protein"]
            total["carbs"] += macros["carbs"]
            total["fat"] += macros["fat"]

            print(f"  {name}: {macros}")
        else:
            errors.append(name)
            print(f"  Skipping {name}")

    return {
        "items": per_item,
        "total": total,
        "errors": errors
    }


# Graph Function (same file, no import needed)
def graph_macros_api(calories, protein, carbs, fat):
    chart_config = {
        "type": "bar",
        "data": {
            "labels": ["Calories", "Protein", "Carbs", "Fat"],
            "datasets": [{
                "label": "Final Sandwich Macros",
                "data": [calories, protein, carbs, fat]
            }]
        }
    }

    url = "https://quickchart.io/chart?c=" + urllib.parse.quote(json.dumps(chart_config))
    print("\nOpening macro chart in browser...")
    webbrowser.open(url)


def print_final_summary(results):
    print("\n" + "=" * 40)
    print("        FINAL SANDWICH SUMMARY")
    print("=" * 40)

    if results["items"]:
        print("\nIngredients and Macros:")
        for item in results["items"]:
            print(
                f"- {item['name']} ({item['category']}) | "
                f"Calories: {item['calories']}, "
                f"Protein: {item['protein']}g, "
                f"Carbs: {item['carbs']}g, "
                f"Fat: {item['fat']}g"
            )
    else:
        print("\nNo ingredient macros were found.")

    print("\nTotal Macros:")
    print(f"Calories: {results['total']['calories']:.2f}")
    print(f"Protein:  {results['total']['protein']:.2f} g")
    print(f"Carbs:    {results['total']['carbs']:.2f} g")
    print(f"Fat:      {results['total']['fat']:.2f} g")

    if results["errors"]:
        print("\nCould not get macros for:")
        for item in results["errors"]:
            print(f"- {item}")

    print("=" * 40)

    graph_macros_api(
        results["total"]["calories"],
        results["total"]["protein"],
        results["total"]["carbs"],
        results["total"]["fat"]
    )
    
if __name__ == "__main__":
    ingredients = get_sandwich_ingredients()
    token = get_token()
    results = calculate_total_macros(ingredients, token)
    print_final_summary(results)
