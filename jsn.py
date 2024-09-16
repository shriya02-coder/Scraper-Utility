import json

def search_json(json_data, search_query, return_field):
    """
    Function to search through the JSON data and return the value of a specified field
    based on the search query.
    
    Parameters:
    json_data (list): List of dictionaries parsed from a JSON file.
    search_query (dict): The fields and their values to search for.
    return_field (str): The field whose value needs to be returned.

    Returns:
    list: A list of values from the matching records.
    """
    results = []
    
    for record in json_data:
        match = True
        # Check if all search criteria match
        for key, value in search_query.items():
            if key in record and record[key] != value:
                match = False
                break
        if match and return_field in record:
            results.append(record[return_field])
    
    return results

# Example usage:
if __name__ == "__main__":
    # Load the JSON data from a file
    with open('data.json', 'r') as file:
        json_data = json.load(file)

    # Define search query and field to return
    search_query = {'name': 'example_name', 'pair': 'example_pair'}
    return_field = 'value'

    # Call the function
    matched_values = search_json(json_data, search_query, return_field)

    # Print the result
    if matched_values:
        print("Matched Values:", matched_values)
    else:
        print("No match found.")