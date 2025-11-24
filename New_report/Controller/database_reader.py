import sqlite3
import os
from datetime import datetime

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "DATA_BASE")
DB_FILE = os.path.join(DATABASE_PATH, "concretePlant.db")


def read_all_recordings():
    """Read all production records from concrete_order table"""
    cmd = "SELECT * FROM concrete_order ORDER BY dTime DESC"
    return execute_read_query(cmd)

def read_recordings_by_date_range(start_date, end_date):
    """Read production records filtered by date range"""
    cmd = f"""SELECT * FROM concrete_order 
             WHERE DATE(dTime) BETWEEN '{start_date}' AND '{end_date}'
             ORDER BY ID ASC"""
    return execute_read_query(cmd)

def read_recordings_by_customer(customer_name):
    """Read production records filtered by customer name"""
    cmd = f"""SELECT * FROM concrete_order 
             WHERE customer_name LIKE '%{customer_name}%'
             ORDER BY dTime DESC"""
    return execute_read_query(cmd)

def read_concrete_formulas():
    """Read all concrete formulas from concrete_formula table"""
    cmd = "SELECT * FROM concrete_formula"
    return execute_read_query(cmd)

def read_formula_by_id(formula_id):
    """Read specific concrete formula by ID"""
    cmd = f"SELECT * FROM concrete_formula WHERE id = {formula_id}"
    result = execute_read_query(cmd)
    return result[0] if result else None

def read_bookings():
    cmd = "SELECT * FROM booking_table ORDER BY Booking_Date_Time DESC"
    return execute_read_query(cmd)

def read_event_log():
    cmd = "SELECT * FROM event_log_table ORDER BY log_time DESC"
    return execute_read_query(cmd)

def execute_read_query(query):
    db_connector = None
    try:
        if not os.path.exists(DB_FILE):
            print(f"Database Read Error: File not found at {DB_FILE}")
            return []
        db_connector = sqlite3.connect(DB_FILE)
        db_cursor = db_connector.cursor()
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if db_connector:
            db_connector.close()
            
def execute_write_query(query, params=()):
    """Execute INSERT/UPDATE/DELETE queries"""
    db_connector = None
    try:
        if not os.path.exists(DB_FILE):
            print(f"Database Write Error: File not found at {DB_FILE}")
            return False
        db_connector = sqlite3.connect(DB_FILE)
        db_cursor = db_connector.cursor()
        db_cursor.execute(query, params)
        db_connector.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database write error: {e}")
        return False
    finally:
        if db_connector:
            db_connector.close()

def get_table_columns(table_name):
    db_connector = None 
    try:
        if not os.path.exists(DB_FILE):
            return []
        db_connector = sqlite3.connect(DB_FILE)
        db_cursor = db_connector.cursor()
        db_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = db_cursor.fetchall()
        column_names = [column[1] for column in columns]
        return column_names
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if db_connector:
            db_connector.close()

def list_all_tables():
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"
    return execute_read_query(cmd)

def check_database_connection():
    if not os.path.exists(DB_FILE):
        return False
    try:
        db_connector = sqlite3.connect(DB_FILE)
        db_connector.close()
        return True
    except sqlite3.Error as e:
        return False

def get_unique_dates():
    cmd = """SELECT DISTINCT DATE(dTime) as record_date 
             FROM concrete_order 
             WHERE dTime IS NOT NULL
             ORDER BY record_date DESC"""
    results = execute_read_query(cmd)
    return [result[0] for result in results] if results else []


def get_stock_levels(start_date=None, end_date=None):
    """
    Calculates total input and output for all materials within a date range.
    If dates are None, returns empty or total (depending on usage).
    """
    
    # Date filter clause
    date_filter_stock = ""
    date_filter_order = ""
    
    if start_date and end_date:
        date_filter_stock = f"WHERE DATE(dTime) BETWEEN '{start_date}' AND '{end_date}'"
        date_filter_order = f"WHERE DATE(dTime) BETWEEN '{start_date}' AND '{end_date}'"

    query = f"""
    SELECT
        material,
        IFNULL(SUM(total_input), 0) AS TotalInput,
        IFNULL(SUM(total_output), 0) AS TotalOutput
    FROM (
        SELECT 'rock1' AS material, rock1_total_weight AS total_input, 0 AS total_output FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'rock2', rock2_total_weight, 0 FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'sand', sand_total_weight, 0 FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'cement', cement_total_weight, 0 FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'fly_ash', fly_ash_total_weight, 0 FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'chem1', chem1_total_weight, 0 FROM concrete_stock {date_filter_stock}
        UNION ALL
        SELECT 'chem2', chem2_total_weight, 0 FROM concrete_stock {date_filter_stock}
        
        UNION ALL
        
        SELECT 'rock1' AS material, 0 AS total_input, rock1_total_weight AS total_output FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'rock2', 0, rock2_total_weight FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'sand', 0, sand_total_weight FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'cement', 0, cement_total_weight FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'fly_ash', 0, fly_ash_total_weight FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'chem1', 0, chemical1_total_weight FROM concrete_order {date_filter_order}
        UNION ALL
        SELECT 'chem2', 0, chemical2_total_weight FROM concrete_order {date_filter_order}
    )
    GROUP BY material
    """
    
    results = execute_read_query(query)
    
    stock_data = {}
    if not results:
        return stock_data
        
    for row in results:
        material = row[0]
        total_input = row[1]
        total_output = row[2]
        remaining = total_input - total_output
        
        stock_data[material] = {
            'input': total_input,
            'output': total_output,
            'remaining': remaining
        }
    return stock_data

# --- FUNCTIONS FOR IMPORT TAB ---

def insert_stock_input(date_str, material_column, amount, customer="", truck="", phone="", address=""):
    """
    Inserts a new record into concrete_stock for a specific material.
    Includes Customer, Truck, Phone, and Address.
    """
    # Create a dynamic query based on the column name
    query = f"""
    INSERT INTO concrete_stock (dTime, {material_column}, customer_name, truck_number, phone_number, address)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    return execute_write_query(query, (date_str, amount, customer, truck, phone, address))

def get_stock_history(limit=50):
    """
    Gets the latest stock imports.
    Returns list of tuples: (dTime, MaterialName, Amount)
    """
    # We query raw data and process in Python to see which column has data
    query = f"SELECT * FROM concrete_stock ORDER BY dTime DESC LIMIT {limit}"
    rows = execute_read_query(query)
    
    # Get column names to map index to name
    cols = get_table_columns('concrete_stock')
    
    history = []
    if not rows or not cols:
        return history
        
    # Map DB column names to Display names
    name_map = {
        'rock1_total_weight': 'หิน 1',
        'rock2_total_weight': 'หิน 2',
        'sand_total_weight': 'ทราย',
        'fly_ash_total_weight': 'เถ้าลอย',
        'cement_total_weight': 'ปูน',
        'chem1_total_weight': 'น้ำยาเคมี 1',
        'chem2_total_weight': 'น้ำยาเคมี 2'
    }

    for row in rows:
        # Assuming row structure matches 'cols' order
        # We look for the first column that is > 0 and matches our material list
        dTime = row[cols.index('dTime')] if 'dTime' in cols else "Unknown"
        
        found_material = "Unknown"
        found_amount = 0.0
        
        for db_col, display_name in name_map.items():
            if db_col in cols:
                idx = cols.index(db_col)
                val = row[idx]
                if val and isinstance(val, (int, float)) and val > 0:
                    found_material = display_name
                    found_amount = val
                    break
        
        if found_amount > 0:
            history.append((dTime, found_material, found_amount))
            
    return history