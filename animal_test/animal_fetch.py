# animal_fetch.py

import requests # Importing the time module for sleep functionality
import time # Importing requests for making HTTP requests
import logging # Importing logging for logging info and errors
from concurrent.futures import ThreadPoolExecutor, as_completed # For concurrent processing of HTTP requests

#Adding logging to display level INFO
logging.basicConfig(level=logging.INFO)

def fetch_animals_retry(page=1, retries=5):
    """
    In case of failure, to fetch the animal data from the APi with retries.

    Parameters:
    - page (int): The page number to fetch.
    - retries (int): In case of failure, the number of retries.

    Returns:
    - dict: JSON response from the API having animal data, or None in case of failure.
    """

    incr = 2 # Increase in time wait between retries
    for i in range(retries):
        try:
            # GET request from the particular page to fetch animals
            response = requests.get(f'http://localhost:3123/animals/v1/animals?page={page}', timeout=20)
            if response.status_code == 200: # If the response is succesful
                logging.info(f"{page} fetched page sucessfully")
                return response.json() # Return the JSON response
            elif response.status_code in (500, 502, 503, 504): # If server error occur
                logging.error(f"On page {page} server error {response.status_code}. Retrying in {i+1}/{retries}...")
                time.sleep(5 * (incr ** i)) # wait before retrying
            else: # For other HTTP errors
                logging.error(f"On page {page} Error {response.status_code}. Retrying in {i+1}/{retries}...")
                time.sleep(5) # Wait before retrying
        except requests.exceptions.RequestException as e: # Handle any request exceptions
            logging.error(f"On page {page} request failed: {e}. Retrying {i+1}/{retries}...")
            time.sleep(5 * (incr ** i)) #Wait before retrying
    logging.error(f"page {page} failed to fetch after {retries} retries.")
    return None # Return None if fetching fails after all retries

def fetch_all_animals(total_pages, max=10):
    """
    To fetch all animals

    Parameters:
    - total_pages (int): Total number of pages to fetch.
    - max (int): Maximum number of threads to use at same time.

    Returns:
    - list: List of all animal.
    """
    all_animals = [] # List to store all animals.
    with ThreadPoolExecutor(max_workers=10) as worker:
    # Creating a dictionary to map future animals to their corresponding page numbers
        future_page = {worker.submit(fetch_animals_retry, page): page for page in range(1, total_pages + 1)}
        for future in as_completed(future_page): #Iterate over completed futures
            page = future_page[future] # Get the page number associated with the future
            try:
                data = future.result() # Get the result of the future
                if data and 'items' in data: #check if data is valid and contains 'items'
                    all_animals.extend(data['items']) #Add items to the List
                    logging.info(f"page {page} processed succesfully")
                else:
                    logging.error(f"For page {page} no data returned, retry may have failed.")
            except Exception as e: # Handle any exceptions that occur during getting the data
                logging.error(f"page {page} fetching failed with error: {e}")
        logging.info(f"Total animals fetched: {len(all_animals)}") #Log the total number of animals got
        return all_animals # Return the list

def fetch_total_pages():
    """

    Fetch the total number of pages in API.

    Returns:
    - int: The total number of pages, or 0 if fetching fails.
    """
    data = fetch_animals_retry(page=1) # Get the first page to know toatal pages
    if data and 'total_pages' in data: # Check if the response is valid and contains total_pages
        logging.info(f"First page data: {data}") # Log the first page data for checking
        total_pages = data['total_pages'] # Extract the total pages
        logging.info(f"Total pages reported by the API: {total_pages}")
        return total_pages # Return the total number of pages
    else:
        logging.error("Failed to get the first page or total pages not found.")
        return 0 # Return 0 if fetching fails
