from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class reg_tab(QObject):
    def __init__(self, main_window, db):
        super(reg_tab, self).__init__()
        self.main_window = main_window
        self.db = db
        self.work_queue = None
        
        self._connect_signals()
        self.reg_add_formula()
        self.load_customers_to_tree()
    
    def set_work_queue(self, work_queue):
        self.work_queue = work_queue
    
    def _connect_signals(self):
        self.main_window.reg_delete_customer_pushButton.clicked.connect(self.delete_selected_customer)
        self.main_window.reg_update_time_pushButton.clicked.connect(self.main_window.update_datetime_to_now)
        self.main_window.reg_save_pushButton.clicked.connect(self.reg_save)
        self.main_window.reg_clear_pushButton.clicked.connect(self.reg_clear)
        self.main_window.reg_list_customer_treeWidget.itemClicked.connect(self.reg_on_customer_item_clicked)
        self.main_window.reg_formula_treeWidget.itemClicked.connect(self.reg_on_formula_item_clicked)
    
    def reg_save(self):
        if not self.main_window.get_data_from_reg_from():
            QMessageBox.warning(self.main_window, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก")
            return
        else:
            date_time, name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement, comment = self.main_window.get_data_from_reg_from()

            if child_cement =="ต้องการเก็บ":
                child_cement_val = 1
            elif child_cement =="ไม่ต้องการเก็บ":
                child_cement_val = 0
            else:
                child_cement_val = 0 

            self.db.update_data_to_table_customer(name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement_val, comment)
            self.main_window.clear_reg_form()
            self.load_customers_to_tree()
            if self.work_queue:
                self.work_queue.load_work_queue()
            return True
    
    def reg_add_formula(self):
        self.main_window.reg_formula_treeWidget.clear()
        all_formula_data = self.db.read_data_in_table_formula()
        for (display_number, db_row) in enumerate(all_formula_data, start=1):
            real_id = db_row[0]
            display_list = [str(display_number)] + [str(item) for item in db_row[1:]]
            tree_item = QTreeWidgetItem(display_list)
            tree_item.setData(0, Qt.UserRole, real_id)
            self.main_window.reg_formula_treeWidget.addTopLevelItem(tree_item)

    def delete_selected_customer(self):
        tree_widget = self.main_window.reg_list_customer_treeWidget
        selected_items = tree_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกรายการที่ต้องการลบก่อน")
            return

        item_to_delete = selected_items[0]
        real_id_to_delete = item_to_delete.data(0, Qt.UserRole)
        if real_id_to_delete is None:
            return

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                     f"คุณต้องการลบลูกค้านี้ (ID: {real_id_to_delete}) ออกจากระบบถาวรหรือไม่?\n(ข้อมูลนี้จะหายไปจากคิวงานด้วย)",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_data_in_table_customer(real_id_to_delete)
                self.load_customers_to_tree()
                if self.work_queue:
                    self.work_queue.load_work_queue()
                return True
            except Exception as e:
                print(f"delete error: {e}")
                return False

    def load_customers_to_tree(self):
        self.main_window.reg_list_customer_treeWidget.clear()
        all_customer_data = self.db.read_data_in_table_customer()
        for (display_number, db_row) in enumerate(all_customer_data, start=1):
            real_id = db_row[0]
            display_list = [str(display_number)] + [str(item) for item in db_row[1:]]
            tree_item = QTreeWidgetItem(display_list)
            tree_item.setData(0, Qt.UserRole, real_id)
            self.main_window.reg_list_customer_treeWidget.addTopLevelItem(tree_item)

    def reg_clear(self):
        self.main_window.clear_reg_form()

    def reg_on_customer_item_clicked(self, item):
        self.main_window.reg_name_lineEdit.clear()
        self.main_window.reg_telephone_lineEdit.clear()
        self.main_window.reg_address_textEdit.clear()
        real_id = item.data(0, Qt.UserRole)
        if real_id is None:
            return
        try:
            customer_data = self.db.get_customer_data_by_id(real_id)
        except Exception as e:
            return
        if customer_data is None:
            return
        try:
            self.main_window.reg_name_lineEdit.setText(customer_data[0])
            self.main_window.reg_telephone_lineEdit.setText(customer_data[1])
            self.main_window.reg_address_textEdit.setText(customer_data[2])
        except Exception as e:
            print(f"Error: {e}")

    def reg_on_formula_item_clicked(self, item):
        self.main_window.reg_formula_name_lineEdit.clear()
        formula_name = item.text(1)
        self.main_window.reg_formula_name_lineEdit.setText(formula_name)