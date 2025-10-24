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
            cursor.execute("SELECT id, dTime, customer_name, amount FROM concrete_order ORDER BY id DESC")
            records = cursor.fetchall()
            conn.close()
            return records if records else []
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def load_data_by_date(self, start_date, end_date):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, dTime, customer_name, amount 
                FROM concrete_order 
                WHERE DATE(dTime) BETWEEN ? AND ?
                ORDER BY id DESC
            """, (start_date, end_date))
            records = cursor.fetchall()
            conn.close()
            return records if records else []
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_summary(self, start_date, end_date):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*), SUM(amount)
                FROM concrete_order 
                WHERE DATE(dTime) BETWEEN ? AND ?
            """, (start_date, end_date))
            result = cursor.fetchone()
            conn.close()
            
            count = result[0] if result[0] else 0
            total = result[1] if result[1] else 0.0
            return count, total
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0, 0.0