import pytest
from meal_max.models.kitchen_model import Meal, create_meal, clear_meals, delete_meal, get_leaderboard, get_meal_by_id, get_meal_by_name, update_meal_stats

@pytest.fixture
def setup_database():
    """Fixture to set up and tear down a test database."""
    clear_meals()  # Clear any existing data before each test
    yield
    clear_meals()  # Clear data after each test

def test_meal_init():
    """Tests the initialization of a Meal instance."""
    meal = Meal(id=1, meal="Pasta", cuisine="Italian", price=12.99, difficulty="MED")
    assert meal.id == 1
    assert meal.meal == "Pasta"
    assert meal.cuisine == "Italian"
    assert meal.price == 12.99
    assert meal.difficulty == "MED"

    with pytest.raises(ValueError):
        Meal(id=2, meal="Salad", cuisine="American", price=-5, difficulty="LOW")
    with pytest.raises(ValueError):
        Meal(id=3, meal="Soup", cuisine="French", price=8, difficulty="INVALID")

def test_create_meal(setup_database):
    """Tests creating a meal in the database."""
    create_meal("Pasta", "Italian", 10.0, "MED")
    meal = get_meal_by_name("Pasta")
    assert meal.meal == "Pasta"
    assert meal.cuisine == "Italian"
    assert meal.price == 10.0
    assert meal.difficulty == "MED"

    # Test for duplicate meal name
    with pytest.raises(ValueError, match="already exists"):
        create_meal("Pasta", "Italian", 10.0, "MED")

    # Test for invalid price and difficulty
    with pytest.raises(ValueError, match="positive number"):
        create_meal("Burger", "American", -5, "LOW")
    with pytest.raises(ValueError, match="LOW, MED, or HIGH"):
        create_meal("Burger", "American", 10, "INVALID")

def test_clear_meals(setup_database):
    """Tests clearing all meals from the database."""
    create_meal("Taco", "Mexican", 8.0, "LOW")
    clear_meals()
    with pytest.raises(ValueError, match="not found"):
        get_meal_by_name("Taco")

def test_delete_meal(setup_database):
    """Tests marking a meal as deleted."""
    create_meal("Pizza", "Italian", 12.0, "HIGH")
    meal = get_meal_by_name("Pizza")
    delete_meal(meal.id)
    
    with pytest.raises(ValueError, match="has been deleted"):
        get_meal_by_id(meal.id)

def test_get_leaderboard(setup_database):
    """Tests retrieving the leaderboard sorted by wins or win percentage."""
    create_meal("Sushi", "Japanese", 15.0, "MED")
    update_meal_stats(1, "win")
    leaderboard = get_leaderboard("wins")
    
    assert leaderboard[0]["meal"] == "Sushi"
    assert leaderboard[0]["wins"] == 1
    assert leaderboard[0]["win_pct"] == 100.0

    with pytest.raises(ValueError, match="Invalid sort_by parameter"):
        get_leaderboard("invalid")

def test_get_meal_by_id(setup_database):
    """Tests retrieving a meal by its ID."""
    create_meal("Burger", "American", 9.99, "LOW")
    meal = get_meal_by_name("Burger")
    retrieved_meal = get_meal_by_id(meal.id)
    assert retrieved_meal.meal == "Burger"

    with pytest.raises(ValueError, match="not found"):
        get_meal_by_id(999)

def test_get_meal_by_name(setup_database):
    """Tests retrieving a meal by its name."""
    create_meal("Sandwich", "American", 5.99, "LOW")
    meal = get_meal_by_name("Sandwich")
    assert meal.meal == "Sandwich"

    with pytest.raises(ValueError, match="not found"):
        get_meal_by_name("NonExistent")

def test_update_meal_stats(setup_database):
    """Tests updating meal stats based on battle outcomes."""
    create_meal("Ramen", "Japanese", 12.5, "MED")
    meal = get_meal_by_name("Ramen")
    
    # Update with a win
    update_meal_stats(meal.id, "win")
    updated_meal = get_meal_by_id(meal.id)
    assert updated_meal.wins == 1
    assert updated_meal.battles == 1

    # Update with a loss
    update_meal_stats(meal.id, "loss")
    updated_meal = get_meal_by_id(meal.id)
    assert updated_meal.battles == 2

    with pytest.raises(ValueError, match="Invalid result"):
        update_meal_stats(meal.id, "invalid_result")

    delete_meal(meal.id)
    with pytest.raises(ValueError, match="has been deleted"):
        update_meal_stats(meal.id, "win")
