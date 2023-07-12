import json
import os


def create_files_from_json(json_data, prefix='', directory='.'):
    for key, value in json_data.items():
        file_name = prefix + key.replace(" ", "_") + '.txt'
        file_path = os.path.join(directory, file_name)
        
        with open(file_path, 'w') as file:
            pass  # Creates an empty file
        
        if isinstance(value, dict):
            create_files_from_json(value, prefix + key + '_', directory)

# JSON data
json_data = {
    "Delivery": {
        "Missing_Package": {},
        "Damaged_Package": {},
        "Out_of_Stock": {}
    },
    "Product_Feedback": {
        "Taste_Feedback": {},
        "Satiation_Feedback": {},
        "Tolerance_Feedback": {}
    },
    "Product_Support": {
        "Texture_Questions": {},
        "Storage_Questions": {},
        "Product_Recommendations": {}
    },
    "Subscription": {
        "Cancellations": {},
        "Address_Changes": {},
        "Delivery_Date_Changes": {}
    },
    "Other": {}
}

# Directory to create the text files
directory = '.'

# Create the text files
create_files_from_json(json_data, directory=directory)
