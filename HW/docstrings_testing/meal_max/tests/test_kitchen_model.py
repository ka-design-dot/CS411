import pytest
import sqlite3
from contextlib import contextmanager
from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    clear_meals,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats
)

######################################################
#
#    Fixtures
#
######################################################

@pytest.fixture
def mock_cursor(mocker):
    """Fixture that provides a mocked database cursor and patches
    the `get_db_connection` function to return a mock connection.
    """
    # Create a mock connection and cursor
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None


    @contextmanager
    def mock_get_db_connection():
        yield mock_conn


    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)
    return mock_cursor 

######################################################
#
#    Add and Delete Meals
#
######################################################

def test_create_meal(mock_cursor):
    """Test creating a new meal in the database."""
    create_meal("Pasta", "Italian", 22.5, "MED")
    expected_args = ("Pasta", "Italian", 22.5, "MED")
    actual_args = mock_cursor.execute.call_args[0][1]
    assert actual_args == expected_args

def test_create_meal_duplicate(mock_cursor):
    """Test creating a meal with a duplicate name, which should raise an error."""
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: meals.meal")
    with pytest.raises(ValueError, match="Meal with name 'Pasta' already exists"):
        create_meal("Pasta", "Italian", 22.5, "MED")

def test_create_meal_invalid_price():
    """Test creating a meal with an invalid (negative) price, which should raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid price: -5.0. Price must be a positive number."):
        create_meal("Pasta", "Italian", -5.0, "MED")

def test_create_meal_invalid_difficulty():
    """Test creating a meal with an invalid difficulty level, which should raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid difficulty level: EASY. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal("Pasta", "Italian", 22.5, "EASY")

def test_delete_meal(mock_cursor):
    """Test soft-deleting a meal in the database by setting its deleted status to TRUE."""
    mock_cursor.fetchone.return_value = [False]
    delete_meal(1)
    expected_select_sql = "SELECT deleted FROM meals WHERE id = ?"
    expected_update_sql = "UPDATE meals SET deleted = TRUE WHERE id = ?"
    actual_select_sql = mock_cursor.execute.call_args_list[0][0][0]
    actual_update_sql = mock_cursor.execute.call_args_list[1][0][0]
    assert actual_select_sql == expected_select_sql
    assert actual_update_sql == expected_update_sql

######################################################
#
#    Retrieve Meal Information
#
######################################################

def test_get_meal_by_id(mock_cursor):
    """Test retrieving a meal by its ID from the database."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 22.0, "MED", False)
    meal = get_meal_by_id(1)
    assert meal.meal == "Pasta"
    assert meal.price == 22.0

def test_get_meal_by_name(mock_cursor):
    """Test retrieving a meal by its name from the database."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 22.0, "MED", False)
    meal = get_meal_by_name("Pasta")
    assert meal.cuisine == "Italian"

def test_get_leaderboard(mock_cursor):
    """Test retrieving a leaderboard of meals ordered by wins."""
    mock_cursor.fetchall.return_value = [
        (1, "Pasta", "Italian", 22.0, "MED", 22, 8, 80.0),
        (2, "Burger", "American", 12.5, "LOW", 20, 15, 75.0)
    ]
    leaderboard = get_leaderboard(sort_by="wins")
    assert leaderboard[0]["meal"] == "Pasta"
    assert leaderboard[1]["meal"] == "Burger"

######################################################
#
#    Update Meal Statistics
#
######################################################

def test_update_meal_stats_win(mock_cursor):
    """Test updating the stats of a meal by incrementing its wins and battles after a win."""
    mock_cursor.fetchone.return_value = [False]
    update_meal_stats(1, "win")
    expected_update_sql = "UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?"
    actual_update_sql = mock_cursor.execute.call_args_list[1][0][0]
    assert actual_update_sql == expected_update_sql

def test_update_meal_stats_false(mock_cursor):
    """Test updating the stats of a meal by incrementing its loss and battles after a loss."""
    mock_cursor.fetchone.return_value = [False]
    update_meal_stats(1, "loss")
    expected_update_sql = "UPDATE meals SET battles = battles + 1, loss = loss + 1 WHERE id = ?"
    actual_update_sql = mock_cursor.execute.call_args_list[1][0][0]
    assert actual_update_sql == expected_update_sql
