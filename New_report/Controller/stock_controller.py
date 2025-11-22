import os
import sys
from PySide6.QtCore import Slot, QObject, QDate, QDateTime, QTime
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

# Import your database reader
try:
    from . import database_reader
except ImportError:
    import database_reader 


class StockController(QObject):
    
    def __init__(self, main_window):
        super(StockController, self).__init__()
        self.stock_window = main_window 
        
        # --- TAB: Stock Status (สถานะสต็อก) ---
        self.table_stock = self.stock_window.tableWidget_stock
        self.btn_refresh = self.stock_window.btn_refresh_stock
        
        # --- TAB: Import Stock (นำเข้าสินค้า) ---
        self.date_edit = self.stock_window.dateEdit_import
        self.time_edit = self.stock_window.timeEdit_import # NEW: Time input
        self.combo_material = self.stock_window.comboBox_material
        self.spin_amount = self.stock_window.doubleSpinBox_amount
        
        # NEW: Extra fields (Customer Name, Truck, Phone, Address)
        self.line_customer = self.stock_window.lineEdit_customer_name
        self.line_truck = self.stock_window.lineEdit_truck
        self.line_phone = self.stock_window.lineEdit_phone
        self.line_address = self.stock_window.lineEdit_address
        
        self.btn_save_import = self.stock_window.pushButton
        self.table_history = self.stock_window.tableWidget_history
        
        # Initialize UI Defaults
        self.date_edit.setDate(QDate.currentDate())
        self.time_edit.setTime(QTime.currentTime()) # Set default time to now
        
        # --- Connect Signals ---
        self.setup_signals()
        
        # Load history initially
        self.load_import_history()

    def setup_signals(self):
        # Tab Stock
        if self.btn_refresh:
            self.btn_refresh.clicked.connect(self.update_stock_display)
            
        # Tab Import
        if self.btn_save_import:
            self.btn_save_import.clicked.connect(self.save_import_data)

    # ==========================================
    #  LOGIC FOR STOCK STATUS TAB
    # ==========================================
    @Slot()
    def update_stock_display(self):
        """Calculates stock and updates the TableWidget."""
        stock_data = database_reader.get_stock_levels()
        
        if not stock_data:
            print("No stock data found.")
            return

        # Mapping: Row Index -> Material Key in 'stock_data'
        row_map = {
            0: 'rock1',
            1: 'rock2',
            2: 'sand',
            3: 'fly_ash',
            4: 'cement',
            5: 'chem1',
            6: 'chem2'
        }

        for row_idx, material_key in row_map.items():
            if material_key in stock_data:
                remain_val = stock_data[material_key]['remaining']
                item = QTableWidgetItem(f"{remain_val:,.2f}") 
                self.table_stock.setItem(row_idx, 1, item)
            else:
                self.table_stock.setItem(row_idx, 1, QTableWidgetItem("0.00"))

    # ==========================================
    #  LOGIC FOR IMPORT TAB
    # ==========================================
    @Slot()
    def save_import_data(self):
        """Reads input, saves to DB, and updates history."""
        
        # 1. Get Data
        date_part = self.date_edit.date().toString("yyyy-MM-dd") 
        time_part = self.time_edit.time().toString("HH:mm:ss")
        full_datetime = f"{date_part} {time_part}" # Combine Date + Time
        
        amount = self.spin_amount.value()
        material_idx = self.combo_material.currentIndex()
        
        # Get extra fields
        customer = self.line_customer.text()
        truck = self.line_truck.text()
        phone = self.line_phone.text()
        address = self.line_address.text()
        
        if amount <= 0:
            QMessageBox.warning(self.stock_window, "Warning", "กรุณาระบุจำนวนมากกว่า 0")
            return

        # 2. Map Combo Index to DB Column Name
        col_map = {
            0: 'rock1_total_weight',
            1: 'rock2_total_weight',
            2: 'sand_total_weight',
            3: 'fly_ash_total_weight',
            4: 'cement_total_weight',
            5: 'chem1_total_weight',
            6: 'chem2_total_weight'
        }
        
        col_name = col_map.get(material_idx)
        if not col_name:
            return

        # 3. Save to DB (Passing new fields)
        success = database_reader.insert_stock_input(
            full_datetime, col_name, amount, 
            customer, truck, phone, address
        )
        
        if success:
            QMessageBox.information(self.stock_window, "Success", "บันทึกข้อมูลเรียบร้อย")
            self.spin_amount.setValue(0.00) 
            self.line_customer.clear()
            self.line_truck.clear()
            self.line_phone.clear()
            self.line_address.clear()
            self.load_import_history()   # Refresh table
        else:
            QMessageBox.critical(self.stock_window, "Error", "เกิดข้อผิดพลาดในการบันทึกข้อมูล")

    def load_import_history(self):
        """Loads latest imports, sorts them by date DESC (Newest First), and displays."""
        history = database_reader.get_stock_history()
        
        # 1. Parse dates so we can sort them correctly in Python
        sorted_history = []
        for row in history:
            dTime, material, amount = row
            dTime_str = str(dTime)
            
            # Try to parse different formats that might be in your DB
            dt_obj = QDateTime()
            if "-" in dTime_str:
                # Try ISO format (yyyy-MM-dd)
                if ":" in dTime_str:
                     dt_obj = QDateTime.fromString(dTime_str, "yyyy-MM-dd HH:mm:ss")
                else:
                     dt_obj = QDateTime.fromString(dTime_str, "yyyy-MM-dd")
            elif "/" in dTime_str:
                # Try Thai format (dd/MM/yyyy)
                dt_obj = QDateTime.fromString(dTime_str, "dd/MM/yyyy")
            
            # Fallback if invalid
            if not dt_obj.isValid():
                # Treat invalid dates as very old so they go to the bottom
                dt_obj = QDateTime.fromString("1900-01-01", "yyyy-MM-dd")

            sorted_history.append({
                "dt": dt_obj,
                "display": dTime_str,
                "material": material,
                "amount": amount
            })

        # 2. Sort by Date Object (Reverse = Newest First)
        sorted_history.sort(key=lambda x: x["dt"], reverse=True)

        # 3. Display in Table
        self.table_history.setRowCount(0) # Clear table
        
        for item in sorted_history:
            row_idx = self.table_history.rowCount()
            self.table_history.insertRow(row_idx)
            
            # Format date consistently for display (dd/MM/yyyy HH:mm) if valid
            display_str = item["display"]
            if item["dt"].isValid() and item["dt"].date().year() > 1900:
                display_str = item["dt"].toString("dd/MM/yyyy HH:mm")

            self.table_history.setItem(row_idx, 0, QTableWidgetItem(display_str))
            self.table_history.setItem(row_idx, 1, QTableWidgetItem(item["material"]))
            self.table_history.setItem(row_idx, 2, QTableWidgetItem(f"{item['amount']:,.2f}"))