from PySide6.QtWidgets import QMainWindow
from View.main_frame import Ui_Billing


class MainWindow(QMainWindow,Ui_Billing):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)   
    
    def Show(self):
        self.show()
    
