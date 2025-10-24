from PySide6.QtCore import QObject, QDate
from Controller.load_data import load_data


class date_select(QObject):
    
    def __init__(self, main_window):
        super(date_select, self).__init__()
        self.main_window = main_window
        self.data_loader = load_data()
        
        # Populate date comboboxes from database
        self.date_to_ComboBox()
        
        
    def date_to_ComboBox(self):
        """add dates to comboboxes from database"""
        dates = self.get_dates_from_database()
        
        if dates:
            # Add to comboboxes
            self.main_window.start_date_comboBox.addItems(dates)
            self.main_window.end_date_comboBox.addItems(dates)
            
            # Set default: end = most recent, start = oldest
            self.main_window.end_date_comboBox.setCurrentIndex(0)  # Most recent
            self.main_window.start_date_comboBox.setCurrentIndex(len(dates) - 1)  # Oldest
        else:
            # Fallback: use current date if no data
            today = QDate.currentDate().toString("dd-MM-yyyy")
            self.main_window.start_date_comboBox.addItem(today)
            self.main_window.end_date_comboBox.addItem(today)
    
    def get_dates_from_database(self):
        """Get unique dates from database records"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_loader.db_path)
            cursor = conn.cursor()
            
            # Get distinct dates from concrete_order table
            cursor.execute("""
                SELECT DISTINCT DATE(dTime) as order_date
                FROM concrete_order
                ORDER BY order_date DESC
            """)
            
            results = cursor.fetchall()
            conn.close()
            
            # Convert to dd-MM-yyyy format
            dates = []
            for row in results:
                date_str = row[0]  # Format: yyyy-MM-dd
                qdate = QDate.fromString(date_str, "yyyy-MM-dd")
                dates.append(qdate.toString("dd-MM-yyyy"))
            
            return dates
            
        except Exception as e:
            print(f"Error getting dates from database: {e}")
            return []
    
    def get_selected_dates(self):
        """Get start and end dates in database (yyyy-MM-dd)"""
        start_str = self.main_window.start_date_comboBox.currentText()
        end_str = self.main_window.end_date_comboBox.currentText()
        
        # Convert from "dd-MM-yyyy" to "yyyy-MM-dd"
        start_date = QDate.fromString(start_str, "dd-MM-yyyy")
        end_date = QDate.fromString(end_str, "dd-MM-yyyy")
        
        return start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd")
    
    def show_value(self, total_records, total_amount):
        """Show summary values in the UI"""
        summary_text = f"{total_records}"
        self.main_window.show_value_lineEdit.setText(summary_text)
    
    def refresh_dates(self):
        """Refresh date comboboxes when data changes"""
        # Clear existing items
        self.main_window.start_date_comboBox.clear()
        self.main_window.end_date_comboBox.clear()
        
        # Repopulate
        self.date_to_ComboBox()