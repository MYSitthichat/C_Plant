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
        if name_customer == "" or phone_number == "" or address == "" or amount_concrete == "" or formula_name == "" or car_number == "" :
            return None
        else:
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
        # self.reg_list_customer_treeWidget.clear()

    def update_datetime_to_now(self):
        current_datetime = QDateTime.currentDateTime()
        self.reg_dateTimeEdit.setDateTime(current_datetime)
        
# --- FORMULA TAB METHODS --- #
    def disable_form_formula(self):
        self.for_name_formula_lineEdit.setDisabled(True)
        self.for_rock_1_lineEdit.setDisabled(True)
        self.for_sand_lineEdit.setDisabled(True)
        self.for_rock_2_lineEdit.setDisabled(True)
        self.for_cement_lineEdit.setDisabled(True)
        self.for_fyash_lineEdit.setDisabled(True)
        self.for_water_lineEdit.setDisabled(True)
        self.for_chem_1_lineEdit.setDisabled(True)
        self.for_chem_2_lineEdit.setDisabled(True)
        self.for_age_lineEdit.setDisabled(True)
        self.for_slump_lineEdit.setDisabled(True)
        self.for_name_formula_lineEdit.clear()
        self.for_rock_1_lineEdit.clear()
        self.for_sand_lineEdit.clear()
        self.for_rock_2_lineEdit.clear()
        self.for_cement_lineEdit.clear()
        self.for_fyash_lineEdit.clear()
        self.for_water_lineEdit.clear()
        self.for_chem_1_lineEdit.clear()
        self.for_chem_2_lineEdit.clear()
        self.for_age_lineEdit.clear()
        self.for_slump_lineEdit.clear()

    def enable_form_formula(self):
        self.for_name_formula_lineEdit.setEnabled(True)
        self.for_rock_1_lineEdit.setEnabled(True)
        self.for_sand_lineEdit.setEnabled(True)
        self.for_rock_2_lineEdit.setEnabled(True)
        self.for_cement_lineEdit.setEnabled(True)
        self.for_fyash_lineEdit.setEnabled(True)
        self.for_water_lineEdit.setEnabled(True)
        self.for_chem_1_lineEdit.setEnabled(True)
        self.for_chem_2_lineEdit.setEnabled(True)
        self.for_age_lineEdit.setEnabled(True)
        self.for_slump_lineEdit.setEnabled(True)
        
    def clear_form_formula(self):
        self.for_name_formula_lineEdit.clear()
        self.for_rock_1_lineEdit.clear()
        self.for_sand_lineEdit.clear()
        self.for_rock_2_lineEdit.clear()
        self.for_cement_lineEdit.clear()
        self.for_fyash_lineEdit.clear()
        self.for_water_lineEdit.clear()
        self.for_chem_1_lineEdit.clear()
        self.for_chem_2_lineEdit.clear()
        self.for_age_lineEdit.clear()
        self.for_slump_lineEdit.clear()
# --- FORMULA TAB METHODS END --- #

