import os
import sys
import csv  
from PySide6.QtCore import Slot, QObject, QDate, QDateTime 
from PySide6.QtWidgets import QTreeWidgetItem, QFileDialog  
from PySide6.QtUiTools import QUiLoader


try:
    from . import database_reader
    from . import stock_controller
except ImportError:
    import database_reader 
    import stock_controller 


# --- UI file path ---
UI_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "UI", "Report.ui")


# Column indices from the 'concrete_order' table schema
# (This section is unchanged)
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
        
        if not os.path.exists(UI_FILE_PATH):
            print(f"Error: UI file not found at {UI_FILE_PATH}")
            sys.exit(1)
            
        self.main_window = loader.load(UI_FILE_PATH, None)
        
        if not self.main_window:
            print(f"Error: Could not load UI file from {UI_FILE_PATH}")
            return
            
        # --- Get references to widgets for TAB 1 (Order History) ---
        self.tree = self.main_window.report_treeWidget
        self.start_date_edit = self.main_window.start_dateEdit
        self.end_date_edit = self.main_window.end_dateEdit_2
        self.show_button = self.main_window.show_pushButton
        self.export_button = self.main_window.export_pushButton
        self.count_line_edit = self.main_window.show_value_lineEdit

        # --- Create the StockController ---
        self.stock_controller = stock_controller.StockController(self.main_window)

        # Setup initial UI state (connect signals)
        self.setup_ui()

    def setup_ui(self):
        """Populates date comboboxes and connects button signals."""
        
        
        self.main_window.tabWidget.setCurrentIndex(0)
       
      
        today = QDate.currentDate()
        self.start_date_edit.setDate(today.addDays(-7)) # Default to 7 days ago
        self.end_date_edit.setDate(today)
            
        
        self.start_date_edit.setDisplayFormat("d/M/yyyy")
        self.end_date_edit.setDisplayFormat("d/M/yyyy")
            
       
        self.show_button.clicked.connect(self.populate_report)
        
        # "ส่งค่าออก CSV" ปุ่ม
        self.export_button.clicked.connect(self.export_to_csv)
       
        
        
        # (This section is unchanged)
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
        self.tree.clear()
        
        # This part correctly reads the date for the SQL query
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        
        orders = database_reader.read_recordings_by_date_range(start_date, end_date)
        
        self.count_line_edit.setText(str(len(orders)))
        
        ingredients = [
            ("หิน 1",       COL_ROCK1_TARGET,   COL_ROCK1_TOTAL),
            ("หิน 2",       COL_ROCK2_TARGET,   COL_ROCK2_TOTAL),
            ("ทราย",      COL_SAND_TARGET,    COL_SAND_TOTAL),
            ("ปูนซีเมนต์",   COL_CEMENT_TARGET,  COL_CEMENT_TOTAL),
            ("เถ้าลอย",   COL_FLY_ASH_TARGET, COL_FLY_ASH_TOTAL),
            ("น้ำ",         COL_WATER_TARGET,   COL_WATER_TOTAL),
            ("น้ำยา 1",    COL_CHEM1_TARGET,   COL_CHEM1_TOTAL),
            ("น้ำยา 2",    COL_CHEM2_TOTAL,   COL_CHEM2_TOTAL)
        ]

        for order in orders:
            parent_item = QTreeWidgetItem(self.tree)
            
            parent_item.setText(0, str(order[COL_ID]))
            parent_item.setText(1, order[COL_CUSTOMER_NAME])
            parent_item.setText(2, order[COL_ADDRESS])
            parent_item.setText(3, order[COL_FORMULA_NAME])
            
            # Reformat Date/Time in Table
            dt_str = order[COL_DTIME] # Get string from DB (e.g., '2025-01-09 01:34:47')
            dt_obj = QDateTime.fromString(dt_str, "yyyy-MM-dd HH:mm:ss")
            formatted_dt = dt_obj.toString("d/M/yyyy HH:mm")
            parent_item.setText(4, formatted_dt)
            
            parent_item.setText(5, f"{order[COL_AMOUNT]:.1f}")
            
            for name, target_idx, actual_idx in ingredients:
                target_val = order[target_idx]
                actual_val = order[actual_idx]
                
                error_percent = 0.0
                if target_val != 0:
                    error_percent = ((actual_val - target_val) / target_val) * 100
                
                child_item = QTreeWidgetItem(parent_item)
                
                child_item.setText(6, name)
                child_item.setText(7, f"{target_val:.1f}")
                child_item.setText(8, f"{actual_val:.1f}")
                child_item.setText(9, f"{error_percent:.2f}")

    
    @Slot()
    def export_to_csv(self):
        """
        ส่งออกข้อมูลที่แสดงใน QTreeWidget (self.tree) ไปยังไฟล์ CSV
        """
        
        # 1. เปิดหน้าต่างให้ผู้ใช้เลือกที่บันทึกไฟล์
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self.main_window, 
            "บันทึกไฟล์ CSV",  # ชื่อไตเติลของหน้าต่าง
            "",               # ไดเรกทอรีเริ่มต้น (ว่างไว้)
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )
        
        # 2. ตรวจสอบว่าผู้ใช้ได้เลือกไฟล์ (ไม่ได้กดยกเลิก)
        if not fileName:
            return  

        try:
            # 3. เปิดไฟล์เพื่อเขียน (ใช้ 'utf-8-sig' เพื่อรองรับภาษาไทยใน Excel)
            with open(fileName, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # 4. เขียนส่วนหัว (Header) ของตาราง
                header_labels = []
                for i in range(self.tree.header().count()):
                    header_labels.append(self.tree.headerItem().text(i))
                writer.writerow(header_labels)
                
                # 5. วนลูปข้อมูลทั้งหมดใน QTreeWidget
                root = self.tree.invisibleRootItem()
                for i in range(root.childCount()):
                    parent_item = root.child(i)
                    
                    
                    parent_data = []
                    for j in range(self.tree.columnCount()):
                        parent_data.append(parent_item.text(j))
                    writer.writerow(parent_data)
                    
                    
                    for k in range(parent_item.childCount()):
                        child_item = parent_item.child(k)
                        child_data = []
                        for j in range(self.tree.columnCount()):
                            child_data.append(child_item.text(j))
                        writer.writerow(child_data)
                        
            print(f"ส่งออกข้อมูลไปยัง {fileName} สำเร็จ")
            
        except IOError as e:
            print(f"เกิดข้อผิดพลาดในการเขียนไฟล์ CSV: {e}")

    def Show_main(self):
        self.main_window.show()