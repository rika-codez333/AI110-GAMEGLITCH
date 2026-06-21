import sys
import unittest
from unittest.mock import MagicMock

# app.py calls streamlit at import time; stub it so we can import the
# pure logic under test without a real Streamlit runtime.
_st = MagicMock()
# selectbox's return value is used as a dict key, so give it a real string.
_st.sidebar.selectbox.return_value = "Normal"
_st.checkbox.return_value = True
# columns() is unpacked into three values.
_st.columns.return_value = (MagicMock(), MagicMock(), MagicMock())
sys.modules.setdefault("streamlit", _st)

from app import get_range_for_difficulty, check_guess, update_score


class TestCheckGuessHints(unittest.TestCase):
    def test_guess_too_high_returns_go_lower(self):
        outcome, message = check_guess(80, 50)
        self.assertEqual(outcome, "Too High")
        self.assertIn("LOWER", message)

    def test_guess_too_low_returns_go_higher(self):
        outcome, message = check_guess(20, 50)
        self.assertEqual(outcome, "Too Low")
        self.assertIn("HIGHER", message)


class TestDifficultyRanges(unittest.TestCase):
    def test_easy_range(self):
        self.assertEqual(get_range_for_difficulty("Easy"), (1, 20))

    def test_normal_range(self):
        self.assertEqual(get_range_for_difficulty("Normal"), (1, 50))

    def test_hard_range(self):
        self.assertEqual(get_range_for_difficulty("Hard"), (1, 100))


class TestUpdateScoreWinFixed(unittest.TestCase):
    def test_win_on_first_attempt_awards_90(self):
        # Option B fix: formula is now 100 - 10 * attempt_number (no +1).
        # First guess → attempt_number=1 → 100 - 10 = 90 points.
        score = update_score(current_score=0, outcome="Win", attempt_number=1)
        self.assertEqual(score, 90)

    def test_win_on_ninth_attempt_hits_minimum_floor(self):
        # attempt_number=9 → 100 - 90 = 10, which equals the floor exactly.
        # attempt_number=10 → 100 - 100 = 0 → clamped to 10.
        # Both should return the 10-point minimum, not 0 or negative.
        score_9  = update_score(0, "Win", attempt_number=9)
        score_10 = update_score(0, "Win", attempt_number=10)
        self.assertEqual(score_9, 10)
        self.assertEqual(score_10, 10)

    def test_win_attempt_number_zero_raises(self):
        # attempt_number=0 or negative is a programming mistake — fail loud.
        with self.assertRaises(ValueError):
            update_score(0, "Win", attempt_number=0)


if __name__ == "__main__":
    unittest.main()
