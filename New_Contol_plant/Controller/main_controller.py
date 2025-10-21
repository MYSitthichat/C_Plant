from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject, Qt
from PySide6.QtWidgets import QFileDialog,QMessageBox,QTreeWidgetItem
from threading import Thread
import time
from datetime import datetime
from Controller.database_control import C_palne_Database


class MainController(QObject):   
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        
        self.db = C_palne_Database()
        self.data_formula = []
        self.reg_add_formula()
        self.load_customers_to_tree()
        self.for_add_formula()
        self.main_window.reg_delete_customer_pushButton.clicked.connect(self.delete_selected_customer)
        self.main_window.reg_update_time_pushButton.clicked.connect(self.main_window.update_datetime_to_now)
        self.main_window.reg_save_pushButton.clicked.connect(self.reg_save)
        self.main_window.reg_clear_pushButton.clicked.connect(self.reg_clear)
        self.main_window.reg_save_new_customer_pushButton.clicked.connect(self.reg_save_new_customer)
        self.main_window.mix_start_load_pushButton.clicked.connect(self.mix_start_load)
        self.main_window.mix_cancel_load_pushButton.clicked.connect(self.mix_cancel_load)
        self.main_window.for_add_formula_pushButton.clicked.connect(self.for_add_formula)
        self.main_window.for_config_formula_pushButton.clicked.connect(self.for_config_formula)
        self.main_window.for_delete_formula_pushButton.clicked.connect(self.for_delete_formula)
        self.main_window.for_save_formula_pushButton.clicked.connect(self.for_save_formula)
        self.main_window.for_cancel_pushButton.clicked.connect(self.for_cancel)
        self.main_window.debug_open_rock_1_pushButton.clicked.connect(self.debug_open_rock_1)
        self.main_window.debug_close_rock_1_pushButton.clicked.connect(self.debug_close_rock_1)
        self.main_window.debug_open_rock_2_pushButton.clicked.connect(self.debug_open_rock_2)
        self.main_window.debug_close_rock_2_pushButton.clicked.connect(self.debug_close_rock_2)
        self.main_window.debug_open_sand_pushButton.clicked.connect(self.debug_open_sand)
        self.main_window.debug_close_sand_pushButton.clicked.connect(self.debug_close_sand)
        self.main_window.debug_open_converyer_under_pushButton.clicked.connect(self.debug_open_converyer_under)
        self.main_window.debug_close_converyer_under_pushButton.clicked.connect(self.debug_close_converyer_under)
        self.main_window.debug_open_converyer_top_pushButton.clicked.connect(self.debug_open_converyer_top)
        self.main_window.debug_close_converyer_top_pushButton.clicked.connect(self.debug_close_converyer_top)
        self.main_window.debug_open_cement_pushButton.clicked.connect(self.debug_open_cement)
        self.main_window.debug_close_cement_pushButton.clicked.connect(self.debug_close_cement)
        self.main_window.debug_open_fyash_pushButton.clicked.connect(self.debug_open_fyash)
        self.main_window.debug_close_fyash_pushButton.clicked.connect(self.debug_close_fyash)
        self.main_window.debug_open_vale_cement_pushButton.clicked.connect(self.debug_open_vale_cement)
        self.main_window.debug_close_vale_cement_pushButton.clicked.connect(self.debug_close_vale_cement)
        self.main_window.debug_open_mixer_pushButton.clicked.connect(self.debug_open_mixer)
        self.main_window.debug_close_mixer_pushButton.clicked.connect(self.debug_close_mixer)
        self.main_window.debug_open_vale_mixer_pushButton.clicked.connect(self.debug_open_vale_mixer)
        self.main_window.debug_close_vale_mixer_pushButton.clicked.connect(self.debug_close_vale_mixer)
        self.main_window.debug_open_water_pushButton.clicked.connect(self.debug_open_water)
        self.main_window.debug_close_water_pushButton.clicked.connect(self.debug_close_water)
        self.main_window.debug_open_vale_water_pushButton.clicked.connect(self.debug_open_vale_water)
        self.main_window.debug_close_vale_water_pushButton.clicked.connect(self.debug_close_vale_water)
        self.main_window.debug_open_chem_1_pushButton.clicked.connect(self.debug_open_chem_1)
        self.main_window.debug_close_chem_1_pushButton.clicked.connect(self.debug_close_chem_1)
        self.main_window.debug_open_chem_2_pushButton.clicked.connect(self.debug_open_chem_2)
        self.main_window.debug_close_chem_2_pushButton.clicked.connect(self.debug_close_chem_2)
        self.main_window.debug_open_vale_chem_pushButton.clicked.connect(self.debug_open_vale_chem)
        self.main_window.debug_close_vale_chem_pushButton.clicked.connect(self.debug_close_vale_chem)
        self.main_window.offset_save_pushButton.clicked.connect(self.offset_save)
        self.main_window.offset_edite_pushButton.clicked.connect(self.offset_edite)
        self.main_window.offset_cancel_pushButton.clicked.connect(self.offset_cancel)



    def reg_save(self):
        if not self.main_window.get_data_from_reg_from():
            QMessageBox.warning(self.main_window, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก")
            return
        else:
            date_time, name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement, comment = self.main_window.get_data_from_reg_from()
            if child_cement =="ต้องการเก็บ":
                child_cement = 1
            elif child_cement =="ไม่ต้องการเก็บ":
                child_cement = 0
            else:
                pass
            print(date_time, name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement, comment)
            self.db.update_data_to_table_customer(name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement, comment)
            self.main_window.clear_reg_form()
            self.load_customers_to_tree()







    def reg_save_new_customer(self):
        print("reg save new customer")

    def mix_start_load(self):
        print("mix start load")

    def mix_cancel_load(self):
        print("mix cancel load")

    def for_add_formula(self):
        print("for add formula")

    def for_config_formula(self):
        print("for config formula")

    def for_delete_formula(self):
        print("for delete formula")

    def for_save_formula(self):
        print("for save formula")

    def for_cancel(self):
        print("for cancel formula")

    def debug_open_rock_1(self):
        print("debug open rock 1")

    def debug_close_rock_1(self):
        print("debug close rock 1")

    def debug_open_rock_2(self):
        print("debug open rock 2")

    def debug_close_rock_2(self):
        print("debug close rock 2")

    def debug_open_sand(self):
        print("debug open sand")

    def debug_close_sand(self):
        print("debug close sand")

    def debug_open_converyer_under(self):
        print("debug open converyer under")

    def debug_close_converyer_under(self):
        print("debug close converyer under")

    def debug_open_converyer_top(self):
        print("debug open converyer top")

    def debug_close_converyer_top(self):
        print("debug close converyer top")

    def debug_open_cement(self):
        print("debug open cement")

    def debug_close_cement(self):
        print("debug close cement")

    def debug_open_fyash(self):
        print("debug open fyash")

    def debug_close_fyash(self):
        print("debug close fyash")

    def debug_open_vale_cement(self):
        print("debug open vale cement")

    def debug_close_vale_cement(self):
        print("debug close vale cement")

    def debug_open_mixer(self):
        print("debug open mixer")

    def debug_close_mixer(self):
        print("debug close mixer")

    def debug_open_vale_mixer(self):
        print("debug open vale mixer")

    def debug_close_vale_mixer(self):
        print("debug close vale mixer")

    def debug_open_water(self):
        print("debug open water")

    def debug_close_water(self):
        print("debug close water")

    def debug_open_vale_water(self):
        print("debug open vale water")

    def debug_close_vale_water(self):
        print("debug close vale water")

    def debug_open_chem_1(self):
        print("debug open chem 1")

    def debug_close_chem_1(self):
        print("debug close chem 1")

    def debug_open_chem_2(self):
        print("debug open chem 2")

    def debug_close_chem_2(self):
        print("debug close chem 2")

    def debug_open_vale_chem(self):
        print("debug open vale chem")

    def debug_close_vale_chem(self):
        print("debug close vale chem")

    def offset_save(self):
        print("offset save")

    def offset_edite(self):
        print("offset edite")

    def offset_cancel(self):
        print("offset cancel")

        
# End methods
    def Show_main(self):
        self.main_window.Show()

    def for_add_formula(self):#REG TAB
        self.data_formula = self.db.read_data_in_table_formula()
        for row in self.data_formula :
            self.main_window.for_formula_treeWidget.addTopLevelItem(QTreeWidgetItem([str(item) for item in row]))

    def reg_add_formula(self):#REG TAB
        self.data_formula = self.db.read_data_in_table_formula()
        for row in self.data_formula :
            self.main_window.reg_formula_treeWidget.addTopLevelItem(QTreeWidgetItem([str(item) for item in row]))
            
    def reg_delete_customer(self):#REG TAB
        tree_widget = self.main_window.reg_list_customer_treeWidget
        selected_items = tree_widget.selectedItems()
        id = selected_items[0].text(0)
        self.db.delete_data_in_table_customer(id)
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกรายการที่ต้องการลบก่อน")
            return
        else:
            for item in selected_items:
                index = tree_widget.indexOfTopLevelItem(item)
                tree_widget.takeTopLevelItem(index)
            
    def delete_selected_customer(self):#REG tab
        tree_widget = self.main_window.reg_list_customer_treeWidget 
        selected_items = tree_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกรายการที่ต้องการลบก่อน")
            return
        item_to_delete = selected_items[0]
        real_id_to_delete = item_to_delete.data(0, Qt.UserRole)
        if real_id_to_delete is None:
            return
        print(f"data in tree {item_to_delete.text(0)}, (ID จริง: {real_id_to_delete})")
        try:
            self.db.delete_data_in_table_customer(real_id_to_delete)
            self.load_customers_to_tree()
        except Exception as e:
            print(f"delete error: {e}")
            
    def load_customers_to_tree(self):#REG TAB
        self.main_window.reg_list_customer_treeWidget.clear() 
        all_customer_data = self.db.read_data_in_table_customer()
        for (display_number, db_row) in enumerate(all_customer_data, start=1):
            real_id = db_row[0] 
            display_list = [str(display_number)] + [str(item) for item in db_row[1:]]
            tree_item = QTreeWidgetItem(display_list)
            tree_item.setData(0, Qt.UserRole, real_id) 
            self.main_window.reg_list_customer_treeWidget.addTopLevelItem(tree_item)

    def reg_clear(self):#REG TAB
        self.main_window.clear_reg_form()
        
        