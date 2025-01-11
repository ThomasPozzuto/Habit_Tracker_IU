

from datetime import timedelta, datetime

def calculate_streak_days(completions):
    """
        Calculates the current and longest streak of consecutive days based on habit completion dates.

        Args:
            completions (list of tuples): A list of tuples where each tuple contains a single completion date
                                          as a string in ISO format.

        Returns:
            tuple: A tuple containing:
                - current_streak (int): The number of consecutive days up to the most recent completion date.
                - longest_streak (int): The maximum number of consecutive days with completions.
    """

    completions = [row[0] for row in completions]
    completions = [datetime.fromisoformat(date_str) for date_str in completions]
    if not completions:
        return 0, 0

    longest_streak = 1
    current_streak = 1
    unit_delta = timedelta(days=1)

    for i in range(1, len(completions)):
        delta = completions[i] - completions[i - 1]
        if delta <= unit_delta:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    return current_streak, longest_streak


def calculate_streak_weeks(completions):
    """
        Calculate the current and longest streak of weekly completions.

        Args:
            completions (list of int): A list of integers representing the week numbers
                                       (ISO week) when the habit was completed.

        Returns:
            tuple: A tuple containing two integers:
                - current_streak (int): The number of consecutive weeks in the current streak.
                - longest_streak (int): The longest streak of consecutive weeks.
     """

    completions = [row[0] for row in completions]
    completions = [datetime.fromisoformat(date_str) for date_str in completions]
    if not completions:
        return 0, 0

    longest_streak = 1
    current_streak = 1
    unit_delta = timedelta(weeks=1)

    for i in range(1, len(completions)):
        delta = completions[i] - completions[i - 1]
        if delta <= unit_delta:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    return current_streak, longest_streak

