import logging
import requests
from meal_max.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

def get_random() -> float:
    """
    Fetches a random decimal number from random.org.

    This function makes a GET request to random.org to retrieve a single random
    decimal number with two decimal places. The response is parsed and converted
    to a float before being returned.

    Returns:
        float: A random decimal number between 0.00 and 1.00.

    Raises:
        ValueError: If the response from random.org is invalid or not a number.
        RuntimeError: If the request to random.org times out or fails.

    Logs:
        INFO: Logs the URL request to random.org and the received random number.
        ERROR: Logs if the request to random.org fails or if the response is invalid.

    """
    url = "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new"

    try:
        # Log the request to random.org
        logger.info("Fetching random number from %s", url)

        response = requests.get(url, timeout=5)

        # Check if the request was successful
        response.raise_for_status()

        random_number_str = response.text.strip()

        try:
            # Attempt to convert the response to a float
            random_number = float(random_number_str)
        except ValueError:
            raise ValueError("Invalid response from random.org: %s" % random_number_str)

        # Log the received random number
        logger.info("Received random number: %.3f", random_number)
        return random_number

    except requests.exceptions.Timeout:
        # Log and raise error if the request timed out
        logger.error("Request to random.org timed out.")
        raise RuntimeError("Request to random.org timed out.")

    except requests.exceptions.RequestException as e:
        # Log and raise error if the request failed
        logger.error("Request to random.org failed: %s", e)
        raise RuntimeError("Request to random.org failed: %s" % e)
