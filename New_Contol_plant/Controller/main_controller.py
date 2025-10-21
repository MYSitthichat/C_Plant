from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject 
from PySide6.QtWidgets import QFileDialog,QMessageBox
from threading import Thread
import time
from datetime import datetime


class MainController(QObject):
    
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        

# End methods
    def Show_main(self):
        self.main_window.Show()
