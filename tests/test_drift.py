import unittest
import pandas as pd
from src.drift import calculate_momentum_scores, derive_drift_signal

class TestDrift(unittest.TestCase):
    def test_momentum_and_drift_derivation(self):
        """Verifies the derivation of drift from narrative and financial momentum components."""
        data = {
            "ticker": ["NVDA"],
            "fiscal_year": [2023],
            "fiscal_quarter": [1],
            "revenue_growth": [0.1],
            "ocf_growth": [0.2],
            "accrual_ratio_delta": [0.0],
            "optimism": [0.8],
            "risk": [10],
            "optimism_delta": [0.2],
            "risk_delta": [0]
        }
        df = pd.DataFrame(data)
        
        mom_df = calculate_momentum_scores(df)
        drift_df = derive_drift_signal(mom_df)
        
        # Check that scores exist
        self.assertIn("financial_momentum", drift_df.columns)
        self.assertIn("narrative_momentum", drift_df.columns)
        self.assertIn("drift_score", drift_df.columns)
        
        # Verify basic physics: drift = nar_mom - fin_mom
        expected_drift = drift_df.iloc[0]["narrative_momentum"] - drift_df.iloc[0]["financial_momentum"]
        self.assertAlmostEqual(drift_df.iloc[0]["drift_score"], expected_drift)

if __name__ == "__main__":
    unittest.main()
