"""
Module: weather_statistics

This script is responsible for calculating weather statistics for every year, for every weather station 
based on weather data stored in a database.

It includes functions to calculate average maximum temperature, average minimum temperature, and total precipitation
for each year and each weather station in the database. The calculated statistics are then stored in the database.

The script logs information about the statistics calculation process, including errors and the duration of the process.

Usage:
    python weather_statistics.py

Make sure to configure the database connection from connect_database.py before running the script.
"""

from datetime import datetime
import logging
from sqlalchemy import extract, func
from connect_database import get_session
from models import WeatherData, WeatherStatistics

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Establish a session with the database
session = get_session()

def calculate_statistics():
    """
    Calculate yearly statistics for weather data and store them in the database.
    """

    # Get the current time to measure the duration of calculation
    start_time = datetime.now()
    logger.info(f'Starting statistics calculation at {start_time}')

    # Start a session to interact with the database
    with get_session() as session:
        try:
            # Query to calculate yearly statistics for each weather station
            query = session.query(
                extract('year', WeatherData.date).label('year'),
                WeatherData.station_id,
                func.avg(WeatherData.max_temp).label('avg_max_temp'),
                func.avg(WeatherData.min_temp).label('avg_min_temp'),
                func.sum(WeatherData.precipitation).label('total_precipitation')
            ).group_by(WeatherData.station_id, extract('year', WeatherData.date))
            
            # Iterate over query results to create WeatherStatistics objects
            for result in query:
                yearly_stat = WeatherStatistics(
                    year=result.year,
                    station_id=result.station_id,
                    avg_max_temp=result.avg_max_temp,
                    avg_min_temp=result.avg_min_temp,
                    total_precipitation=result.total_precipitation
                )
                # Add each WeatherStatistics object to the session for bulk insertion
                session.add(yearly_stat)

            # Commit the session to persist changes in the database
            session.commit()

            # Record the end time of calculation
            end_time = datetime.now()
            
            # Log the completion of calculation and the duration
            logger.info(f'Finished statistics calculation at {end_time}, duration: {end_time - start_time}')
        
        except Exception as e:
            # If an error occurs during the calculation, rollback the session to maintain data integrity
            session.rollback()
            # Log the error
            logger.error(f'Error calculating statistics: {e}')

def main():
    """
    Main function to execute the statistics calculation.
    """
    calculate_statistics()

    session.close()

if __name__ == "__main__":
    main()
