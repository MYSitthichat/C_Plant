from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class reg_tab(QObject):
    def __init__(self, main_window, db, temp_queue):
        super(reg_tab, self).__init__()
        self.main_window = main_window
        self.db = db
        self.temp_queue = temp_queue  # Add temp_queue
        self.work_queue = None
        self.selected_customer_id = None  # Track selected customer

        self._connect_signals()
        self.reg_add_formula()
        self.load_customers_to_tree()
    
    def set_work_queue(self, work_queue):
        self.work_queue = work_queue

    def _connect_signals(self):
        self.main_window.reg_save_pushButton.clicked.connect(self.reg_save)
        self.main_window.reg_clear_pushButton.clicked.connect(self.reg_clear)
        self.main_window.reg_update_time_pushButton.clicked.connect(self.main_window.update_datetime_to_now)
        self.main_window.reg_list_customer_treeWidget.itemClicked.connect(self.reg_on_customer_item_clicked)
        self.main_window.reg_delete_customer_pushButton.clicked.connect(self.reg_delete_customer)
        self.main_window.reg_formula_treeWidget.itemClicked.connect(self.reg_on_formula_item_clicked)

    def reg_add_formula(self):
        self.main_window.reg_formula_treeWidget.clear()
        try:
            formula_data = self.db.read_data_in_table_formula()
            if not formula_data:
                pass

            self.main_window.reg_formula_treeWidget.setColumnWidth(0, 50)
            self.main_window.reg_formula_treeWidget.setColumnWidth(1, 150)
            self.main_window.reg_formula_treeWidget.setColumnWidth(2, 100)
            self.main_window.reg_formula_treeWidget.setColumnWidth(3, 100)
            self.main_window.reg_formula_treeWidget.setColumnWidth(4, 100)

            for (display_number, db_row) in enumerate(formula_data, start=1):
                display_list = [
                    str(display_number),
                    str(db_row[1]),  # formula_name
                    str(db_row[2]),  # rock1
                    str(db_row[3]),  # sand
                    str(db_row[4]),  # rock2
                    str(db_row[5]),  # fly_ash
                    str(db_row[6]),  # cement
                    str(db_row[7]),  # water
                    str(db_row[8]),  # chem1
                    str(db_row[9]),  # chem2
                    str(db_row[10]), # age
                    str(db_row[11])  # slump
                ]

                tree_item = QTreeWidgetItem(display_list)
                tree_item.setData(0, Qt.UserRole, db_row[0])
                self.main_window.reg_formula_treeWidget.addTopLevelItem(tree_item)
        except Exception as e:
            print(f"Error during reg_add_formula: {e}")

    def reg_on_formula_item_clicked(self, item):
        formula_name = item.text(1)
        self.main_window.reg_formula_name_lineEdit.setText(formula_name)

    def load_customers_to_tree(self):
        self.main_window.reg_list_customer_treeWidget.clear()
        try:
            customer_data = self.db.read_data_in_table_customer()
            if not customer_data:
                pass

            self.main_window.reg_list_customer_treeWidget.setColumnWidth(0, 50)
            self.main_window.reg_list_customer_treeWidget.setColumnWidth(1, 200)
            self.main_window.reg_list_customer_treeWidget.setColumnWidth(2, 150)
            self.main_window.reg_list_customer_treeWidget.setColumnWidth(3, 300)

            for (display_number, db_row) in enumerate(customer_data, start=1):
                display_list = [
                    str(display_number),
                    str(db_row[1]),  # name
                    str(db_row[2]),  # phone_number
                    str(db_row[3])   # address
                ]

                tree_item = QTreeWidgetItem(display_list)
                tree_item.setData(0, Qt.UserRole, db_row[0])
                self.main_window.reg_list_customer_treeWidget.addTopLevelItem(tree_item)
        except Exception as e:
            print(f"Error during load_customers_to_tree: {e}")

    def reg_save(self):
        if not self.main_window.get_data_from_reg_from():
            QMessageBox.warning(self.main_window, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก")
            return
        else:
            date_time, name_customer, phone_number, address, formula_name, amount_concrete, car_number, child_cement, comment = self.main_window.get_data_from_reg_from()

            # Validate formula exists in database
            formula_exists = self.db.check_name_formula_exists(formula_name)
            if not formula_exists:
                QMessageBox.warning(
                    self.main_window, 
                    "สูตรคอนกรีตไม่ถูกต้อง", 
                    f"ไม่พบสูตรคอนกรีต '{formula_name}' ในระบบ\nกรุณาเลือกสูตรจากรายการหรือตรวจสอบชื่อสูตร"
                )
                # Focus on formula field for user to correct
                self.main_window.reg_formula_name_lineEdit.setFocus()
                self.main_window.reg_formula_name_lineEdit.selectAll()
                return  # Stop here - don't clear data, don't save

            if child_cement == "ต้องการเก็บ":
                child_cement_val = 1
            elif child_cement == "ไม่ต้องการเก็บ":
                child_cement_val = 0
            else:
                child_cement_val = 0 

            # Add to temporary queue instead of database
            order_data = {
                'customer_id': self.selected_customer_id,
                'name': name_customer,
                'phone_number': phone_number,
                'address': address,
                'formula_name': formula_name,
                'amount': amount_concrete,
                'car_number': car_number,
                'child_cement': child_cement_val,
                'comment': comment
            }
            
            new_order = self.temp_queue.add_order(order_data)
            QMessageBox.information(self.main_window, "สำเร็จ", f"เพิ่มออเดอร์ของ {name_customer} เรียบร้อยแล้ว")

            # Clear form and reload
            self.main_window.clear_reg_form()
            self.selected_customer_id = None  # Reset selection
            self.main_window.reg_name_lineEdit.setReadOnly(False)
            self.main_window.reg_telephone_lineEdit.setReadOnly(False)
            self.main_window.reg_address_textEdit.setReadOnly(False)
            
            self.main_window.tab.setCurrentWidget(self.main_window.work_tab)
            
            if self.work_queue:
                self.work_queue.load_work_queue()
            return True

    def reg_on_customer_item_clicked(self, item):
        self.main_window.reg_name_lineEdit.clear()
        self.main_window.reg_telephone_lineEdit.clear()
        self.main_window.reg_address_textEdit.clear()
        
        real_id = item.data(0, Qt.UserRole)
        self.selected_customer_id = real_id  # Store selected customer ID
        
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
            # Make customer fields read-only when existing customer is selected
            # self.main_window.reg_name_lineEdit.setReadOnly(True)
            # self.main_window.reg_telephone_lineEdit.setReadOnly(True)
            # self.main_window.reg_address_textEdit.setReadOnly(True)
        except Exception as e:
            print(f"Error: {e}")

    def reg_clear(self):
        self.main_window.clear_reg_form()
        self.selected_customer_id = None  # Reset selection
        # Enable customer fields for new customer entry
        # self.main_window.reg_name_lineEdit.setReadOnly(False)
        # self.main_window.reg_telephone_lineEdit.setReadOnly(False)
        # self.main_window.reg_address_textEdit.setReadOnly(False)

    def reg_delete_customer(self):
        selected_items = self.main_window.reg_list_customer_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกลูกค้าที่ต้องการลบ")
            return

        item_to_delete = selected_items[0]
        real_id_to_delete = item_to_delete.data(0, Qt.UserRole)
        customer_name = item_to_delete.text(1)

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                    f"คุณต้องการลบลูกค้า '{customer_name}' ใช่หรือไม่?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_data_in_table_customer(real_id_to_delete)
                self.load_customers_to_tree()
                if self.work_queue:
                    self.work_queue.load_work_queue()
                QMessageBox.information(self.main_window, "สำเร็จ", "ลบลูกค้าเรียบร้อยแล้ว")
            except Exception as e:
                QMessageBox.warning(self.main_window, "ผิดพลาด", f"ไม่สามารถลบข้อมูลได้: {e}")