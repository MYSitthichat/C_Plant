from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTreeWidgetItem
from Controller.load_data import load_data
from Controller.date_select import date_select


class MainController(QObject):
    
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        self.data_loader = load_data()
        
        # Setup date selector
        self.date_selector = date_select(self.main_window)
        
        # Connect buttons
        self.main_window.reload_pushButton.clicked.connect(self.reload_data)
        self.main_window.print_pushButton.clicked.connect(self.print_data)
        
        # Connect date changes to filter
        # self.date_selector.on_date_changed = self.filter_by_date

        # Load initial data
        self.load_data()

    def load_data(self):
        """Load all data without date filter"""
        data = self.data_loader.load_all_data()
        self.display_data(data)
        
        # Update summary
        if data:
            total_amount = sum(float(row[3]) for row in data)
            self.date_selector.update_summary(len(data), total_amount)
        
        return data
    
    def filter_by_date(self):
        """Filter data by selected dates (called by reload button)"""
        start_date, end_date = self.date_selector.get_selected_dates()
        
        # Load filtered data
        data = self.data_loader.load_data_by_date(start_date, end_date)
        self.display_data(data)
        
        # Get and update summary
        count, total = self.data_loader.get_summary(start_date, end_date)
        self.date_selector.update_summary(count, total)
    
    def display_data(self, data):
        """Display data in TreeWidget"""
        self.main_window.billing_treeWidget.clear()
        
        if data:
            for row in data:
                item_data = [str(cell) for cell in row]
                self.main_window.billing_treeWidget.addTopLevelItem(
                    QTreeWidgetItem(item_data)
                )

    def reload_data(self):
        """Reload button clicked - apply date filter"""
        self.filter_by_date()

    def print_data(self):
        """Print selected record"""
        if self.main_window.billing_treeWidget.currentItem() is None:
            QMessageBox.information(
                self.main_window, 
                "Information", 
                "Please select an item to print"
            )
        else:
            item = self.main_window.billing_treeWidget.currentItem()
            booking_id = item.text(0)
            print(f"Printing booking ID: {booking_id}")
        
    def Show_main(self):
        self.main_window.Show()