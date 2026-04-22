#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 20:09:42 2026

@author: jonathanhunal
"""


 token = get_token()

 while True:
     ingredients = get_sandwich_ingredients()
     results = calculate_total_macros(ingredients, token)
     print_final_summary(results)

     again = input("\nWould you like to build another sandwich? (yes or no): ").strip().lower()

     if again == "yes":
         print("\nLet's build another sandwich!\n")
     elif again == "no":
         print("\nThanks for using the Sandwich Maker! Enjoy your meal!")
         break
     else:
         print("Invalid input. Please enter yes or no.")
         

