import sqlite3
import os


class C_palne_Database():
    def __init__(self, db_path):
        self.db_path = db_path
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
        db_path = os.path.normpath(db_path) 

    def read_data_all_data_in_table_formula(self):
        query = "SELECT * FROM concrete_formula;" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"Read {len(results)} rows from concrete_formula table.")
            return results
        except sqlite3.Error as e:
            print(f"error {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def read_data_all_in_table_oder(self):
        query = "SELECT * FROM concrete_order;" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"Read {len(results)} rows from concrete_order table.")
            return results
        except sqlite3.Error as e:
            print(f"error {e}")
            return []
        finally:
            if conn:
                conn.close()
        


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
    db_path = os.path.normpath(db_path) 
    db = C_palne_Database(db_path)
    # results = db.read_data_all_data_in_table_formula()
    results = db.read_data_all_in_table_oder()
    for row in results:
        print(row)