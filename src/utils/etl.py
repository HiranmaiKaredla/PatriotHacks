import pandas as pd
import requests
import time
import os
from tqdm import tqdm
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

# Get Azure Maps subscription key from the .env file
AZURE_MAPS_KEY = os.getenv('AZURE_MAPS_KEY')

if not AZURE_MAPS_KEY:
    raise ValueError("Azure Maps subscription key not found. Please add it to the .env file.")

def extract_data(file_path):
    """
    Extract data from CSV file into a pandas DataFrame.
    :param file_path: str, path to the CSV file
    :return: DataFrame
    """
    try:
        data = pd.read_csv(file_path, sep=";", encoding='latin1')
        print(f"Data loaded successfully with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def reverse_geocode_azure(lat, lon, retries=3, backoff_factor=1):
    """
    Reverse geocoding using Azure Maps API with retries and exponential backoff.
    :param lat: float, latitude
    :param lon: float, longitude
    :param retries: int, number of retry attempts
    :param backoff_factor: float, factor for exponential backoff delay
    :return: str, postal code (zip code) or None
    """
    url = f"https://atlas.microsoft.com/search/address/reverse/json"
    params = {
        'api-version': '1.0',
        'subscription-key': AZURE_MAPS_KEY,
        'language': 'en-US',
        'query': f"{lat},{lon}"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if data and 'addresses' in data and data['addresses']:
                return data['addresses'][0]['address'].get('postalCode', None)
        except requests.exceptions.RequestException as e:
            print(f"Error during reverse geocoding attempt {attempt + 1}/{retries}: {e}")
            time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error: {e}")
    return None

def fetch_zip_code(row):
    """
    Helper function to fetch the zip code for a given row.
    This function is used in parallel execution.
    """
    if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
        zip_code = reverse_geocode_azure(row['latitude'], row['longitude'])
        return zip_code
    return None

def transform_data(df, max_workers=10):
    """
    Transform data by handling missing values, adding zip codes, and converting data types for the first 1000 rows.
    Uses concurrent processing to speed up the reverse geocoding process.
    :param df: DataFrame
    :param max_workers: int, number of threads to use for concurrent API calls
    :param limit: int, number of rows to process
    :return: Cleaned DataFrame.
    """
    print("Initial DataFrame info:\n")
    print(df.info())

    # Add a new column for zip codes
    df['zip_code'] = None

    # Limit the processing to the first 'limit' rows (in this case, 1000)
    df_limited = df

    # Process the first 1000 rows in the dataset using concurrent execution
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use tqdm to display a progress bar
        futures = {executor.submit(fetch_zip_code, row): idx for idx, row in df_limited.iterrows()}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing rows"):
            idx = futures[future]
            try:
                zip_code = future.result()
                if zip_code:
                    print(f"Row {idx + 1} - Latitude: {df.at[idx, 'latitude']}, Longitude: {df.at[idx, 'longitude']}, Zip Code: {zip_code}")
                df.at[idx, 'zip_code'] = zip_code
            except Exception as e:
                print(f"Error processing row {idx + 1}: {e}")

    # Resetting the index after cleaning
    df_clean = df_limited.reset_index(drop=True)

    print(f"\nCleaned data has {df_clean.shape[0]} rows and {df_clean.shape[1]} columns.")
    return df_clean

def load_data(df, output_file):
    """
    Load cleaned data into a CSV file or a database.
    :param df: DataFrame
    :param output_file: str, output file path for the cleaned data
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}.")
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    input_file = '../../data/apartments_for_rent_classified_100K.csv'  
    output_file = '../../data/final-data.csv'  

    df = extract_data(input_file)

    if df is not None:
        df_clean = transform_data(df, max_workers=10)  # Process the first 1000 rows
        load_data(df_clean, output_file)
