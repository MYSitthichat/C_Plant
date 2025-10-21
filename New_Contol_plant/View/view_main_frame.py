from PySide6.QtWidgets import QMainWindow 
from View.main_frame import Ui_Control_Plant
from PySide6.QtCore import QDateTime

class MainWindow(QMainWindow,Ui_Control_Plant):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
    
    def Show(self):
        self.update_datetime_to_now()
        self.show()

    def get_data_from_reg_from(self):
        name_customer = self.reg_name_lineEdit.text()
        phone_number = self.reg_telephone_lineEdit.text()
        address = self.reg_address_textEdit.toPlainText()
        date_time = self.reg_dateTimeEdit.dateTime()
        car_number = self.reg_number_car_lineEdit.text()
        comment = self.reg_comment_textEdit.toPlainText()
        child_cement = self.reg_child_cement_comboBox.currentText()
        amount_concrete = self.reg_amount_unit_lineEdit.text()
        formula_name = self.reg_formula_name_lineEdit.text()
        return date_time, name_customer, phone_number, address, formula_name,amount_concrete,car_number,child_cement,comment

    def clear_reg_form(self):
        self.reg_name_lineEdit.clear()
        self.reg_telephone_lineEdit.clear()
        self.reg_address_textEdit.clear()
        self.update_datetime_to_now()
        self.reg_number_car_lineEdit.clear()
        self.reg_comment_textEdit.clear()
        self.reg_child_cement_comboBox.setCurrentIndex(0)
        self.reg_amount_unit_lineEdit.clear()
        self.reg_formula_name_lineEdit.clear()
        self.reg_list_customer_treeWidget.clear()

    def update_datetime_to_now(self):
        current_datetime = QDateTime.currentDateTime()
        self.reg_dateTimeEdit.setDateTime(current_datetime)

