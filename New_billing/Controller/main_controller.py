from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTreeWidgetItem
from Controller.load_data import load_data
from Controller.date_select import date_select
from Controller.create_bill import BillGenerator


class MainController(QObject):
    
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        self.data_loader = load_data()
        self.bill_generator = BillGenerator()

        # Setup date selector
        self.date_selector = date_select(self.main_window)
        
        self.main_window.print_pushButton.clicked.connect(self.print_data)

        self.date_selector.on_date_changed = self.filter_by_date

        # Load initial data
        self.load_data()

    def load_data(self):
        """Load all data without date filter"""
        data = self.data_loader.load_all_data()
        self.display_data(data)
        
        # Update value display in line UI
        if data:
            total_amount = sum(float(row[3]) for row in data)
            self.date_selector.show_value(len(data), total_amount)
        
        return data
    
    def filter_by_date(self):
        """Filter data by selected dates (called by reload button)"""
        start_date, end_date = self.date_selector.get_selected_dates()
        
        # Load filtered data
        data = self.data_loader.load_data_by_date(start_date, end_date)
        self.display_data(data)
        
        # Get and update value in line UI
        count, total = self.data_loader.get_summary(start_date, end_date)
        self.date_selector.show_value(count, total)
    
    def display_data(self, data):
        """Display data in TreeWidget"""
        self.main_window.billing_treeWidget.clear()
        
        if data:
            for row in data:
                item_data = [str(cell) for cell in row]
                self.main_window.billing_treeWidget.addTopLevelItem(
                    QTreeWidgetItem(item_data)
                )

    def print_data(self):
        """Generate and print bill for selected item"""
        # Get selected item from TreeWidget
        selected_items = self.main_window.billing_treeWidget.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(
                self.main_window,
                "No Selection",
                "Please select a bill to print."
            )
            return
        
        # Get the ID from the first column of selected item
        selected_item = selected_items[0]
        bill_id = selected_item.text(0)  # Assuming ID is in first column
        
        try:
            # Generate and print the bill
            success = self.bill_generator.generate_and_print_bill(bill_id)
            
            if success:
                QMessageBox.information(
                    self.main_window,
                    "Success",
                    f"Bill for ID {bill_id} has been generated and sent to printer."
                )
            else:
                QMessageBox.warning(
                    self.main_window,
                    "Print Failed",
                    f"Failed to print bill for ID {bill_id}. Check console for details."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Error printing bill: {str(e)}"
            )
            print(f"Error in print_data: {e}")
            import traceback
            traceback.print_exc()
        
    def Show_main(self):
        self.main_window.Show()