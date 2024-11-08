import pytest

"""Unit tests for battle_model that will """

"""Importing the class from battle_model and getting Meal"""
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal, update_meal_stats

""" The first meal is an American Cheeseburger that is $13 and easy and quick to prepare"""
def sample_meal_one():
    return Meal (meal = "Cheeseburger", price = 13.0, cusine = "American", difficulty = "LOW", id = 1)

""" The second meal is an Italian pizza that is $20 and take a bit more time and effort"""
def sample_meal_two():
    return Meal (meal = "Pizza", price = 20.0, cusine = "Italian", difficulty = "MED", id = 2)

""" TEST 1: Adding combatants """

""" TEST 2: Clearing Combatants """

""" TEST 3: Test Getting the Combatants """

""" TEST 4: """