import unittest
import pandas as pd
from src.normalization import normalize_sec_metrics, CANONICAL_SCHEMA

class TestNormalization(unittest.TestCase):
    def test_normalize_empty_df(self):
        """Verifies that an empty DataFrame result in an empty normalized output."""
        df = pd.DataFrame()
        result = normalize_sec_metrics(df)
        self.assertTrue(result.empty)

    def test_canonical_schema_mapping(self):
        """Verifies that SEC facts are correctly mapped to the wide-format canonical schema."""
        raw_records = [
            {"ticker": "NVDA", "fy": 2023, "fp": "Q1", "metric": "Revenues", "value": 1e9, "filed": "2023-01-01"},
            {"ticker": "NVDA", "fy": 2023, "fp": "Q1", "metric": "NetIncomeLoss", "value": 2e8, "filed": "2023-01-01"},
            {"ticker": "NVDA", "fy": 2023, "fp": "Q1", "metric": "NetCashProvidedByUsedInOperatingActivities", "value": 1.5e8, "filed": "2023-01-01"},
            {"ticker": "NVDA", "fy": 2023, "fp": "Q1", "metric": "Assets", "value": 5e9, "filed": "2023-01-01"}
        ]
        raw_df = pd.DataFrame(raw_records)
        norm_df = normalize_sec_metrics(raw_df)
        
        # Check columns
        self.assertIn("revenue", norm_df.columns)
        self.assertIn("net_income", norm_df.columns)
        self.assertIn("total_assets", norm_df.columns)
        
        # Check values
        self.assertEqual(norm_df.iloc[0]["revenue"], 1e9)
        self.assertEqual(norm_df.iloc[0]["net_income"], 2e8)
        self.assertEqual(norm_df.iloc[0]["total_assets"], 5e9)
        
        # Check types
        self.assertEqual(norm_df.iloc[0]["fiscal_year"], 2023)
        self.assertEqual(norm_df.iloc[0]["fiscal_quarter"], 1)

if __name__ == "__main__":
    unittest.main()
