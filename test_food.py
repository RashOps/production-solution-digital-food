"""
File : Test the Food class and its functions
"""

import os
import unittest
from food import Food

class TestFood(unittest.TestCase):
    """ class test food """

    def test_get_name(self):
        """ test_get_name """
        print('test_get_name')
        food_one = Food()
        food_two = Food()

        food_two.set_name('coconut')

        self.assertEqual(food_one.get_name() , None)
        self.assertEqual(food_two.get_name() , 'coconut')

    def test_is_fat(self):
        """ test_is_fast 
        you may test 3 different foods
        """
        print('test_is_fat')
        food_one = Food()
        food_two = Food()
        food_three = Food()

        # Set food fat
        food_one.set_fat(25.0)
        food_two.set_fat(20.0)
        food_three.set_fat(15.0)

        self.assertEqual(food_one.is_fat(), True)
        self.assertEqual(food_two.is_fat(), False)
        self.assertEqual(food_three.is_fat(), False)

    def test_retrieve_food(self):
        """
        Test the "retrieve_food_infos() function"
        """
        print('test_retrieve_food')
        food_one = Food()
        food_two = Food()

        # Retrieve food info
        food_one.retrieve_food_infos("pomme")
        food_two.retrieve_food_infos("citron")

        # test settings Food One
        self.assertEqual(food_one.get_name(), "pomme")
        self.assertEqual(food_one.is_fat(), False)
        self.assertEqual(food_one.get_calories(), 73.0)
        self.assertEqual(food_one.get_fat(), 0.4)
        self.assertEqual(food_one.get_carbs(), 17.0)
        self.assertEqual(food_one.get_proteins(), 0.4)

        # test settings Food Two
        self.assertEqual(food_two.get_name(), "citron")
        self.assertEqual(food_two.is_fat(), False)
        self.assertEqual(food_two.get_calories(), 21.0)
        self.assertEqual(food_two.get_fat(), 0.2)
        self.assertEqual(food_two.get_carbs(), 4.5)
        self.assertEqual(food_two.get_proteins(), 0.5)

    def test_display_food(self):
        """
        No need to test this function.
        It's a display function
        """

    def test_to_csv_file(self):
        """
        Test the save to csv file function
        """
        print('test_save_csv_file')

        food_one = Food()
        food_one.retrieve_food_infos("pomme")
        food_one.save_to_csv_file("temp_food.csv")

        with open("temp_food.csv", 'r') as f:
            lines = f.readlines()

        if os.path.exists("temp_food.csv"):
            os.remove("temp_food.csv")

        self.assertEqual(len(lines), 2) # Header + Data
        self.assertIn("name,calories", lines[0])
        self.assertIn("pomme", lines[1])

if __name__ == '__main__':
    unittest.main()
