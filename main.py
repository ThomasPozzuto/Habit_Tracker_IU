#main.py

from database_and_sql import create_and_populate_db
from interface import HabitTrackerApp
import tkinter as tk

# Initialize database and app
create_and_populate_db()

# Launch UI
root = tk.Tk()
app = HabitTrackerApp(root)
root.mainloop()