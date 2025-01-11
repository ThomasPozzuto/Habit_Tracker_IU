import tkinter as tk
from datetime import timedelta, datetime
from tkinter import ttk, messagebox
from streak_calculation import calculate_streak_days, calculate_streak_weeks
from classes import Habit, Tracker



class HabitTrackerApp:
    """
    A tkinter application for tracking habits with features to add, delete, mark as completed, and view habits by frequency (daily, weekly).
    """

    def __init__(self, root):
        """
        Initializes the HabitTrackerApp with the main tkinter window, creates the UI widgets, and loads the habits into the Treeview.

        Args:
            root (tk.Tk): The main tkinter window.
        """
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("1200x600")  # Adjust window size for better layout


        self.create_widgets()

        # Load habits into the Treeview
        self.load_habits()

    def create_widgets(self):
        """
        Creates the UI components including header buttons, habit list Treeview and buttons
        """
        # Top Frame for Header Buttons
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # show all / daily / weekly
        tk.Button(self.top_frame, text="All habits", width=15, command=self.show_all_habits).pack(side=tk.LEFT, padx=5)
        tk.Button(self.top_frame, text="Daily habits", width=15, command=self.show_daily_habits).pack(side=tk.LEFT,padx=5)
        tk.Button(self.top_frame, text="Weekly habits", width=15, command=self.show_weekly_habits).pack(side=tk.LEFT,padx=5)


        # Quit
        tk.Button(self.top_frame, text="Quit Tracker", width=15, command=self.root.quit).pack(side=tk.RIGHT, padx=10)

        # Center Frame for Treeview and Buttons
        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        # Treeview table (left)
        self.table_frame = tk.Frame(self.center_frame)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = (
        "tracked_since", "name", "frequency", "current_streak", "longest_streak", "last_completion", "habit_state")
        self.habit_tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=10)
        self.habit_tree.pack(fill=tk.BOTH, expand=True)

        # Define headings for the table
        self.habit_tree.heading("tracked_since", text="Tracked Since")
        self.habit_tree.heading("name", text="Name")
        self.habit_tree.heading("frequency", text="Frequency")
        self.habit_tree.heading("current_streak", text="Current Streak")
        self.habit_tree.heading("longest_streak", text="Longest Streak")
        self.habit_tree.heading("last_completion", text="Last Completion")
        self.habit_tree.heading("habit_state", text="State of Habit")

        # Define column widths
        self.habit_tree.column("tracked_since", width=100, anchor='center')
        self.habit_tree.column("name", width=150, anchor='center')
        self.habit_tree.column("frequency", width=100, anchor='center')
        self.habit_tree.column("current_streak", width=100, anchor='center')
        self.habit_tree.column("longest_streak", width=100, anchor='center')
        self.habit_tree.column("last_completion", width=100, anchor='center')
        self.habit_tree.column("habit_state", width=150, anchor='center')

        # add / delete / complete
        self.button_frame = tk.Frame(self.center_frame)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        tk.Button(self.button_frame, text="Complete habit", width=15, command=self.complete_habit).pack(pady=10)
        tk.Button(self.button_frame, text="Add new habit", width=15, command=self.add_habit).pack(pady=10)
        tk.Button(self.button_frame, text="Delete habit", width=15, command=self.delete_habit).pack(pady=10)

    def load_habits(self):
        """
        Clears the existing entries in the Treeview and loads habits from the HabitTracker, then populates the Treeview with the habit details.
        """
        # clear all
        for row in self.habit_tree.get_children():
            self.habit_tree.delete(row)

        # fetch all habits
        habits = Tracker.get_all_habits()

        for habit in habits:
            habit_name, frequency, created_at, last_at = habit


            completions_days = Tracker.get_completion_days(habit_name)
            current_streak_days, longest_streak_days = calculate_streak_days(completions_days)

            # habit state computing daily
            if frequency == 'daily':
                yesterday = datetime.now().date() - timedelta(days=1)
                last_compl = datetime.fromisoformat(last_at).date() if last_at else None

                if last_compl < yesterday:
                    habit_state = "Habit Broken"
                    current_streak_days = 0
                else:
                    habit_state = "Streak - Keep on Going!"

            else:
                #habit state computing weekly
                completions_weeks = Tracker.get_completion_days(habit_name)
                current_streak_weeks, longest_streak_weeks = calculate_streak_weeks(completions_weeks)


                last_completion_date = datetime.fromisoformat(last_at) if last_at else None
                if last_completion_date:
                    last_completion_week = last_completion_date.isocalendar()[1]
                    last_week = datetime.now().isocalendar()[1] - 1


                    if last_completion_week < last_week:
                        habit_state = "Habit Broken"
                        current_streak_weeks = 0
                    else:
                        habit_state = "Streak - Keep on Going!"
                else:
                    habit_state = "Habit Broken"
            #insert to tree
            self.habit_tree.insert(
                "",
                tk.END,
                values=(
                    created_at, habit_name, frequency,
                    current_streak_days if frequency == 'daily'
                    else current_streak_weeks,
                    longest_streak_days if frequency == 'daily'
                    else longest_streak_weeks,
                    last_at, habit_state
                )
            )

    def complete_habit(self):
        """
        Marks the selected habit as completed and updates the habit list in the Treeview.
        Displays a message if the habit is already completed on the current day or week.
        """
        selected_item = self.habit_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a habit to mark as completed.")
            return

        habit_name = self.habit_tree.item(selected_item, "values")[1]
        habit_frequency = self.habit_tree.item(selected_item, "values")[2]


        habit = Habit(name=habit_name, frequency=habit_frequency)
        # Get the list of completed days for the habit
        last_completion = Tracker.last_completion_date(habit_name)

        # Get current date and week number for completion check
        current_date = datetime.now().date()
        current_week = datetime.now().isocalendar()[1]

        if habit.frequency == 'daily':
            if last_completion:
                completion_date = datetime.fromisoformat(last_completion).date()
                if current_date == completion_date:
                    messagebox.showinfo("Info", f"Habit '{habit_name}' already completed today!")
                    return
        elif habit.frequency == 'weekly':
            if last_completion:
                completion_week = datetime.fromisoformat(last_completion).isocalendar()[1]
                if current_week == completion_week:
                    messagebox.showinfo("Info", f"Habit '{habit_name}' already completed this week!")
                    return

        # Add completion if not already completed
        habit.add_completion()
        # reload
        self.load_habits()
        messagebox.showinfo("Success", f"Habit '{habit_name}' completed!")


    def add_habit(self):
        """
        Opens a new window to add a new habit with a name and frequency (daily or weekly).
        """
        new_window = tk.Toplevel(self.root)
        new_window.title("Add New Habit")
        new_window.geometry("300x200")

        tk.Label(new_window, text="Habit Name:").pack(pady=5)
        name_entry = tk.Entry(new_window)
        name_entry.pack(pady=5)

        tk.Label(new_window, text="Choose Frequency:").pack(pady=5)

        # Dropdown menu for selecting frequency
        frequency_var = tk.StringVar(new_window)
        frequency_var.set("daily")  # daily as default
        frequency_menu = ttk.Combobox(new_window, textvariable=frequency_var, values=["daily", "weekly"],
                                      state="readonly")
        frequency_menu.pack(pady=5)

        def save_habit():
            """
            Handles the process of saving a new habit and its first completion.
            Shows warning if habit not named and prevents saving without name.
            """
            habit_name = name_entry.get()
            frequency = frequency_var.get()
            if habit_name and frequency:

                # Create a new habit and add it to the database and adds first completion
                new_habit = Habit(name=habit_name, frequency=frequency)
                new_habit.add_new()
                new_habit.add_completion()

                messagebox.showinfo("Success",
                                    f"Habit '{habit_name}' added successfully with its first completion!")
                new_window.destroy()
                self.load_habits()

            else:
                messagebox.showerror("Error", "Please enter all fields.")

        # Save button
        tk.Button(new_window, text="Save", command=save_habit).pack(pady=10)

    def delete_habit(self):
        """
        Deletes the selected habit from the list and updates the habit list in the Treeview.
        Prompts the user to confirm deletion.
        """
        selected_item = self.habit_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a habit to delete.")
            return

        habit_name = self.habit_tree.item(selected_item, "values")[1]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{habit_name}'?")
        if confirm:
                habit = Habit(name=habit_name, frequency=None)
                habit.delete()
                self.load_habits()
                messagebox.showinfo("Success", f"Habit '{habit_name}' deleted successfully!")


    def show_all_habits(self):
        """
        Displays all habits in the Treeview.
        """
        self.load_habits()

    def show_daily_habits(self):
        """
        Filters and displays daily habits in the Treeview.
        """
        self.filter_habits_by_frequency("daily")

    def show_weekly_habits(self):
        """
        Filters and displays weekly habits in the Treeview.
        """
        self.filter_habits_by_frequency("weekly")

    def filter_habits_by_frequency(self, frequency):
        """
        Filters habits by frequency (daily or weekly) and displays them in the Treeview.
        Determines habit state for displaying.


        Args:
            frequency (str): The frequency to filter by ("daily" or "weekly").
        """
        # Clear the Treeview
        for row in self.habit_tree.get_children():
            self.habit_tree.delete(row)

        # Fetch all habits from the Tracker
        habits = Tracker.get_all_habits()

        for habit in habits:
            habit_name, habit_frequency, created_at, last_at = habit
            if habit_frequency != frequency:
                continue

            # Fetch completions and calculate streaks
            completions = Tracker.get_completion_days(habit_name)
            if habit_frequency == 'daily':
                current_streak, longest_streak = calculate_streak_days(completions)

                # Determine the state of the habit
                yesterday = datetime.now().date() - timedelta(days=1)
                last_compl = datetime.fromisoformat(last_at).date() if last_at else None

                if not last_compl or last_compl < yesterday:
                    habit_state = "Habit Broken"
                    current_streak = 0
                else:
                    habit_state = "Streak - Keep on Going!"

            else:  # Weekly habits
                current_streak, longest_streak = calculate_streak_weeks(completions)

                # Determine the state of the habit
                last_completion_date = datetime.fromisoformat(last_at) if last_at else None
                if last_completion_date:
                    last_completion_week = last_completion_date.isocalendar()[1]
                    last_week = datetime.now().isocalendar()[1] - 1  # Last week's ISO week number

                    if last_completion_week < last_week:
                        habit_state = "Habit Broken"
                        current_streak = 0
                    else:
                        habit_state = "Streak - Keep on Going!"
                else:
                    habit_state = "Habit Broken"

            # Insert the habit into the Treeview
            self.habit_tree.insert(
                "",
                tk.END,
                values=(
                    created_at, habit_name, habit_frequency,
                    current_streak, longest_streak, last_at, habit_state
                )
            )
