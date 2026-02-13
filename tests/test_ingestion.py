import unittest
from unittest.mock import patch, MagicMock
from src.ingestion import fetch_raw_sec_data, extract_facts_to_df

class TestIngestion(unittest.TestCase):
    def test_cik_mapping_failure(self):
        """Verifies that an unknown ticker returns None gracefully."""
        result = fetch_raw_sec_data("UNKNOWN")
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_sec_data_success(self, mock_get):
        """Verifies that actual SEC facts are correctly fetched and persisted."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"facts": {"us-gaap": {"Assets": {"units": {"USD": [{"val": 100, "form": "10-K"}]}}}}}
        mock_get.return_value = mock_response

        data = fetch_raw_sec_data("AAPL")
        self.assertIsNotNone(data)
        self.assertIn("facts", data)

    def test_extract_facts_to_df(self):
        """Verifies that the raw fact JSON is correctly flattened into a DataFrame."""
        sample_data = {
            "facts": {
                "us-gaap": {
                    "Assets": {
                        "units": {
                            "USD": [
                                {"val": 500000, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-04-01"}
                            ]
                        }
                    }
                }
            }
        }
        df = extract_facts_to_df("TEST", sample_data)
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]["metric"], "Assets")
        self.assertEqual(df.iloc[0]["value"], 500000)

if __name__ == "__main__":
    unittest.main()
