import sqlite3
from datetime import datetime, timedelta
import random

####################
#db connection var
####################

conn = sqlite3.connect('habits.db') # Connect to habits.db - creates habits.db if not exists
conn.execute("PRAGMA foreign_keys = ON;")# enable foreign key constraints

###################
#sample data var
###################

today = datetime.now().date()
start = today - timedelta(weeks=4)  # Default start date is 4 weeks ago for sample habits

###################
#SQL´s as var
###################

ADD_HABIT = """
    INSERT INTO habits (name, frequency, created_at)
    VALUES (?, ?, ?)
"""

DELETE_HABIT = """
    DELETE FROM habits
    WHERE name = ?
"""

ADD_COMPLETION = """
    INSERT INTO completions (id, completed_at)
    VALUES (
        (SELECT id FROM habits WHERE name = ?), ?
    )
"""

GET_HABITS = """
    SELECT
        h.name,
        h.frequency,
        h.created_at,
        MAX(c.completed_at) AS last_completed_at
    FROM habits h
    LEFT JOIN completions c ON c.id = h.id
    GROUP BY h.name, h.frequency, h.created_at
"""

GET_COMPLETIONS = """
    SELECT completed_at
    FROM completions
    WHERE id = (
        SELECT id FROM habits WHERE name = ?
    )
"""

GET_MAX_COMPLETION_DATE = """
    SELECT MAX(completed_at)
    FROM completions
    WHERE id = (
        SELECT id FROM habits WHERE name = ?
    )
"""

##########################################################################################################
#start sample data construction
##########################################################################################################
"""
Creates the sample habits starting 4 weeks ago.

- used to populate the habits.db with sample data

habit_1 : random completion for the first 10 days only, daily frequency
habit_2 : completion for all days, daily frequency
habit_3 : random completion for all days, daily frequency
habit_4 : random completion for each Monday, weekly frequency
habit_5 : completion for each Monday, weekly frequency

"""
# List of sample habits for habits in habits.db
single_habits = [
    ['habit_1', 'daily', start.isoformat()],
    ['habit_2', 'daily', start.isoformat()],
    ['habit_3', 'daily', start.isoformat()],
    ['habit_4', 'weekly', start.isoformat()],
    ['habit_5', 'weekly', start.isoformat()],
]

# Generate completion records for completions in habits.db
completion_samples = []
for i in range((today - start).days):
    completion_date = start + timedelta(days=i)
    week_num = completion_date.isocalendar()[1]

    if random.choice([True, False]) and i < 10:
        completion_samples.append(['habit_1', completion_date.isoformat()])
    completion_samples.append(['habit_2', completion_date.isoformat()])
    if random.choice([True, False]):
        completion_samples.append(['habit_3', completion_date.isoformat()])
    if completion_date.weekday() == 0 and random.choice([True, False]):
        completion_samples.append(['habit_4', completion_date.isoformat()])
    if completion_date.weekday() == 0:
        completion_samples.append(['habit_5', completion_date.isoformat()])


##########################################################################################################
#end sample data construction
##########################################################################################################


def create_and_populate_db():
    """
    Creates the habits database and populates it with sample data, if it already exits it just connects
     - creates `habits` and `completions`
    """
    cursor = conn.cursor()

    # Create the `habits` table
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE,
                        frequency TEXT,
                        created_at TEXT NOT NULL)''')

    # Create the `completions` table
    cursor.execute('''CREATE TABLE IF NOT EXISTS completions (
                        id INTEGER,
                        completed_at TEXT NOT NULL,

                        FOREIGN KEY (id) REFERENCES habits (id) ON DELETE CASCADE)''')

    conn.commit()

    # Check if the `habits` table is empty
    cursor.execute("SELECT COUNT(*) FROM habits")
    if cursor.fetchone()[0] == 0:
        # Populate `habits` table
        cursor.executemany("INSERT INTO habits (name, frequency, created_at) VALUES (?, ?, ?)", single_habits)

        # Populate `completions` table
        cursor.executemany("""INSERT INTO completions (id, completed_at)
                              VALUES ((SELECT id FROM habits WHERE name = ?), ?)""",
                           completion_samples)
        conn.commit()


def execute_query(query, params=(), fetch=False):
    """
    Executes a SQL query with optional parameters.

    Args:
        query (str): The SQL query to execute.
        params (tuple): Parameters to bind to the query.
        fetch (bool): Whether to fetch results.

    Returns:
        list or None: Query results if fetch=True, else None.
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    if fetch:
        return cursor.fetchall()
    else:
        return []
    cursor.close()