# main.py

import logging 

#Import required functions from other modules
from animal_fetch import fetch_total_pages,fetch_all_animals
from animal_transform import transform_all_animals
from animal_post import post_all_animals, batch_animals

def main():
    """
    Main function to fetch, transform and post the animals
    """
    total_pages = fetch_total_pages() # fetch the total number of pages from API

    if total_pages >0: # Check if there are any pages to fetch
        animals = fetch_all_animals(total_pages) #Fetch all animals
        if animals:
            transformed_animals = transform_all_animals(animals) # Transform the fetched data
            post_all_animals(transformed_animals) # Post the data
        else:
            logging.error("No animals fetched.")
    else:
        logging.error("Failed to get the total number of pages.")

if __name__ == '__main__':
    main()

