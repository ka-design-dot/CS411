import pytest

"""Importing the class from battle_model and getting Meal"""
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal, update_meal_stats

@pytest.fixture()
def BattleModel():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()



