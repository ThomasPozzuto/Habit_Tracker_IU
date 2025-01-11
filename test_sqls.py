import unittest
import sqlite3
from datetime import datetime
from database_and_sql import ADD_HABIT, DELETE_HABIT, ADD_COMPLETION, GET_HABITS, GET_COMPLETIONS, GET_MAX_COMPLETION_DATE

class TestHabitDatabase(unittest.TestCase):


    def setUp(self):
        """Set up an in-memory SQLite database and create tables."""
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.connection.cursor()

        # Create tables
        self.cursor.execute('''CREATE TABLE habits (
                                id INTEGER PRIMARY KEY,
                                name TEXT UNIQUE,
                                frequency TEXT,
                                created_at TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE completions (
                                id INTEGER,
                                completed_at TEXT NOT NULL,
                                FOREIGN KEY (id) REFERENCES habits (id) ON DELETE CASCADE)''')

        self.connection.commit()

    def tearDown(self):
        """Close the database connection after each test."""
        self.connection.close()

    def test_add_habit(self):
        """Test adding a habit to the database."""
        habit_name = "Exercise"
        frequency = "daily"
        created_at = datetime.now().isoformat()

        self.cursor.execute(ADD_HABIT, (habit_name, frequency, created_at))
        self.connection.commit()

        # Verify the habit was added
        self.cursor.execute("SELECT name, frequency, created_at FROM habits WHERE name = ?", (habit_name,))
        habit = self.cursor.fetchone()
        self.assertEqual(habit, (habit_name, frequency, created_at))

    def test_delete_habit(self):
        """Test deleting a habit from the database."""
        self.cursor.execute(ADD_HABIT, ("Exercise", "daily", datetime.now().isoformat()))
        self.connection.commit()

        # Delete the habit
        self.cursor.execute(DELETE_HABIT, ("Exercise",))
        self.connection.commit()

        # Verify the habit was deleted
        self.cursor.execute("SELECT * FROM habits WHERE name = ?", ("Exercise",))
        self.assertIsNone(self.cursor.fetchone())

    def test_add_completion(self):
        """Test adding a completion for a habit."""
        self.cursor.execute(ADD_HABIT, ("Exercise", "daily", datetime.now().isoformat()))
        self.connection.commit()

        completed_at = datetime.now().isoformat()
        self.cursor.execute(ADD_COMPLETION, ("Exercise", completed_at))
        self.connection.commit()

        # Verify the completion was added
        self.cursor.execute("""SELECT completed_at FROM completions
                               WHERE id = (SELECT id FROM habits WHERE name = ?)""", ("Exercise",))
        completion = self.cursor.fetchone()
        self.assertEqual(completion[0], completed_at)

    def test_get_habits(self):
        """Test retrieving all habits."""
        self.cursor.execute(ADD_HABIT, ("Exercise", "daily", datetime.now().isoformat()))
        self.cursor.execute(ADD_HABIT, ("Read", "weekly", datetime.now().isoformat()))
        self.connection.commit()

        self.cursor.execute(GET_HABITS)
        habits = self.cursor.fetchall()

        # Verify both habits are retrieved
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0][0], "Exercise")
        self.assertEqual(habits[1][0], "Read")

    def test_get_completions(self):
        """Test retrieving completions for a specific habit."""
        self.cursor.execute(ADD_HABIT, ("Exercise", "daily", datetime.now().isoformat()))
        completed_at = datetime.now().isoformat()
        self.cursor.execute(ADD_COMPLETION, ("Exercise", completed_at))
        self.connection.commit()

        self.cursor.execute(GET_COMPLETIONS, ("Exercise",))
        completions = self.cursor.fetchall()

        # Verify the correct completion is retrieved
        self.assertEqual(len(completions), 1)
        self.assertEqual(completions[0][0], completed_at)

    def test_get_max_completion_date(self):
        """Test retrieving the latest completion date for a specific habit."""
        self.cursor.execute(ADD_HABIT, ("Exercise", "daily", datetime.now().isoformat()))
        completed_at_1 = "2024-12-29T10:00:00"
        completed_at_2 = "2024-12-30T10:00:00"
        self.cursor.execute(ADD_COMPLETION, ("Exercise", completed_at_1))
        self.cursor.execute(ADD_COMPLETION, ("Exercise", completed_at_2))
        self.connection.commit()

        self.cursor.execute(GET_MAX_COMPLETION_DATE, ("Exercise",))
        max_date = self.cursor.fetchone()

        # Verify the latest completion date
        self.assertEqual(max_date[0], completed_at_2)


if __name__ == '__main__':
    unittest.main()
