"""
Module: models

This module handles data management tasks related to creation of database and tables.

It provides functionality to create and manage a PostgreSQL database for storing weather data,
defines SQLAlchemy ORM models for weather-related tables, and sets up logging for monitoring
the execution of database-related tasks.

Dependencies:
    - psycopg2
    - sqlalchemy
"""

import logging
import psycopg2
from psycopg2 import sql
from sqlalchemy import UniqueConstraint, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
# Importing the database engine from database.py
from connect_database import engine 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database name
DB_NAME = 'weather_db'

def create_database():
    """
    Creates a PostgreSQL database if it doesn't exist.
    """
    # Connection parameters
    conn_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME])
        exists = cursor.fetchone()
        
        if not exists:
            # Create the database if it does not exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            logger.info(f"Database '{DB_NAME}' created successfully.")
        else:
            logger.info(f"Database '{DB_NAME}' already exists.")
    except psycopg2.Error as e:
        logger.error("Error creating database: %s", e)
    finally:
        if conn:
            conn.close()

# Define a base class for ORM models
Base = declarative_base()

# Define the model for weather data
class WeatherData(Base):
    """
    ORM model representing weather data.
    """
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    station_id = Column(String, nullable=False)
    max_temp = Column(Float, nullable=True)
    min_temp = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint('station_id', 'date', name='station_date_uc'),
    )
    
class WeatherStatistics(Base):
    """
    ORM model representing weather statistics data.
    """
    __tablename__ = 'weather_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    station_id = Column(String, nullable=False)
    avg_max_temp = Column(Float, nullable=True)
    avg_min_temp = Column(Float, nullable=True)
    total_precipitation = Column(Float, nullable=True)

if __name__ == "__main__":
    create_database()
    # Creating the database engine and tables 
    Base.metadata.create_all(engine)