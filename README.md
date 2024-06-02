# Weather Data Code Challenge

This project provides a RESTful API for accessing weather data and statistics. The API is built using Flask and Flask-RESTx, with data stored in a PostgreSQL database. 

## Features

- Retrieve weather data filtered by date and station ID.
- Retrieve weather statistics filtered by year and station ID.
- Paginated responses for large datasets.
- Structured logging with log rotation.
- Configurable settings through a config file.

## Project Structure

/weather-data-challenge

/config

config.ini

/src

app.py

connect_database.py

models.py

ingest_data.py

/wx_data

requirements.txt

README.md

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtualenv (optional but recommended)

## Setup

### Clone the Repository
```bash
git clone https://github.com/ManasaAddagatla/weather-data-challenge.git

cd weather-data-challenge
```

### Create and Activate Virtual Environment (Optional)
```bash
python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
## Configure the Application

- Update the config/config.ini file with your database credentials:

[database]

user = your_db_user

password = your_db_password

host = your_db_host

port = your_port_number

database = your_db_name

- Run the connect_database.py file:
```bash
python src/connect_database.py
```

Ensure connection to your PostgreSQL server has been established and that it is running.

- Run the models.py file:
```bash
python src/models.py
```
It creates the database in the PostgreSQL server if it does not exist, and creates two tables: weather_data and weather_statistics to store data.

- Run the ingest_data.py file:
```bash
python src/ingest_data.py
```
It should ingest data from wx_data into your database, which takes approximately 1 hour to run locally. It handles ingestion of duplicates, and also produces log output in a log file: ingestion.log.

- Run the weather_statistics.py file:
```bash
python src/weather_statistics.py
```
The weather_statistics table is updated with calculated statistics: 

- Average maximum temperature (in degrees Celsius)

- Average minimum temperature (in degrees Celsius)

- Total accumulated precipitation (in centimeters)

Missing data will be ignored while calculation.


## Run the Application
```bash
python src/app.py
```
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
```bash
python unit_tests.py
```
## Swagger UI
To interact with the API via a web interface, you can use the Swagger UI. Once the application is running, navigate to http://127.0.0.1:5000/ in your browser to access the Swagger documentation and try out the endpoints.
