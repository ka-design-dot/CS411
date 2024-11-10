import pytest
from unittest.mock import patch
from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.models.battle_model import BattleModel

######################################################
#
#    Helper Functions
#
######################################################

def sample_meal_one():
    """Create a sample meal representing a Cheeseburger."""
    return Meal(meal="Cheeseburger", price=13.0, cuisine="American", difficulty="LOW", id=1)

def sample_meal_two():
    """Create a sample meal representing a Pizza."""
    return Meal(meal="Pizza", price=20.0, cuisine="Italian", difficulty="MED", id=2)

######################################################
#
#    Unit Tests
#
######################################################

def test_add_combatant():
    """Test adding a single combatant to BattleModel."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    assert len(battle_model.get_combatants()) == 1

def test_add_combatant_limit():
    """Test adding more than two combatants, which should raise a ValueError."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    battle_model.prep_combatant(sample_meal_two())
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal_one())  # Attempting to add a third combatant

def test_clear_combatants():
    """Test clearing all combatants from BattleModel."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    battle_model.clear_combatants()
    assert len(battle_model.get_combatants()) == 0

def test_get_combatants():
    """Test retrieving the full list of combatants from BattleModel."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    battle_model.prep_combatant(sample_meal_two())
    combatants = battle_model.get_combatants()

    assert len(combatants) == 2
    assert combatants[0] == sample_meal_one()
    assert combatants[1] == sample_meal_two()

def test_not_enough_combatants():
    """Test initiating a battle with fewer than two combatants, which should raise a ValueError."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

def test_get_battle_score():
    """Test calculating the battle score of a combatant."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    score = battle_model.get_battle_score(sample_meal_one())
    assert isinstance(score, float)
    expected_score = (sample_meal_one().price * len(sample_meal_one().cuisine)) - 3  # 3 for LOW difficulty
    assert score == expected_score

@patch("meal_max.utils.random_utils.get_random", return_value=0.5)
def test_battle_outcome(mock_random):
    """Test battling between two combatants and verifying the outcome."""
    battle_model = BattleModel()
    battle_model.prep_combatant(sample_meal_one())
    battle_model.prep_combatant(sample_meal_two())

    winner = battle_model.battle()
    assert winner in [sample_meal_one(), sample_meal_two()]
    assert len(battle_model.get_combatants()) == 1
