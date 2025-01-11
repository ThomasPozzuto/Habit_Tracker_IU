from database_and_sql import conn
from datetime import datetime

from database_and_sql import GET_HABITS, GET_COMPLETIONS, GET_MAX_COMPLETION_DATE, execute_query

class Habit:
    """
    Represents a habit in the tracker.

    Attributes:
        name (str): The name of the habit.
        frequency (str): Frequency of the habit ('daily' or 'weekly').
        created_at (str): The creation date of the habit in ISO format.
        completed_at (str): The most recent completion date.
    """

    def __init__(self, name, frequency, created_at=None, completed_at=None):

        self.name = name
        self.frequency = frequency
        self.created_at = created_at or datetime.now().date().isoformat()
        self.completed_at = completed_at

    def add_new(self):
        """
        Adds a new habit to the database.
        """
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habits (name, frequency, created_at) VALUES (?, ?, ?)",
                       (self.name, self.frequency, self.created_at))
        conn.commit()

    def add_completion(self):
        """
        Adds a completion record for the habit.
        """
        self.completed_at = datetime.now().date().isoformat()


        cursor = conn.cursor()
        cursor.execute("INSERT INTO completions (id, completed_at) VALUES "
                       "((SELECT id FROM habits WHERE name = ?), ?)",
                       (self.name, self.completed_at))
        conn.commit()

    def delete(self):
        """
        Deletes the habit and its completions from the database.
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habits WHERE name = ?", (self.name,))
        conn.commit()

class Tracker:
    """
    Handles tracking and retrieval of habits and their completions.
    """

    @staticmethod
    def get_all_habits():
        """
        Retrieves all habits with their details.

        Returns:
            list: List of tuples containing habit details.
        """
        return execute_query(GET_HABITS, fetch=True)

    @staticmethod
    def get_completion_days(habit_name):
        """
        Retrieves completion dates for a specific habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            list: List of completion dates.
        """
        return execute_query(GET_COMPLETIONS, (habit_name,), fetch=True)

    @staticmethod
    def last_completion_date(habit_name):
        """
        Retrieves the last completion date for a specific habit.

        Returns:
            str: Last completion date.
        """
        result = execute_query(GET_MAX_COMPLETION_DATE, (habit_name,), fetch=True)
        return result[0][0] if result else None
