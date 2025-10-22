import sqlite3
import os
from datetime import datetime

# Database path
# This path goes up 3 levels:
# 1. from .../Controller/ to .../New_report/
# 2. from .../New_report/ to .../C_PLANT-MAIN/
# 3. from .../C_PLANT-MAIN/ to your root (this seems wrong, let's fix)

# --- CORRECTED PATH LOGIC ---
# We need to go from .../New_report/Controller/
# up to .../C_PLANT-MAIN/ and then into /DATA_BASE/

# os.path.dirname(__file__) is .../New_report/Controller
# os.path.dirname(os.path.dirname(__file__)) is .../New_report
# os.path.dirname(os.path.dirname(os.path.dirname(__file__))) is .../C_PLANT-MAIN
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "DATA_BASE")
DB_FILE = os.path.join(DATABASE_PATH, "concretePlant.db")
# --- END CORRECTION ---


def read_all_recordings():
    """Read all production records from concrete_order table"""
    # CORRECTED: Changed table to concrete_order and column to dTime
    cmd = "SELECT * FROM concrete_order ORDER BY dTime DESC"
    return execute_read_query(cmd)

def read_recordings_by_date_range(start_date, end_date):
    """
    Read production records filtered by date range
    Args:
        start_date: Start date string in format 'YYYY-MM-DD'
        end_date: End date string in format 'YYYY-MM-DD'
    """
    # CORRECTED: Changed table to concrete_order and column to dTime
    cmd = f"""SELECT * FROM concrete_order 
             WHERE DATE(dTime) BETWEEN '{start_date}' AND '{end_date}'
             ORDER BY ID ASC"""  # <-- THIS IS THE FIX (was 'dTime DESC')
    return execute_read_query(cmd)

def read_recordings_by_customer(customer_name):
    """Read production records filtered by customer name"""
    # CORRECTED: Changed table to concrete_order and column to dTime/customer_name
    cmd = f"""SELECT * FROM concrete_order 
             WHERE customer_name LIKE '%{customer_name}%'
             ORDER BY dTime DESC"""
    return execute_read_query(cmd)

def read_concrete_formulas():
    """Read all concrete formulas from concrete_formula table"""
    # CORRECTED: Changed table to concrete_formula
    cmd = "SELECT * FROM concrete_formula"
    return execute_read_query(cmd)

def read_formula_by_id(formula_id):
    """Read specific concrete formula by ID"""
    # CORRECTED: Changed table to concrete_formula and column to id
    cmd = f"SELECT * FROM concrete_formula WHERE id = {formula_id}"
    result = execute_read_query(cmd)
    return result[0] if result else None

def read_bookings():
    """Read all bookings from booking_table"""
    # WARNING: 'booking_table' does not exist in your DB schema.
    cmd = "SELECT * FROM booking_table ORDER BY Booking_Date_Time DESC"
    return execute_read_query(cmd)

def read_event_log():
    """Read event logs from event_log_table"""
    # WARNING: 'event_log_table' does not exist in your DB schema.
    cmd = "SELECT * FROM event_log_table ORDER BY log_time DESC"
    return execute_read_query(cmd)

def execute_read_query(query):
    """
    Execute SELECT query and return results
    Args:
        query: SQL SELECT query string
    Returns:
        List of tuples containing query results, or empty list on error
    """
    db_connector = None # Initialize connector to None
    try:
        # Check if the database file exists before connecting
        if not os.path.exists(DB_FILE):
            print(f"Database Read Error: File not found at {DB_FILE}")
            print("Please check the DATABASE_PATH variable in database_reader.py")
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

def get_table_columns(table_name):
    """Get column names for a specific table"""
    db_connector = None # Initialize connector to None
    try:
        if not os.path.exists(DB_FILE):
            print(f"Database Columns Error: File not found at {DB_FILE}")
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
    """List all tables in the database"""
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"
    return execute_read_query(cmd)

def check_database_connection():
    """Check if database file exists and is accessible"""
    if not os.path.exists(DB_FILE):
        print(f"Database file not found: {DB_FILE}")
        return False
    
    try:
        db_connector = sqlite3.connect(DB_FILE)
        db_connector.close()
        return True
    except sqlite3.Error as e:
        print(f"Cannot connect to database: {e}")
        return False

def get_unique_dates():
    """Get list of unique dates from concrete_order table for date filters"""
    # CORRECTED: Changed table to concrete_order and column to dTime
    cmd = """SELECT DISTINCT DATE(dTime) as record_date 
             FROM concrete_order 
             WHERE dTime IS NOT NULL
             ORDER BY record_date DESC"""
    results = execute_read_query(cmd)
    return [result[0] for result in results] if results else []

# For testing purposes
if __name__ == "__main__":
    print("Testing database connection...")
    print(f"Attempting to connect to: {DB_FILE}")
    
    if check_database_connection():
        print("✓ Database connection successful!")
        
        print("\nAvailable tables:")
        tables = list_all_tables()
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n'concrete_order' table columns:")
        columns = get_table_columns("concrete_order")
        for col in columns:
            print(f"  - {col}")
        
        print("\nSample data from 'concrete_order' (first 3 records):")
        records = read_all_recordings()
        if records:
            for i, record in enumerate(records[:3]):
                print(f"  Record {i+1}: {record}")
        else:
            print("  - No records found or DB error.")
            
        print("\nUnique Dates:")
        dates = get_unique_dates()
        if dates:
            print(f"  - Found {len(dates)} unique dates. Newest: {dates[0]}, Oldest: {dates[-1]}")
        else:
            print("  - No dates found.")
            
    else:
        print("✗ Database connection failed!")
        print("  Please check the DATABASE_PATH and DB_FILE variables in this script.")

# --- THIS IS THE MISSING FUNCTION ---
def get_stock_levels():
    """
    Calculates the total input, total output, and remaining stock for all materials.
    Returns a dictionary where keys are material names (e..g., 'rock1', 'sand').
    
    NOTE: This query handles the column name difference:
    - concrete_stock uses 'chem1_total_weight'
    - concrete_order uses 'chemical1_total_weight'
    """
    
    query = """
    SELECT
        material,
        IFNULL(SUM(total_input), 0) AS TotalInput,
        IFNULL(SUM(total_output), 0) AS TotalOutput
    FROM (
        -- Get all inputs from concrete_stock
        SELECT 'rock1' AS material, rock1_total_weight AS total_input, 0 AS total_output FROM concrete_stock
        UNION ALL
        SELECT 'rock2', rock2_total_weight, 0 FROM concrete_stock
        UNION ALL
        SELECT 'sand', sand_total_weight, 0 FROM concrete_stock
        UNION ALL
        SELECT 'cement', cement_total_weight, 0 FROM concrete_stock
        UNION ALL
        SELECT 'fly_ash', fly_ash_total_weight, 0 FROM concrete_stock
        UNION ALL
        SELECT 'chem1', chem1_total_weight, 0 FROM concrete_stock
        UNION ALL
        SELECT 'chem2', chem2_total_weight, 0 FROM concrete_stock
        
        UNION ALL
        
        -- Get all outputs from concrete_order
        SELECT 'rock1' AS material, 0 AS total_input, rock1_total_weight AS total_output FROM concrete_order
        UNION ALL
        SELECT 'rock2', 0, rock2_total_weight FROM concrete_order
        UNION ALL
        SELECT 'sand', 0, sand_total_weight FROM concrete_order
        UNION ALL
        SELECT 'cement', 0, cement_total_weight FROM concrete_order
        UNION ALL
        SELECT 'fly_ash', 0, fly_ash_total_weight FROM concrete_order
        UNION ALL
        SELECT 'chem1', 0, chemical1_total_weight FROM concrete_order  -- <-- CORRECTED NAME
        UNION ALL
        SELECT 'chem2', 0, chemical2_total_weight FROM concrete_order  -- <-- CORRECTED NAME
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
            'remaining': remaining
        }
    return stock_data