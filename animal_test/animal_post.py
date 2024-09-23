# animal_post.py

import requests # Import the requests library for making HTTP requests
import time # Import time for sleep functionality during retries
import logging # Import logging for logging messages and errors
from concurrent.futures import ThreadPoolExecutor # Import for multi executions

# Add logging to show messages for severe errors
logging.basicConfig(level=logging.INFO)

def batch_animals(animals, batch_size=100):
    """
    yields batches of animals from the input

    it splits the list of animals into smaller batches

    Args:
        animals (list): A list of animal dictionaries
        batch_size (int): The size of each batch ( default value is 100 )

    Yields:
        list: A group of animal dictionaries.
    """
    for i in range(0, len(animals), batch_size):
        yield animals[i:i + batch_size]

def post_animals_retry(batch, retries=5):
    """
    Posts a batch of animals to the URL with retry logic.

    In case of posting error, it retries number of times as we provided

    Args:
        batch (list): To post the batch of animals
        retries (int): number of attempts ( default is set to 5)
    Returns:
        int: The number of animals that are posted or 0 if it fails
    """
    url = 'http://localhost:3123/animals/v1/home' # Define the API endpoint to post the animals
    incr = 2 # Increase in time wait between retries

    for i in range(retries):
        try:
            # Log that batch thats being posted
            logging.info(f"Posting batch: {batch}")
            # creaete a request to the URL with the animal list
            response = requests.post(url, json=batch, timeout=20)
            if response.status_code == 200:
                # Log success if the request pass
                logging.info(f"Posted batch of {len(batch)} animals successfully")
                return len(batch) # Return the number of animals sent
            elif response.status_code in (500, 502, 503, 504):
                # Log server errors and apply the increase in time wait 
                logging.error(f"Server error {response.status_code} while posting batch. Retrying...")
                time.sleep(5 * (incr ** i))
            else:
                # log other errors and retry
                logging.error(f"Error {response.status_code} while posting batch: {response.text}. Retrying...")
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            #Log any request exceptions and retry
            logging.error(f"Request failed: {e}. Retrying...")
            time.sleep(5 * (incr ** i))

    return 0

def post_all_animals(animals):
    """
    Post all animals

    Args:
        animals(list): list of animals to post
    """
    total_posted = 0 # Initialize counter
    # Use ThreadPoolExecutor to post same time
    with ThreadPoolExecutor(max_workers=2) as worker:
        futures = {worker.submit(post_animals_retry, batch): batch for batch in batch_animals(animals)}
        for future in futures:
            try:
                # Wait for the result, this might raise an exception if the posting failed
                posted_count = future.result()
                total_posted += posted_count # Collect total number of animals posted
            except Exception as e:
                logging.error(f"Error posting batch: {e}")
    # Log the total number of animals posted
    logging.info(f"Total animals posted: {total_posted}")

