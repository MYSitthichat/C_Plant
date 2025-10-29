from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class formula_tab(QObject):
    def __init__(self, main_window, db, reg_tab=None):
        super(formula_tab, self).__init__()
        self.main_window = main_window
        self.db = db
        self.reg_tab = reg_tab
        self.data_formula = []
        
        self._connect_signals()
        self.for_load_formula_to_tree()
        self.main_window.disable_form_formula()
    
    def _connect_signals(self):
        self.main_window.for_formula_treeWidget.itemClicked.connect(self.for_on_formula_item_clicked)
        self.main_window.for_delete_formula_pushButton.clicked.connect(self.delete_selected_formula)
        self.main_window.for_add_formula_pushButton.clicked.connect(self.for_add_new_formula)
        self.main_window.for_config_formula_pushButton.clicked.connect(self.for_config_formula)
        self.main_window.for_save_formula_pushButton.clicked.connect(self.for_save_formula)
        self.main_window.for_cancel_pushButton.clicked.connect(self.for_cancel)

    def for_add_formula_to_tree_widget(self):#formula TAB
        self.data_formula = self.db.read_data_in_table_formula()
        for row in self.data_formula :
            self.main_window.for_formula_treeWidget.addTopLevelItem(QTreeWidgetItem([str(item) for item in row]))

    def delete_selected_formula(self):#FOR tab
        tree_widget = self.main_window.for_formula_treeWidget
        selected_items = tree_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกรายการที่ต้องการลบก่อน")
            return
        item_to_delete = selected_items[0]
        real_id_to_delete = item_to_delete.data(0, Qt.UserRole)
        if real_id_to_delete is None:
            return
        try:
            self.db.delete_data_in_table_formula(real_id_to_delete)
            self.for_load_formula_to_tree()
            self.main_window.clear_form_formula()
            self.main_window.for_formula_treeWidget.clearSelection()
            if self.reg_tab:
                self.reg_tab.reg_add_formula()
        except Exception as e:
            print(f"delete error: {e}")

    def for_load_formula_to_tree(self):#FOR TAB
        self.main_window.for_formula_treeWidget.clear()
        all_formula_data = self.db.read_data_in_table_formula()
        for (display_number, db_row) in enumerate(all_formula_data, start=1):
            real_id = db_row[0]
            display_list = [str(display_number)] + [str(item) for item in db_row[1:]]
            tree_item = QTreeWidgetItem(display_list)
            tree_item.setData(0, Qt.UserRole, real_id)
            self.main_window.for_formula_treeWidget.addTopLevelItem(tree_item)
            self.main_window.for_save_formula_pushButton.setDisabled(True)

    def for_on_formula_item_clicked(self, item):#formula TAB
        result = self.db.get_data_formula_by_id(item.data(0, Qt.UserRole))
        if result is None:
            return
        try:
            self.main_window.for_name_formula_lineEdit.setText(str(result[0]))  
            self.main_window.for_rock_1_lineEdit.setText(str(result[1])) 
            self.main_window.for_sand_lineEdit.setText(str(result[2])) 
            self.main_window.for_rock_2_lineEdit.setText(str(result[3])) 
            self.main_window.for_cement_lineEdit.setText(str(result[4]))
            self.main_window.for_fyash_lineEdit.setText(str(result[5]))
            self.main_window.for_water_lineEdit.setText(str(result[6]))
            self.main_window.for_chem_1_lineEdit.setText(str(result[7]))
            self.main_window.for_chem_2_lineEdit.setText(str(result[8]))
            self.main_window.for_age_lineEdit.setText(str(result[9]))
            self.main_window.for_slump_lineEdit.setText(str(result[10]))
        except Exception as e:
            print(f"Error setting formula data to form: {e}")


    def for_add_new_formula(self):# formula tab methods
        self.main_window.clear_form_formula()
        self.main_window.enable_form_formula()
        self.main_window.for_formula_treeWidget.clearSelection()
        self.main_window.for_save_formula_pushButton.setEnabled(True)
        self.main_window.for_delete_formula_pushButton.setDisabled(True)
        self.main_window.for_config_formula_pushButton.setDisabled(True)

    def for_save_formula(self):# formula tab methods
        name_formula = self.main_window.for_name_formula_lineEdit.text()
        rock_1 = self.main_window.for_rock_1_lineEdit.text() 
        sand = self.main_window.for_sand_lineEdit.text()
        rock_2 = self.main_window.for_rock_2_lineEdit.text()
        cement = self.main_window.for_cement_lineEdit.text()
        fyash = self.main_window.for_fyash_lineEdit.text()
        water = self.main_window.for_water_lineEdit.text()
        chem_1 = self.main_window.for_chem_1_lineEdit.text()
        chem_2 = self.main_window.for_chem_2_lineEdit.text()
        age = self.main_window.for_age_lineEdit.text()
        slump = self.main_window.for_slump_lineEdit.text()
        selected_items = self.main_window.for_formula_treeWidget.selectedItems()
        if not selected_items:
            if self.db.check_name_formula_exists(name_formula):
                QMessageBox.warning(self.main_window, "ชื่อสูตรซ้ำ", "ชื่อสูตรนี้มีอยู่ในระบบแล้ว")
                return
            if name_formula == "" or rock_1 == "" or sand == "" or rock_2 == "" or cement == "" or fyash == "" or water == "" or chem_1 == "" or chem_2 == "" or age == "" or slump == "":
                QMessageBox.warning(self.main_window, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก")
                return
            self.db.insert_data_to_table_formula(name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump)
            self.main_window.clear_form_formula()
            self.main_window.disable_form_formula()
            self.for_load_formula_to_tree()
            self.main_window.for_save_formula_pushButton.setDisabled(True)
            self.main_window.for_delete_formula_pushButton.setEnabled(True)
            self.main_window.for_config_formula_pushButton.setEnabled(True)
            self.main_window.for_add_formula_pushButton.setEnabled(True)
            if self.reg_tab:
                self.reg_tab.reg_add_formula()
        else:
            item_to_update = selected_items[0]
            real_id_to_update = item_to_update.data(0, Qt.UserRole)
            if real_id_to_update is None:
                return
            if name_formula == "" or rock_1 == "" or sand == "" or rock_2 == "" or cement == "" or fyash == "" or water == "" or chem_1 == "" or chem_2 == "" or age == "" or slump == "":
                QMessageBox.warning(self.main_window, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก")
                return
            self.db.update_data_to_table_formula(real_id_to_update, name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump)
            self.main_window.clear_form_formula()
            self.main_window.disable_form_formula()
            self.for_load_formula_to_tree()
            self.main_window.for_save_formula_pushButton.setDisabled(True)
            self.main_window.for_delete_formula_pushButton.setEnabled(True)
            self.main_window.for_config_formula_pushButton.setEnabled(True)
            self.main_window.for_add_formula_pushButton.setEnabled(True)
            if self.reg_tab:
                self.reg_tab.reg_add_formula()

    def for_cancel(self):# formula tab methods
        self.main_window.for_formula_treeWidget.clearSelection()
        self.main_window.disable_form_formula()
        self.main_window.for_save_formula_pushButton.setDisabled(True)
        self.main_window.for_delete_formula_pushButton.setEnabled(True)
        self.main_window.for_add_formula_pushButton.setEnabled(True)
        self.main_window.for_config_formula_pushButton.setEnabled(True)

    def for_config_formula(self):# formula tab methods
        selected_items = self.main_window.for_formula_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกรายการสูตรที่ต้องการแก้ไขก่อน")
            return
        self.main_window.enable_form_formula()
        self.main_window.for_save_formula_pushButton.setEnabled(True)
        self.main_window.for_delete_formula_pushButton.setDisabled(True)
        self.main_window.for_add_formula_pushButton.setDisabled(True)