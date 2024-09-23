# animal_transform.py

from datetime import datetime, timezone # Import required modules for handling dates and times

def transform_friends(animal):
    """
    Transforms the 'friends' field in the animal dictionary.

    if the 'friends' field is present and not empty, it converts
    it from a comma-delimited string into a list. if the 'friends'
    field is not present or is empty, it sets it to an empty list.

    Args:
        animal (dict): A dictionary representing an animal.

    Returns:
        dict: The modified animal dictionary with 'friends' as a list.
    """  
    if 'friends' in animal:
        # Check if 'friends' is a string
        if instance(animal['friends'], str):
            # Split the friends string to a list
            animal['friends'] = animal['friends'].split(',')
        elif not isinstance(animal['friends'], list):
            animal['friends'] = []
    else:
        # If 'friends' is not present or is empty, initialize as an empty list
        animal['friends'] = []
    return animal

def transform_born_at(animal):
    """
    Transforms the 'born_at' field in the animal dictionary.

    if the 'born_at' field is populated, it converts the timestamp (assumed to be in milliseconds)
    into an ISO8601 formatted string in UTC. 
    if 'born_at' is not populated, it remains unchanged.

    Args:
        animal (dict): A dictionary representing an animal.

    Return:
        dict: The modified animal dictionary with 'born_at' as an ISO8601 string
    """
    if 'born_at' in animal and animal['born_at'] is not None:
        try:
            timestamp = animal['born_at'] / 1000 # Convert milliseconds to seconds
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)# Convert to a datetime in UTC
            animal['born_at'] = dt.isoformat() # Convert datetime to ISO8601
        except (TypeError, valueError):
            #To handle when conversion fails
            animal['born_at'] = None
    return animal

def transform_all_animals(animals): # Transorm a list of all animals
    return [transform_born_at(transform_friends(animal)) for animal in animals]

