import os
import sqlite3


class load_data:
    def __init__(self):
        is_docker = os.environ.get('IS_DOCKER', 'false').lower() == 'true'

        if is_docker:
            self.db_path = "/app/DATA_BASE/concretePlant.db"
            # print(f"[load_data Docker Mode] Using DB path: {self.db_path}")
        else:
            script_dir = os.path.dirname(__file__)
            db_path_relative = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
            self.db_path = os.path.normpath(db_path_relative)
            # print(f"[load_data Local Mode] Using DB path: {self.db_path}")

        db_dir = os.path.dirname(self.db_path)

        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir)
                # print(f"[load_data] Created directory: {db_dir}")
            except OSError as e:
                print(f"[load_data] !!! Error creating directory {db_dir}: {e}")
        elif not os.path.isdir(db_dir):
            print(f"[load_data] !!! Error: Expected directory but found a file at {db_dir}")

        if not os.path.exists(self.db_path):
            print(f"[load_data] Warning: Database file not found at {self.db_path}. It should be created.")
    
    def load_all_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, dTime, customer_name, amount FROM concrete_order ORDER BY id DESC")
            records = cursor.fetchall()
            conn.close()
            return records if records else []
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
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
            print(f"[load_data] Database error: {e}")
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
            print(f"[load_data] Database error: {e}")
            return 0, 0.0
    
    def load_bill_info(self, id):
        """Load bill information from database by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_name, address, amount 
                FROM concrete_order 
                WHERE id = ? 
                LIMIT 1
            """, (id,))
            record = cursor.fetchone()
            conn.close()
            return record
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
            return None
    
    def load_concrete_strength(self, id):
        """Load concrete strength from formula_name column"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT formula_name 
                FROM concrete_order 
                WHERE id = ? 
                LIMIT 1
            """, (id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else ""
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
            return ""
    
    def load_concrete_age(self, id):
        """Load concrete age from age column"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT age 
                FROM concrete_order 
                WHERE id = ? 
                LIMIT 1
            """, (id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else ""
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
            return ""
    
    def load_concrete_slump(self, id):
        """Load concrete slump from slump column"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT slump 
                FROM concrete_order 
                WHERE id = ? 
                LIMIT 1
            """, (id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else ""
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
            return ""
    
    def load_record_time(self, id):
        """Load record time from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dTime 
                FROM concrete_order 
                WHERE id = ? 
                LIMIT 1
            """, (id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"[load_data] Database error: {e}")
            return None