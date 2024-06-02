import unittest
from app import app

class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_weather_data_no_filter(self):
        response = self.app.get('/weather/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get_weather_data_with_filter(self):
        response = self.app.get('/weather/?date=2003-06-01&station_id=USC00110072')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get_weather_stats_no_filter(self):
        response = self.app.get('/weather/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get_weather_stats_with_filter(self):
        response = self.app.get('/weather/stats/?year=1991&station_id=USC00110087')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
