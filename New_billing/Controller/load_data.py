from View.view_main_frame import MainWindow
import os
import sqlite3


database_path = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(database_path, "..", "..", "DATA_BASE", "concretePlant.db")
database_path = os.path.normpath(database_path)

class load_data:
    def __init__(self):
        self.db_path = database_path
    
    def load_all_data(self):
        try:
            # load data from the sqlite database
            conn = sqlite3.connect(self.db_path)
            # read last tens records from recording table
            cursor = conn.cursor()
            cursor.execute("SELECT Booking_ID, Record_Time, Customer_Name, Amount FROM recording_table ORDER BY Booking_ID DESC LIMIT 40")
            records = cursor.fetchall()
            conn.close()
            return records
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
