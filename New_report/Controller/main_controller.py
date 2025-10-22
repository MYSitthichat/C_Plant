import os
import sys
# Import PySide6 modules
from PySide6.QtCore import Slot, QObject, QDate  # --- CHANGED: Added QDate ---
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtUiTools import QUiLoader

# --- CHANGE 1: Use relative import ---
# Import from the same 'Controller' folder
try:
    from . import database_reader
except ImportError:
    print("Error: Could not import database_reader.py from within Controller folder.")
    sys.exit(1)
# --- END CHANGE 1 ---

# This import should already work because of the fix in App.py
from View.view_main_frame import MainWindow


# --- CHANGE 2: Fix UI file path ---
# Path from this file (.../Controller/) up to .../New_report/ and then into .../UI/
# This assumes your UI file is named 'Report.ui' and is inside the 'UI' folder
UI_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "UI", "Report.ui")
# --- END CHANGE 2 ---


# Column indices from the 'concrete_order' table schema
# These help make the code more readable
COL_ID = 0
COL_DTIME = 1
COL_CUSTOMER_NAME = 2
COL_ADDRESS = 4
COL_FORMULA_NAME = 5
COL_AMOUNT = 6
COL_ROCK1_TOTAL = 9
COL_SAND_TOTAL = 10
COL_ROCK2_TOTAL = 11
COL_CEMENT_TOTAL = 12
COL_FLY_ASH_TOTAL = 13
COL_WATER_TOTAL = 14
COL_CHEM1_TOTAL = 15
COL_CHEM2_TOTAL = 16
COL_ROCK1_TARGET = 17
COL_SAND_TARGET = 18
COL_ROCK2_TARGET = 19
COL_CEMENT_TARGET = 20
COL_FLY_ASH_TARGET = 21
COL_WATER_TARGET = 22
COL_CHEM1_TARGET = 23
COL_CHEM2_TARGET = 24


class MainController(QObject):
    
    def __init__(self):
        super(MainController, self).__init__()
        
        # Load the UI file
        loader = QUiLoader()
        
        # Make sure the UI file exists
        if not os.path.exists(UI_FILE_PATH):
            print(f"Error: UI file not found at {UI_FILE_PATH}")
            print("Please check the 'UI_FILE_PATH' variable in main_controller.py")
            sys.exit(1)
            
        self.main_window = loader.load(UI_FILE_PATH, None)
        
        if not self.main_window:
            print(f"Error: Could not load UI file from {UI_FILE_PATH}")
            return
            
        # Get references to the widgets from the .ui file
        self.tree = self.main_window.report_treeWidget
        
        # --- CHANGED: Use QDateEdit widgets ---
        self.start_date_edit = self.main_window.start_dateEdit
        self.end_date_edit = self.main_window.end_dateEdit_2
        # --- END CHANGE ---
        
        self.show_button = self.main_window.show_pushButton
        self.export_button = self.main_window.export_pushButton
        self.count_line_edit = self.main_window.show_value_lineEdit

        # Setup initial UI state (populate comboboxes, connect signals)
        self.setup_ui()

    def setup_ui(self):
        """Sets default dates for QDateEdit widgets and connects button signals."""
        
        # --- CHANGED: Set default dates for QDateEdit widgets ---
        dates = database_reader.get_unique_dates()
        
        # Assuming dates are sorted newest-to-oldest and in 'yyyy-MM-dd' format
        if dates:
            oldest_date_str = dates[-1] # Get the oldest date
            newest_date_str = dates[0]  # Get the newest date
            
            # Convert string dates to QDate objects
            oldest_qdate = QDate.fromString(oldest_date_str, "yyyy-MM-dd")
            newest_qdate = QDate.fromString(newest_date_str, "yyyy-MM-dd")
            
            # Set the QDateEdit widgets
            self.start_date_edit.setDate(oldest_qdate)
            self.end_date_edit.setDate(newest_qdate)
        else:
            # If no dates found, just default to today
            today = QDate.currentDate()
            self.start_date_edit.setDate(today)
            self.end_date_edit.setDate(today)
        # --- END CHANGE ---
            
        # Connect the "Show" button to the populate_report function
        self.show_button.clicked.connect(self.populate_report)
        
        # --- Optional: Adjust column widths to look better ---
        self.tree.setColumnWidth(0, 60)   # ลำดับ (ID)
        self.tree.setColumnWidth(1, 120)  # ชื่อลูกค้า (Customer)
        self.tree.setColumnWidth(2, 250)  # รายละเอียด (Details)
        self.tree.setColumnWidth(3, 80)   # กำลังอัด (Strength)
        self.tree.setColumnWidth(4, 160)  # วันที่ เวลา (DateTime)
        self.tree.setColumnWidth(5, 80)   # จำนวน (Amount)
        self.tree.setColumnWidth(6, 150)  # ส่วนผสม (Ingredient)
        self.tree.setColumnWidth(7, 100)  # ค่าที่กำหนด (Target)
        self.tree.setColumnWidth(8, 100)  # ชั่งจริง (Actual)
        self.tree.setColumnWidth(9, 100)  # ความผิดพลาด (Error)


    @Slot()
    def populate_report(self):
        """Fetches data from DB and populates the QTreeWidget."""
        # Clear existing items from the tree
        self.tree.clear()
        
        # --- CHANGED: Get dates from QDateEdit widgets ---
        # Get the QDate object from the widget
        start_qdate = self.start_date_edit.date()
        end_qdate = self.end_date_edit.date()
        
        # Convert the QDate to the 'yyyy-MM-dd' string format for the database
        start_date = start_qdate.toString("yyyy-MM-dd")
        end_date = end_qdate.toString("yyyy-MM-dd")
        # --- END CHANGE ---
        
        # Fetch the data using your (now corrected) reader function
        orders = database_reader.read_recordings_by_date_range(start_date, end_date)
        
        # Update the total count display
        self.count_line_edit.setText(str(len(orders)))
        
        # Define the ingredients and their corresponding column indexes
        ingredients = [
            # (Display Name, Target Index, Actual Index)
            ("หิน 1",       COL_ROCK1_TARGET,   COL_ROCK1_TOTAL),
            ("หิน 2",       COL_ROCK2_TARGET,   COL_ROCK2_TOTAL),
            ("ทราย",      COL_SAND_TARGET,    COL_SAND_TOTAL),
            ("ปูนซีเมนต์",   COL_CEMENT_TARGET,  COL_CEMENT_TOTAL),
            ("เถ้าลอย",   COL_FLY_ASH_TARGET, COL_FLY_ASH_TOTAL),
            ("น้ำ",         COL_WATER_TARGET,   COL_WATER_TOTAL),
            ("น้ำยา 1",    COL_CHEM1_TARGET,   COL_CHEM1_TOTAL),
            ("น้ำยา 2",    COL_CHEM2_TARGET,   COL_CHEM2_TOTAL)
        ]

        # Loop through each order (row) from the database
        for order in orders:
            # 1. Create the Parent Item (the order itself)
            parent_item = QTreeWidgetItem(self.tree)
            
            # 2. Populate the Parent Item's columns
            parent_item.setText(0, str(order[COL_ID]))
            parent_item.setText(1, order[COL_CUSTOMER_NAME]) # This is "New Column" in your .ui
            parent_item.setText(2, order[COL_ADDRESS])
            parent_item.setText(3, order[COL_FORMULA_NAME])
            parent_item.setText(4, order[COL_DTIME])
            parent_item.setText(5, f"{order[COL_AMOUNT]:.1f}")
            
            # 3. Create Child Items (the ingredients)
            for name, target_idx, actual_idx in ingredients:
                target_val = order[target_idx]
                actual_val = order[actual_idx]
                
                # Calculate error percentage, handling division by zero
                error_percent = 0.0
                if target_val != 0:
                    error_percent = ((actual_val - target_val) / target_val) * 100
                
                # Create the child item, attached to the parent
                child_item = QTreeWidgetItem(parent_item)
                
                # Populate the Child Item's columns
                child_item.setText(6, name)
                child_item.setText(7, f"{target_val:.1f}")
                child_item.setText(8, f"{actual_val:.1f}")
                child_item.setText(9, f"{error_percent:.2f}") # Show 2 decimal places

    def Show_main(self):
        # Corrected to lowercase 'show()' for PySide6
        self.main_window.show()