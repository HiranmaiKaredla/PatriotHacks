import http.client
import json
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv("ATTOM_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please make sure it is set in the .env file.")

WAIT_TIMEOUT = 2
PAGE_SIZE = 10  # Fetch only 2 properties

# Get properties list from Attom API using ZIP code
def get_avm_for_zip(zip_code):
    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")
    headers = {
        'accept': "application/json",
        'apikey': API_KEY  # API key from .env file
    }

    page = 1
    # Build the query using ZIP code, page, and page size (2 in this case)
    query = f"/propertyapi/v1.0.0/property/address?postalcode={zip_code}&page={page}&pagesize={PAGE_SIZE}"
    conn.request("GET", query, headers=headers)

    res = conn.getresponse()
    data = res.read()
    response = json.loads(data.decode("utf-8"))

    if response.get('status', {}).get('code') != 0:
        print(f"Failed to retrieve data for ZIP: {zip_code}")
        return None

    conn.close()
    return response

# Print the full JSON response and save it to a file
def print_and_save_json_response(response, file_name="property_data_final.json"):
    if response:
        # Print the JSON data in a formatted way
        print(json.dumps(response, indent=4))
        
        # Save the JSON response to a file
        with open(file_name, "w") as json_file:
            json.dump(response, json_file, indent=4)
        print(f"JSON data has been saved to {file_name}")

def execute():
    # Only querying ZIP code 22030
    ZIP_CODE_TO_QUERY = "22030"  # Fairfax, VA

    # Query and get 2 properties from Attom API
    avm_api_results = get_avm_for_zip(ZIP_CODE_TO_QUERY)

    # Print and save the JSON response
    print_and_save_json_response(avm_api_results)

if __name__ == "__main__":
    execute()
