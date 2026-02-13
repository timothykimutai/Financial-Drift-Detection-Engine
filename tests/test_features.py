import unittest
import pandas as pd
import numpy as np
from src.features import engineering_financial_features

class TestFeatures(unittest.TestCase):
    def test_feature_calculations(self):
        """Verifies that accounting ratios (FCF, Accruals) are correctly calculated."""
        data = {
            "ticker": ["AAPL"],
            "fiscal_year": [2023],
            "fiscal_quarter": [1],
            "revenue": [1e6],
            "net_income": [2e5],
            "operating_cash_flow": [2.5e5],
            "total_assets": [5e6],
            "accounts_receivable": [1e5],
            "share_based_compensation": [5e4],
            "capex": [5e4]
        }
        df = pd.DataFrame(data)
        feat_df = engineering_financial_features(df)
        
        # FCF: OCF - Capex = 2.5e5 - 5e4 = 2e5
        self.assertEqual(feat_df.iloc[0]["free_cash_flow"], 2e5)
        # Accrual Ratio: (NI - OCF) / Total Assets = (2e5 - 2.5e5) / 5e6 = -5e4 / 5e6 = -0.01
        self.assertAlmostEqual(feat_df.iloc[0]["accrual_ratio"], -0.01)

    def test_growth_clipping(self):
        """Verifies that extreme growth outliers are clipped to the GROWTH_LIMIT (±200%)."""
        data = {
            "ticker": ["TSLA", "TSLA"],
            "fiscal_year": [2023, 2023],
            "fiscal_quarter": [1, 2],
            "revenue": [100, 10000],  # 9900% growth -> should clip to 200% (2.0)
            "operating_cash_flow": [100, 2], # -98% growth -> within limit
            "net_income": [0, 0], "total_assets": [0, 0], "capex": [0, 0]
        }
        df = pd.DataFrame(data)
        feat_df = engineering_financial_features(df)
        
        # Revenue growth 99x should be clipped to 2.0
        self.assertEqual(feat_df.iloc[1]["revenue_growth"], 2.0)
        # OCF growth -98% (0.02 ratio) is -0.98
        self.assertAlmostEqual(feat_df.iloc[1]["ocf_growth"], -0.98)

if __name__ == "__main__":
    unittest.main()
