from contextlib import contextmanager
import pytest

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

@pytest.fixture(autouse=True)
def setup_and_teardown_database():
    """Fixture to ensure a clean database state before and after each test."""
    clear_meals()
    yield
    clear_meals()

def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("meal_max.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor


##################################################
# Meal Creation and Initialization Test Cases
##################################################

def test_meal_initialization():
    """Test successful initialization of a Meal instance with valid parameters."""
    meal = Meal(id=1, meal="Truffle Risotto", cuisine="Italian-Fusion", price=22.08, difficulty="MED")
    assert meal.id == 1
    assert meal.meal == "Truffle Risotto"
    assert meal.cuisine == "Italian-Fusion"
    assert meal.price == 22.08
    assert meal.difficulty == "MED"


def test_meal_initialization_invalid_price():
    """Test initializing a meal with an invalid price raises ValueError."""
    with pytest.raises(ValueError, match="Price must be a positive value."):
        Meal(id=2, meal="Negative Price", cuisine="Italian", price=-5.0, difficulty="LOW")


def test_meal_initialization_invalid_difficulty():
    """Test initializing a meal with an invalid difficulty raises ValueError."""
    with pytest.raises(ValueError, match="Difficulty must be 'LOW', 'MED', or 'HIGH'."):
        Meal(id=3, meal="Invalid Difficulty", cuisine="French", price=25.0, difficulty="UNKNOWN")


def test_create_meal():
    """Test successfully creating a new meal entry in the database."""
    create_meal("Bangers and Mash", "British", 17.0, "MED")
    meal = get_meal_by_name("Bangers and Mash")
    assert meal.meal == "Bangers and Mash"
    assert meal.cuisine == "British"
    assert meal.price == 17.0
    assert meal.difficulty == "MED"


def test_create_duplicate_meal():
    """Test creating a duplicate meal raises ValueError."""
    create_meal("Bangers and Mash", "British", 17.0, "MED")
    with pytest.raises(ValueError, match="Meal with name 'Bangers and Mash' already exists"):
        create_meal("Bangers and Mash", "British", 17.0, "MED")


def test_create_meal_invalid_parameters():
    """Test creating a meal with invalid price or difficulty raises ValueError."""
    with pytest.raises(ValueError, match="Invalid price: -12.0. Price must be a positive number."):
        create_meal("Invalid Price", "Japanese", -12.0, "LOW")

    with pytest.raises(ValueError, match="Invalid difficulty level: UNKNOWN. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal("Invalid Difficulty", "Japanese", 19.0, "UNKNOWN")


##################################################
# Clear and Delete Meal Test Cases
##################################################

def test_clear_meals():
    """Test clearing all meals from the database."""
    create_meal("Chicken Masala", "Indian", 13.6, "LOW")
    clear_meals()
    with pytest.raises(ValueError, match="Meal with name 'Chicken Masala' not found"):
        get_meal_by_name("Chicken Masala")


def test_delete_meal():
    """Test deleting a meal and ensuring it cannot be retrieved."""
    create_meal("Soondaegook", "South Korean", 20.4, "HIGH")
    meal = get_meal_by_name("Soondaegook")
    delete_meal(meal.id)

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        get_meal_by_id(meal.id)


##################################################
# Leaderboard Retrieval Test Cases
##################################################

def test_get_leaderboard_by_wins():
    """Test retrieving the leaderboard sorted by wins."""
    create_meal("Sushi Omakase", "Japanese", 25.5, "MED")
    update_meal_stats(1, "win")
    leaderboard = get_leaderboard("wins")

    assert leaderboard[0]["meal"] == "Sushi Omakase"
    assert leaderboard[0]["wins"] == 1
    assert leaderboard[0]["win_pct"] == 100.0


def test_get_leaderboard_invalid_parameter():
    """Test invalid leaderboard sort parameter raises ValueError."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: invalid"):
        get_leaderboard("invalid")


##################################################
# Meal Retrieval Test Cases
##################################################

def test_get_meal_by_id():
    """Test retrieving a meal by its ID."""
    create_meal("Peking Duck", "Chinese", 33.98, "HIGH")
    meal = get_meal_by_name("Peking Duck")
    retrieved_meal = get_meal_by_id(meal.id)
    assert retrieved_meal.meal == "Peking Duck"


def test_get_meal_by_id_not_found():
    """Test retrieving a non-existent meal by ID raises ValueError."""
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)


def test_get_meal_by_name():
    """Test retrieving a meal by its name."""
    create_meal("Beef Wellington", "British", 40.8, "HIGH")
    meal = get_meal_by_name("Beef Wellington")
    assert meal.meal == "Beef Wellington"


def test_get_meal_by_name_not_found():
    """Test retrieving a non-existent meal by name raises ValueError."""
    with pytest.raises(ValueError, match="Meal with name 'NonExistent' not found"):
        get_meal_by_name("NonExistent")


##################################################
# Meal Stats Update Test Cases
##################################################

def test_update_meal_stats_with_win():
    """Test updating meal stats with a win result."""
    create_meal("Pho", "Vietnamese", 10.2, "LOW")
    meal = get_meal_by_name("Pho")

    update_meal_stats(meal.id, "win")
    updated_meal = get_meal_by_id(meal.id)

    assert updated_meal.wins == 1
    assert updated_meal.battles == 1


def test_update_meal_stats_with_loss():
    """Test updating meal stats with a loss result."""
    create_meal("Pho", "Vietnamese", 10.2, "LOW")
    meal = get_meal_by_name("Pho")

    update_meal_stats(meal.id, "loss")
    updated_meal = get_meal_by_id(meal.id)

    assert updated_meal.battles == 1
    assert updated_meal.wins == 0  # No wins should be added


def test_update_meal_stats_invalid_result():
    """Test updating meal stats with an invalid result raises ValueError."""
    create_meal("Pho", "Vietnamese", 10.2, "LOW")
    meal = get_meal_by_name("Pho")

    with pytest.raises(ValueError, match="Invalid result: invalid_result. Expected 'win' or 'loss'."):
        update_meal_stats(meal.id, "invalid_result")


def test_update_stats_for_deleted_meal():
    """Test updating stats for a deleted meal raises ValueError."""
    create_meal("Pho", "Vietnamese", 10.2, "LOW")
    meal = get_meal_by_name("Pho")
    delete_meal(meal.id)

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        update_meal_stats(meal.id, "win")
