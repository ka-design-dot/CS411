import pytest
import requests
from meal_max.utils.random_utils import get_random
from unittest.mock import Mock

# Define a constant for a mock random number to be used in tests
RANDOM_NUMBER = 0.57  # Example random number

@pytest.fixture
def mock_random_org(mocker):
    """Fixture to mock requests.get for successful random.org response."""
    # Create a mock response object and set the text attribute to our constant
    mock_response = Mock()
    mock_response.text = f"{RANDOM_NUMBER}"
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org):
    """Test retrieving a random decimal from random.org."""
    result = get_random()

    # Assert that the result matches the mocked random number
    assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"

    # Verify the requests.get call with the correct URL
    requests.get.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new",
        timeout=5
    )

def test_get_random_request_failure(mocker):
    """Test behavior when a request to random.org fails."""
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

def test_get_random_timeout(mocker):
    """Test behavior when a request to random.org times out."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

def test_get_random_invalid_response(mock_random_org):
    """Test behavior when random.org returns an invalid response."""
    mock_random_org.text = "invalid_response"  # Set the response to something invalid

    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()
