# Weather Data Code Challenge

This project provides a RESTful API for accessing weather data and statistics. The API is built using Flask and Flask-RESTx, with data stored in a PostgreSQL database. The answers to questions part of the code challenge can be found in answers/answers.docx.

## Features

- Retrieve weather data filtered by date and station ID.
- Retrieve weather statistics filtered by year and station ID.
- Paginated responses for large datasets.
- Structured logging.
- Configurable settings through a config file.

## Project Structure

```bash
/weather-data-challenge
│
├── /config
│   └── config.ini # Configuration file for database connection settings.
│
├── /src
│   ├── app.py # Main Flask application file containing API endpoints.
│   ├── connect_database.py # Module for establishing connection to the database.
│   ├── models.py # Defines the database schema and ORM models.
│   ├── ingest_data.py # Script for ingesting weather data into the database.
│   ├── weather_statistics.py # Script for calculating weather statistics and storing them in database.
│   └── unit_tests.py # Unit tests for testing the functionality of the application. 
│
├── /wx_data # Directory containing raw weather data files.
│
├── README.md # This file provides an overview of the project, its structure, setup and implementation.
│
└── requirements.txt # List of Python dependencies required for the project.
```
## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtualenv (optional but recommended)

## Setup

### Clone the Repository

	git clone https://github.com/ManasaAddagatla/weather-data-challenge.git

	cd weather-data-challenge
### Create and Activate Virtual Environment (Optional)

	python -m venv venv

	source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install Dependencies

	pip install -r requirements.txt

## Configure the Application

#### Update the config/config.ini file with your database credentials:

	[database]
	user = your_db_user
	password = your_db_password
	host = your_db_host
	port = your_port_number
	database = your_db_name
#### Run the connect_database.py file:

	python src/connect_database.py

Ensure connection to your PostgreSQL server has been established and that it is running.

#### Run the models.py file:

	python src/models.py

It creates the database in the PostgreSQL server if it does not exist, and creates two tables: weather_data and weather_statistics to store data.

#### Run the ingest_data.py file:

	python src/ingest_data.py

It should ingest data from wx_data into your database, which takes approximately 1 hour to run locally for entire data. It handles ingestion of duplicates, and also produces log output in a log file: ingestion.log.

#### Run the weather_statistics.py file:

	python src/weather_statistics.py

The weather_statistics table is updated with calculated statistics: 

- Average maximum temperature (in degrees Celsius)

- Average minimum temperature (in degrees Celsius)

- Total accumulated precipitation (in centimeters)

Missing data will be ignored while calculation.

## Run the Application

	python src/app.py

## Usage

### Endpoints:

#### Get Weather Data

URL: /weather/

Method: GET

Query Parameters:

date (optional): Filter by date (YYYY-MM-DD).

station_id (optional): Filter by weather station ID.

#### Get Weather Statistics

URL: /weather/stats/

Method: GET

Query Parameters:

year (optional): Filter by year.

station_id (optional): Filter by weather station ID.

## Testing
To run tests, run the unit_test.py:

	python src/unit_tests.py

## Swagger UI
To interact with the API via a web interface, you can use the Swagger UI. Once the application is running, navigate to http://127.0.0.1:5000/ in your browser to access the Swagger documentation and try out the endpoints.
