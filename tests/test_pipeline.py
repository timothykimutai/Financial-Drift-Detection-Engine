import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.pipeline import QuantitativePipeline

class TestPipeline(unittest.TestCase):
    @patch('src.pipeline.fetch_raw_sec_data')
    @patch('src.pipeline.generate_visual_artifacts')
    def test_orchestration_flow(self, mock_viz, mock_fetch):
        """Verifies the complete integration flow from ingestion to final artifact persistence."""
        # 1. Mock raw ingestion
        mock_fetch.return_value = {
            "facts": {
                "us-gaap": {
                    "Revenues": {"units": {"USD": [{"val": 100, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-01-01"}]}},
                    "NetIncomeLoss": {"units": {"USD": [{"val": 20, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-01-01"}]}},
                    "Assets": {"units": {"USD": [{"val": 500, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-01-01"}]}},
                    "NetCashProvidedByUsedInOperatingActivities": {"units": {"USD": [{"val": 25, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-01-01"}]}},
                    "PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": [{"val": 5, "form": "10-Q", "fy": 2023, "fp": "Q1", "filed": "2023-01-01"}]}}
                }
            }
        }
        
        # 2. Execute pipeline
        pipeline = QuantitativePipeline()
        result = pipeline.run_ticker_analysis("MSFT")
        
        # 3. Assert functional completion
        self.assertIsNotNone(result)
        self.assertIn("drift_score", result.columns)
        self.assertIn("explanation", result.columns)
        self.assertEqual(result.iloc[0]["ticker"], "MSFT")

if __name__ == "__main__":
    unittest.main()
