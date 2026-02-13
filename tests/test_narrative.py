import unittest
from src.narrative import NarrativeProcessor

class TestNarrative(unittest.TestCase):
    def test_transcript_cleaning(self):
        """Verifies that speaker metadata and excessive whitespace are removed."""
        proc = NarrativeProcessor()
        raw = "John Doe: Hello. \n\n Operator: Instructions here."
        clean = proc.clean_and_persist("TEST", "Q1 2023", raw)
        self.assertIn("Hello", clean)
        self.assertNotIn("John Doe:", clean)
        self.assertNotIn("Operator:", clean)

    def test_baseline_extraction(self):
        """Verifies that a baseline signal is returned when no LLM client is active."""
        proc = NarrativeProcessor(api_key="invalid")
        signals = proc.extract_signals("Some text")
        self.assertIn("optimism", signals)
        self.assertEqual(signals["optimism"], 0.0)

if __name__ == "__main__":
    unittest.main()
