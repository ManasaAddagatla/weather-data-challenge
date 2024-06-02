"""
Module: ingest_data

This script is responsible for ingesting weather data from raw text files into a database.

It includes functions to parse and clean the weather data, as well as to ingest the cleaned data
into a database using SQLAlchemy. 

The script logs information about the ingestion process, including errors, duplicates, 
and the duration of the process into a log file.

Usage:
    python ingest_data.py

Make sure to configure the database connection from connect_database.py and file paths before running the script.
"""

import os
import glob
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import numpy as np
from sqlalchemy.exc import IntegrityError
from connect_database import get_session
from models import WeatherData

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config log file
LOG_FILE = os.path.join(script_dir, 'ingestion.log')
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Path to the weather data files
DATA_PATH = os.path.join(script_dir, '..', 'wx_data')

def parse_weather_data(file_path):
    """
    Parse and clean weather data from a file.

    Args:
        file_path (str): Path to the weather data file.

    Returns:
        pd.DataFrame: Parsed and cleaned weather data.
    """
    # Read data from file
    data = pd.read_csv(file_path, delimiter='\t', header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])
    
    # Replace missing values with NULL
    data.replace(-9999, None, inplace=True)  
    
    # Convert date in raw text to datetime format
    data['date'] = pd.to_datetime(data['date'], format='%Y%m%d', errors='coerce')
    
    # Extract station ID from file name
    station_id=os.path.basename(file_path).split('.')[0]

    # Convert temperature and precipitation units
    data['max_temp'] = np.where(pd.notnull(data['max_temp']), data['max_temp'] / 10.0, None)
    data['min_temp'] = np.where(pd.notnull(data['min_temp']), data['min_temp'] / 10.0, None)
    data['precipitation'] = np.where(pd.notnull(data['precipitation']), data['precipitation'] / 10.0, None)
    
    # Add station ID to the DataFrame
    data['station_id'] = station_id
    
    return data


def ingest_data():
    """
    Ingest weather data into the database.
    """
    # Establish a session with the database
    session = get_session()

    # Record the start time of ingestion process
    main_start_time = datetime.now()
    logger.info(f'Starting ingestion at {main_start_time}')

    # Get a list of all weather data files in the specified directory
    files = glob.glob(os.path.join(DATA_PATH, '*.txt'))

    # Initialize counters for total records and duplicates found
    total_record_count = 0
    total_duplicate_count = 0

    # Iterate through each weather data file
    for file_path in files:
        file_name = os.path.basename(file_path)

        # Record the start time of ingestion process for current file
        start_time = datetime.now()
        logger.info(f"Starting ingestion of data from file: {file_name} at {start_time}")

        # Parse and clean the data from the current file
        data = parse_weather_data(file_path)

        # Initialize counters for records and duplicates found in the current file
        record_count = 0
        duplicate_count = 0  

        # Iterate through each row of data in the current file
        for _, row in data.iterrows():
            # Create a WeatherData object from the current row
            record = WeatherData(
                station_id=row['station_id'],
                date=row['date'],
                max_temp=row['max_temp'],
                min_temp=row['min_temp'],
                precipitation=row['precipitation']
            )
            try:
                # Add the record to the session and commit the transaction
                session.add(record)
                session.commit()
                record_count += 1
            except IntegrityError:
                # If a duplicate record is found, rollback the transaction
                session.rollback()
                duplicate_count += 1
        
        # Record the end time of ingestion process for current file
        end_time = datetime.now()
        logger.info(f'Finished ingestion at {end_time}, duration: {end_time - start_time}')

        # Log the number of records inserted from the current file
        logger.info(f"Number of records inserted from {file_name}: {record_count}")

        # Update total record and duplicate counts
        total_record_count += record_count
        total_duplicate_count += duplicate_count
    
    # Log the total number of duplicates found during ingestion
    logger.info(f"Total number of duplicates found: {total_duplicate_count}")  

    # Record the end time of ingestion process
    main_end_time = datetime.now()

    # Log the completion of ingestion process along with its duration
    logger.info(f'Finished ingestion at {main_end_time}, duration: {main_end_time - main_start_time}')
    logger.info(f'Total number of records ingested: {total_record_count}')

def main():
    """
    Main function to perform data ingestion.
    """
    ingest_data()

if __name__ == "__main__":
    main()