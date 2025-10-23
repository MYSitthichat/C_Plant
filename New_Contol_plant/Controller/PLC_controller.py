import sys
from PySide6.QtWidgets import QApplication
import time
from PySide6.QtCore import Slot , QObject, Qt

class PLC_Controller(QObject):
    def __init__(self):
        super().__init__()
        
    @Slot(str)
    
    def debug_rock_1_action(self, action):
        if action == "start":
            print("Debug: Starting Rock 1")
        elif action == "stop":
            print("Debug: Stopping Rock 1")
