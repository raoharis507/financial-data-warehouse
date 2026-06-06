import unittest
import requests

BASE_URL = "http://127.0.0.1:8000"

class TestFinancialDataWarehouse(unittest.TestCase):
    
    def test_health(self):
        response = requests.get(f"{BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")
    
    def test_q1_list_assets(self):
        response = requests.get(f"{BASE_URL}/api/assets")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
    
    def test_q2_asset_details(self):
        response = requests.get(f"{BASE_URL}/api/assets/AAPL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["assetId"], "AAPL")
    
    def test_q3_list_sources(self):
        response = requests.get(f"{BASE_URL}/api/sources")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
    
    def test_q5_timeseries(self):
        response = requests.get(f"{BASE_URL}/api/timeseries/AAPL/Nasdaq")
        self.assertEqual(response.status_code, 200)
    
    def test_analytics_moving_average(self):
        response = requests.get(f"{BASE_URL}/api/analytics/ma/AAPL/Nasdaq?days=5")
        self.assertEqual(response.status_code, 200)
        self.assertIn("moving_average", response.json())
    
    def test_analytics_forecast(self):
        response = requests.get(f"{BASE_URL}/api/analytics/forecast/AAPL/Nasdaq?days_ahead=3")
        self.assertEqual(response.status_code, 200)
        self.assertIn("predictions", response.json())
    
    def test_llm_assistant(self):
        response = requests.get(f"{BASE_URL}/api/assistant/ask?query=list%20assets")
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

if __name__ == "__main__":
    unittest.main()
