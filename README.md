# Habit_Tracker_IU

This repostery holds a habit tracker written in phyton version 3.13.1.

A Python-based habit tracking application to help users efficiently track and manage daily and weekly habits. This project includes a user-friendly Tkinter interface and a robust SQLite database to store habit data, calculate streaks, and provide instant feedback on habit performance.



#

Features:

 - Track daily and weekly habits.
 - Streak calculation for continuous habit completion.
 - Visual feedback on habit states.
 - Automatic sample data generation for testing.
 - User-friendly interface built with Tkinter.
 - Persistent data storage using SQLite.

#

Instalation and Starting:

To use the tracker, copy all .py files to a folder of your choice. 

Now open the command promt :

  Press Windows and R at the same time
  type cmd
  press Enter

Now navigate to the folder where you copied the files to and type "python main.py" to start the tracker.

#

Usage:

1. Launch the application by running main.py
2. Use the interface to:
   - Add new habits (daily or weekly).
   - Mark habits as completed.
   - View streaks and habit states
   - Delete habits to track
3. The Database will automatically save your data, so you can resume your progress anytime.

Important Notifications :
 1. The Tracker will generate some sample data when running the first time. Please feel free to delete them if you don´t need them.


![image](https://github.com/user-attachments/assets/e342aa6e-2367-4c2b-ab75-360a820010e4)


#


Testing:

This Tracker also comes with two testfiles written with pythons build in unittest module.

1. test_sqls.py
   This files holds the unittest for all SQL commands that interact with the database
   
2. test_streak_calculation.py
   This files holds the unittest for streak calculation

To run the the testfiles, open your command promt, navigate to the folder of the tracker and type "python -m unittest "

#

Contact:

If you have any questions, please feel free to contact me at thomas.pozzuto@iu-study.org










