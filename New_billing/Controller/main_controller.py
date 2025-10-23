from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject
import csv
from PySide6.QtWidgets import QFileDialog,QMessageBox, QTreeWidgetItem
from threading import Thread
import time
from datetime import datetime
from Controller.load_data import load_data


class MainController(QObject):
    
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        self.main_window.reload_pushButton.clicked.connect(self.reload_data)
        self.main_window.print_pushButton.clicked.connect(self.print_data)

        # Load initial data
        self.load_data()

    def load_data(self):
        data_loader = load_data()
        data = data_loader.load_all_data()
        
        # Display data in billing_treeWidget
        if data:
            self.main_window.billing_treeWidget.clear()
            for table_name, rows in data.items():
                for row in rows:
                    item_data = [str(cell) for cell in row]
                    from PySide6.QtWidgets import QTreeWidgetItem
                    self.main_window.billing_treeWidget.addTopLevelItem(QTreeWidgetItem(item_data))
        
        return data

    def reload_data(self):
        pass


    def print_data(self):
        pass
        
# End methods
    def Show_main(self):
        self.main_window.Show()
        