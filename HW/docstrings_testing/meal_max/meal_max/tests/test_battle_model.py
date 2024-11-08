import pytest
from unittest.mock import patch
from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random
from meal_max.models.battle_model import BattleModel

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

""" TEST 1: Adding combatants: testing prep_combatant """
def test_add_combatant (sample_meal_one):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one)
    assert len (battle_model.get_combatants()) == 1 #makes sure that there is only 1 contestant as it should be

""" TEST 2: Adding combatants over the limit: testing prep_combatant does not add too much """
def test_add_combatant_limit (sample_meal_one, sample_meal_two):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one) #adding the Cheeseburger
    battle_model.prep_combatant(sample_meal_two) #adding the Pizza
    with pytest.raises (ValueError, match = "Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal_one) #raises the ValueError if there is greater than 2

""" TEST 3: Clearing Combatants """
def test_clear_combatants (sample_meal_one):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one)
    battle_model.clear_combatants()
    assert len (battle_model.get_combatants()) == 0 #makes sure that there are none

""" TEST #4: Test Getting the Combatants: so that its the full list of the meals """
def test_get_combatants (sample_meal_one, sample_meal_two):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one) #adding the Cheeseburger
    battle_model.prep_combatant(sample_meal_two) #adding the Pizza
    combatants = battle_model.get_combatants()

    assert len (combatants) == 2 #its 2 because we added 2: Cheeseburger and Pizza
    assert combatants[0] == sample_meal_one #makes sure that it gives the info on the Cheeseburger
    assert combatants[1] == sample_meal_two #makes sure that it gives the info on the Pizza
    
""" TEST #5: Battling with < 2 combatants so that it gives a Value Error """
def test_not_enough_combatants (sample_meal_one):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one) #adding the Cheeseburger
    with pytest.raises (ValueError, match = "Two combatants must be prepped for a battle."):
        battle_model.battle() #raises the ValueError if < 2 fighters 

""" TEST #6: Testing the get_battle_score """
def test_get_battle_score (sample_meal_one):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one)
    score = battle_model.get_battle_score(sample_meal_one) #adding the Cheeseburger
    assert isinstance(score,float) 
    expected_score = (sample_meal_one.price * len(sample_meal_one.cuisine)) - 2 #2 is the amount for MED as HIGH is 1 and LOW is 3
    assert score == expected_score #makes sure that the score given by the program matches the formulaic result


""" TEST #7: Battling with 2 combatants: should produce a winner and loser should be removed """
@patch("meal_max.utils.random_utils.get_random", return_value=0.5) 
def test_battle_outcome (sample_meal_one, sample_meal_two):
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one) #adding the Cheeseburger
    battle_model.prep_combatant(sample_meal_two) #adding the Pizza

    winner = battle_model.battle() 
    assert winner in [sample_meal_one, sample_meal_two] #the winner is one of them
    assert len(battle_model.get_combatants()) == 1 #because the loser was discarded so now its 1