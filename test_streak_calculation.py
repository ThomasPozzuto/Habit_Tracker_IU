import unittest
from streak_calculation import calculate_streak_days, calculate_streak_weeks


class TestStreakCalculations(unittest.TestCase):

    def test_calculate_streak_days_empty(self):
        """Test calculate_streak_days with no completions."""
        completions = []
        self.assertEqual(calculate_streak_days(completions), (0, 0))

    def test_calculate_streak_days_single_completion(self):
        """Test calculate_streak_days with a single completion."""
        completions = [("2024-12-12",)]
        self.assertEqual(calculate_streak_days(completions), (1, 1))

    def test_calculate_streak_days_consecutive(self):
        """Test calculate_streak_days with consecutive days."""
        completions = [("2024-12-10",), ("2024-12-11",), ("2024-12-12",)]
        self.assertEqual(calculate_streak_days(completions), (3, 3))

    def test_calculate_streak_days_non_consecutive(self):
        """Test calculate_streak_days with non-consecutive days."""
        completions = [("2024-12-10",), ("2024-12-12",), ("2024-12-14",)]
        self.assertEqual(calculate_streak_days(completions), (1, 1))

    def test_calculate_streak_days_mixed(self):
        """Test calculate_streak_days with mixed consecutive and non-consecutive days."""
        completions = [("2024-12-10",), ("2024-12-11",), ("2024-12-13",), ("2024-12-14",)]
        self.assertEqual(calculate_streak_days(completions), (2, 2))

    def test_calculate_streak_days_longest(self):
        """Test calculate_streak_days for identifying the longest streak."""
        completions = [("2024-12-10",), ("2024-12-11",), ("2024-12-12",), ("2024-12-15",), ("2024-12-16",)]
        self.assertEqual(calculate_streak_days(completions), (2, 3))

    def test_calculate_streak_weeks_empty(self):
        """Test calculate_streak_weeks with no completions."""
        completions = []
        self.assertEqual(calculate_streak_weeks(completions), (0, 0))

    def test_calculate_streak_weeks_single_completion(self):
        """Test calculate_streak_weeks with a single completion."""
        completions = [("2024-12-10",)]  # Week 50
        self.assertEqual(calculate_streak_weeks(completions), (1, 1))

    def test_calculate_streak_weeks_consecutive(self):
        """Test calculate_streak_weeks with consecutive weeks."""
        completions = [
            ("2024-12-10",),  # Week 50
            ("2024-12-17",),  # Week 51
            ("2024-12-24",),  # Week 52
        ]
        self.assertEqual(calculate_streak_weeks(completions), (3, 3))

    def test_calculate_streak_weeks_non_consecutive(self):
        """Test calculate_streak_weeks with non-consecutive weeks."""
        completions = [
            ("2024-12-10",),  # Week 50
            ("2024-12-24",),  # Week 52
            ("2025-01-07",),  # Week 2
        ]
        self.assertEqual(calculate_streak_weeks(completions), (1, 1))

    def test_calculate_streak_weeks_mixed(self):
        """Test calculate_streak_weeks with mixed consecutive and non-consecutive weeks."""
        completions = [
            ("2024-12-10",),  # Week 50
            ("2024-12-17",),  # Week 51
            ("2024-12-31",),  # Week 1 (non-consecutive)
            ("2025-01-07",),  # Week 2
        ]
        self.assertEqual(calculate_streak_weeks(completions), (2, 2))

    def test_calculate_streak_weeks_longest(self):
        """Test calculate_streak_weeks for identifying the longest streak."""
        completions = [
            ("2024-12-10",),  # Week 50
            ("2024-12-17",),  # Week 51
            ("2024-12-24",),  # Week 52
            ("2025-01-14",),  # Week 3 (non-consecutive)
            ("2025-01-21",),  # Week 4
        ]
        self.assertEqual(calculate_streak_weeks(completions), (2, 3))


if __name__ == '__main__':
    unittest.main()
