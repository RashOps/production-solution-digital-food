"""
Launch function in command line
"""

from food import Food
import argparse
print("Running script...")

parser = argparse.ArgumentParser("Food Informations")
parser.add_argument('-f', '--food', help="your food name", default='tomate')

args = parser.parse_args()

food = Food()
food.retrieve_food_infos(args.food)
food.display_food_infos()
food.save_to_csv_file("food.csv")
print(f"Aliment gras ({food.get_name()}) ? : {food.is_fat()}")
