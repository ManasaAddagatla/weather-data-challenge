"""
Module: app.py

This module implements a Flask-based RESTful API for accessing weather data and statistics.

The API provides endpoints to retrieve weather data and weather statistics with filtering and 
pagination options. It uses Flask-RESTx to define and document the API endpoints. Swagger UI is 
integrated to allow interactive documentation and exploration of the API.

Usage:
    To run the API, execute this script:
        python app.py

    Before running the script, make sure to configure the database connection from connect_database.py 
    and adjust any default pagination parameters as needed.

Notes:
    - Pagination: The API supports pagination for large datasets to improve performance and reduce response times. 
      The default page size is set to 10 items per page, but this can be adjusted using the 'page_size' parameter.
    - Error Handling: The API handles errors gracefully and returns appropriate HTTP status codes and error messages 
      in case of invalid requests or server errors.
    - Swagger UI: The API is documented using Swagger UI, which provides interactive documentation and allows users 
      to explore and test the API endpoints directly from their web browser.

Dependencies:
    - Flask: A micro web framework for building web applications in Python.
    - Flask-RESTx: An extension for Flask that adds support for quickly building REST APIs.
    - SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python, used for database operations.
    - models: Module containing SQLAlchemy models for weather data and statistics.
    - connect_database: Module containing functions to establish a connection to the database.
"""

from flask import Flask
from flask_restx import Api, Resource, fields
from models import WeatherData, WeatherStatistics
from connect_database import get_session

# Create a Flask application instance
app = Flask(__name__)

# Create a Flask-RESTx API instance with versioning and basic information
api = Api(app, version='1.0', title='Weather API', description='API for weather data')

# Define default pagination parameters for listing resources
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

# Create a namespace for weather data operations in the API
weather_ns = api.namespace('weather', description='Weather data operations')

# Define input model for filtering weather data using Flask-RESTx parser
weather_filter_model = api.parser()
weather_filter_model.add_argument('date', type=str, help='Date in YYYY-MM-DD format', location='args')
weather_filter_model.add_argument('station_id', type=str, help='Weather station ID', location='args')
weather_filter_model.add_argument('page', type=int, help='Page number', location='args', default=DEFAULT_PAGE)
weather_filter_model.add_argument('page_size', type=int, help='Number of items per page', location='args', default=DEFAULT_PAGE_SIZE)

# Define output model for weather data
weather_model = api.model('WeatherData', {
    'id': fields.Integer(description='Unique ID'),
    'date': fields.Date(description='Date in YYYY-MM-DD format'),
    'station_id': fields.String(description='Weather station ID'),
    'max_temp': fields.Float(description='Maximum temperature'),
    'min_temp': fields.Float(description='Minimum temperature'),
    'precipitation': fields.Float(description='Precipitation')
})

@weather_ns.route('/')

class WeatherAPI(Resource):
    """
    Resource class for handling weather data API requests.

    Attributes:
        None

    Methods:
        get(self): Retrieves weather data based on provided filters and pagination parameters.
    """
    # Declare the expected input model for endpoint
    @weather_ns.expect(weather_filter_model)
    
    # Define the output model to format response data
    @weather_ns.marshal_with(weather_model, as_list=True)
    
    def get(self):
        """
        Retrieve weather data based on provided filters and pagination parameters.

        This method handles HTTP GET requests to retrieve weather data based on optional query parameters.
        It parses the query parameters provided in the request and constructs a query to retrieve the matching data from the database.
        Supports filtering by date and weather station ID, and provides pagination for large result sets.

        Returns:
            tuple: A tuple containing a list of weather data objects and pagination metadata.
                   The list contains weather data objects retrieved from the database.
                   The pagination metadata includes total items, current page, and page size.

        Example:
            An HTTP GET request to /weather/?date=2003-01-01&station_id=USC00111280&page=1&page_size=10
            will retrieve weather data for the date '2003-01-01', station ID 'USC00111280', with pagination applied.
        """
        # Parse request arguments
        args = weather_filter_model.parse_args()
        date = args.get('date')
        station_id = args.get('station_id')
        page = args.get('page')
        page_size = args.get('page_size')
        
        # Create a query object to retrieve weather data
        query = get_session().query(WeatherData)

        # Apply filters based on request parameters
        if date:
            query = query.filter(WeatherData.date == date)
        if station_id:
            query = query.filter(WeatherData.station_id == station_id)

        # Perform pagination
        total_items = query.count()
        query = query.limit(page_size).offset((page - 1) * page_size)

        # Execute the query and format response data
        return query.all(), {'total_items': total_items, 'page': page, 'page_size': page_size}

# Namespace for weather statistics endpoints
stats_ns = api.namespace('weather/stats', description='Weather statistics operations')

# Define input model for filtering weather statistics
stats_filter_model = api.parser()
stats_filter_model.add_argument('year', type=int, help='Year', location='args')
stats_filter_model.add_argument('station_id', type=str, help='Weather station ID', location='args')
stats_filter_model.add_argument('page', type=int, help='Page number', location='args', default=DEFAULT_PAGE)
stats_filter_model.add_argument('page_size', type=int, help='Number of items per page', location='args', default=DEFAULT_PAGE_SIZE)

# Define output model for weather statistics
stats_model = api.model('WeatherStatistics', {
    'year': fields.Integer(description='Year'),
    'station_id': fields.String(description='Weather station ID'),
    'avg_max_temp': fields.Float(description='Average maximum temperature'),
    'avg_min_temp': fields.Float(description='Average minimum temperature'),
    'total_precipitation': fields.Float(description='Total precipitation')
})

@stats_ns.route('/')

class WeatherStatsAPI(Resource):
    """
    Represents an endpoint for retrieving weather statistics.

    This class defines a Flask-RESTx resource for handling HTTP GET requests to retrieve weather statistics.
    It expects optional query parameters for filtering the statistics by year, weather station ID, and supports pagination.

    Attributes:
        None
    """
    # Specify the input model for this endpoint
    @stats_ns.expect(stats_filter_model)
    
    # Specify the output model for this endpoint
    @stats_ns.marshal_with(stats_model, as_list=True)

    def get(self):
        """
        Retrieve weather statistics.

        This method handles HTTP GET requests to retrieve weather statistics based on optional query parameters.
        It parses the query parameters provided in the request and constructs a query to retrieve the matching statistics from the database.
        Supports filtering by year and weather station ID, and provides pagination for large result sets.

        Returns:
            tuple: A tuple containing a list of weather statistics objects and pagination metadata.
                   The list contains weather statistics objects retrieved from the database.
                   The pagination metadata includes total items, current page, and page size.

        Example:
            An HTTP GET request to /weather/stats/?year=1991&station_id=USC00110072&page=1&page_size=10
            will retrieve weather statistics for the year 1991, station ID 'USC00110072', with pagination applied.
        """
        # Parse the arguments provided in the request
        args = stats_filter_model.parse_args()
        
        # Get the values of parameters
        year = args.get('year')
        station_id = args.get('station_id')
        page = args.get('page')
        page_size = args.get('page_size')
        
        # Start building the query to retrieve weather statistics from database
        query = get_session().query(WeatherStatistics)

        # If year parameter is provided, filter the query by year
        if year:
            query = query.filter(WeatherStatistics.year == year)
        
        # If station_id parameter is provided, filter the query by station_id
        if station_id:
            query = query.filter(WeatherStatistics.station_id == station_id)

         # Perform pagination
        total_items = query.count()
        query = query.limit(page_size).offset((page - 1) * page_size)

        # Return query result along with pagination metadata
        return query.all(), {'total_items': total_items, 'page': page, 'page_size': page_size}

if __name__ == '__main__':
    # Run the Flask application in debug mode if this script is executed directly
    app.run(debug=True)