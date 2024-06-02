"""
Module for managing SQLAlchemy database connections to PostgreSQL database.
"""

import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the config file
config_path = os.path.join(script_dir, '..', 'config', 'config.ini')

# Initialize and read the configuration
config = configparser.ConfigParser()
config.read(config_path)

# Database configuration
db_user = config['database']['user']
db_password = config['database']['password']
db_host = config['database']['host']
db_port = config['database']['port']
db_name = config['database']['database']

# Connection string
CONNECTION_STRING = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create engine and session
engine = create_engine(CONNECTION_STRING, echo=False)
Session = sessionmaker(bind=engine)

def get_session():
    """
    Function to get a new session object for interacting with the database.

    Returns:
        sqlalchemy.orm.Session: A new session object.
    """
    return Session()
