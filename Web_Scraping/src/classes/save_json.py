import json

def price_to_json(dictionary):
    # Save to a JSON file
    file_name = f"Data/price/onion_price_{dictionary.get('price_dt')}.json"
    with open(file_name, 'w') as json_file:
        json.dump(dictionary, json_file, indent=2)

    print(f"JSON data with updated onion prices saved to {file_name}!")