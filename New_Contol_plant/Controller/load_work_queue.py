from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class load_work_queue(QObject):
    def __init__(self, main_window, db, reg_tab=None):
        super(load_work_queue,  self).__init__()
        self.main_window = main_window
        self.db = db
        self.reg_tab = reg_tab

        self._connect_signals()
        # self.load_work_queue()

    def _connect_signals(self):
        self.main_window.work_start_pushButton.clicked.connect(self.start_selected_work)
        self.main_window.work_cancel_pushButton.clicked.connect(self.cancel_selected_work)

    def load_work_queue(self):
        # print("--- Loading Work Queue ---") 
        self.main_window.work_queue_treeWidget.clear()
        try:
            work_data = self.db.get_work_queue() 
            # print(f"Data fetched from DB: {work_data}") 
            if not work_data:
                #  print("No work data found matching criteria (batch_state 0 or 1 and matching formula).") 
                pass

            self.main_window.work_queue_treeWidget.setColumnWidth(0, 50)
            self.main_window.work_queue_treeWidget.setColumnWidth(1, 150)
            self.main_window.work_queue_treeWidget.setColumnWidth(2, 200)
            self.main_window.work_queue_treeWidget.setColumnWidth(3, 300)

            for (display_number, db_row) in enumerate(work_data, start=1):
                # print(f"Processing row {display_lfnumber}: {db_row}")
                display_list = [
                    str(display_number),
                    str(db_row[4]), # formula_name
                    str(db_row[1]), # name
                    str(db_row[3]), # address
                    str(db_row[8]), # rock1
                    str(db_row[9]), # sand
                    str(db_row[10]), # rock2
                    str(db_row[11]), # cement
                    str(db_row[12]), # fly_ash
                    str(db_row[13]), # water
                    str(db_row[14]), # chem1
                    str(db_row[15])  # chem2
                ]

                tree_item = QTreeWidgetItem(display_list)
                tree_item.setData(0, Qt.UserRole, db_row)
                self.main_window.work_queue_treeWidget.addTopLevelItem(tree_item)
                # print(f"Added item to tree: {display_list}") 
            # print("--- Finished Loading Work Queue ---") 
        except Exception as e:
            print(f"!!! Error during load_work_queue: {e}") 

    def cancel_selected_work(self):
        # print("Cancel work")
        selected_items = self.main_window.work_queue_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกคิวงานที่ต้องการยกเลิก")
            return

        item_to_cancel = selected_items[0]
        data = item_to_cancel.data(0, Qt.UserRole)
        customer_id = data[0]
        customer_name = data[1]
        formula_name = data[4]

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                    f"คุณต้องการยกเลิกคิวงานนี้ ใช่หรือไม่?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Remove the item from the treeWidget
                index = self.main_window.work_queue_treeWidget.indexOfTopLevelItem(item_to_cancel)
                self.main_window.work_queue_treeWidget.takeTopLevelItem(index)
                
                QMessageBox.information(self.main_window, "สำเร็จ", "ยกเลิกคิวงานเรียบร้อยแล้ว")
            except Exception as e:
                QMessageBox.warning(self.main_window, "ผิดพลาด", f"เกิดข้อผิดพลาด: {e}")


    def start_selected_work(self):
        # print("Start work")
        selected_items = self.main_window.work_queue_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกคิวงานที่ต้องการเริ่ม")
            return

        item_to_start = selected_items[0]
        data = item_to_start.data(0, Qt.UserRole)

    
        customer_id = data[0]
        customer_name = data[1]  
        phone_number = data[2]
        formula_name = data[4]
        amount = data[5]
        target_rock1 = data[8]
        target_sand = data[9]
        target_rock2 = data[10]
        target_cement = data[11]
        target_flyash = data[12]
        target_water = data[13]
        target_chem1 = data[14]
        target_chem2 = data[15]

        self.clear_mixer_monitors()
        self.main_window.mix_customer_name_lineEdit.setText(customer_name)
        self.main_window.mix_customer_phone_lineEdit.setText(phone_number)
        self.main_window.mix_customer_formula_name_lineEdit.setText(formula_name)
        self.main_window.mix_number_cube_lineEdit.setText(str(amount))
        self.main_window.mix_wieght_targrt_rock_1_lineEdit.setText(str(target_rock1))
        self.main_window.mix_wieght_target_sand_lineEdit.setText(str(target_sand))
        self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(target_rock2))
        self.main_window.mix_wieght_target_cement_lineEdit.setText(str(target_cement))
        self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(target_flyash))
        self.main_window.mix_wieght_target_water_lineEdit.setText(str(target_water)) 
        self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(target_chem1))
        self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(target_chem2))
        self.db.update_customer_batch_state(customer_id, 2)
        self.load_work_queue()
        self.main_window.tab.setCurrentWidget(self.main_window.Mix_tab)


    def clear_mixer_monitors(self):
        """ล้างค่าที่แสดงผลในหน้า Mixer เพื่อเตรียมรับงานใหม่"""

        self.main_window.mix_monitor_rock_1_lineEdit.clear()
        self.main_window.mix_monitor_sand_lineEdit.clear()
        self.main_window.mix_monitor_rock_2_lineEdit.clear()
        self.main_window.mix_monitor_cement_lineEdit.clear()
        self.main_window.mix_monitor_fyash_lineEdit.clear()
        self.main_window.mix_monitor_water_lineEdit.clear()
        self.main_window.mix_monitor_chem_1_lineEdit.clear()
        self.main_window.mix_monitor_chem_2_lineEdit.clear()
        self.main_window.mix_monitor_sum_rock_and_sand_lineEdit.clear()
        self.main_window.mix_monitor_sum_fyash_and_cement_lineEdit.clear()
        self.main_window.mix_monitor_sum_chem_lineEdit.clear()  
        self.main_window.mix_wieght_Loaded_rock_1_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_sand_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_rock_2_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_cement_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_fyash_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_water_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_chem_1_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_chem_2_lineEdit.clear()
        self.main_window.mix_result_load_lineEdit.clear()
        self.main_window.mix_result_mix_lineEdit.clear()
        self.main_window.mix_result_mix_success_lineEdit.clear()
        self.main_window.mix_monitor_status_textEdit.clear()