from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject, Qt
from PySide6.QtWidgets import QFileDialog,QMessageBox,QTreeWidgetItem
from threading import Thread
import time
from datetime import datetime
from Controller.database_control import C_palne_Database
from Controller.PLC_controller import PLC_Controller

class MainController(QObject):
    action = Slot(str)
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()

        self.db = C_palne_Database()
        self.plc_controller = PLC_Controller()
        self.data_formula = []

        # reg tab
        self.reg_add_formula()
        self.load_customers_to_tree()
        self.main_window.reg_delete_customer_pushButton.clicked.connect(self.delete_selected_customer)
        self.main_window.reg_update_time_pushButton.clicked.connect(self.main_window.update_datetime_to_now)
        self.main_window.reg_save_pushButton.clicked.connect(self.reg_save)
        self.main_window.reg_clear_pushButton.clicked.connect(self.reg_clear)
        self.main_window.reg_list_customer_treeWidget.itemClicked.connect(self.reg_on_customer_item_clicked)
        self.main_window.reg_formula_treeWidget.itemClicked.connect(self.reg_on_formula_item_clicked)
        # end reg tab

      
        self.load_work_queue() 
        self.main_window.work_start_pushButton.clicked.connect(self.start_selected_work)
        self.main_window.work_cancel_pushButton.clicked.connect(self.cancel_selected_work)
       
        # formula tab
        self.for_load_formula_to_tree()
        self.main_window.disable_form_formula()
        self.main_window.for_formula_treeWidget.itemClicked.connect(self.for_on_formula_item_clicked)
        self.main_window.for_delete_formula_pushButton.clicked.connect(self.delete_selected_formula)
        self.main_window.for_add_formula_pushButton.clicked.connect(self.for_add_new_formula)
        self.main_window.for_config_formula_pushButton.clicked.connect(self.for_config_formula)
        self.main_window.for_save_formula_pushButton.clicked.connect(self.for_save_formula)
        self.main_window.for_cancel_pushButton.clicked.connect(self.for_cancel)
        # end formula tab

        self.main_window.mix_start_load_pushButton.clicked.connect(self.mix_start_load)
        self.main_window.mix_cancel_load_pushButton.clicked.connect(self.mix_cancel_load)

        # self.main_window.debug_open_rock_1_pushButton.clicked.connect(self.plc_controller.emit.action("start"))
        # self.main_window.debug_close_rock_1_pushButton.clicked.connect(self.plc_controller.debug_rock_1_action(action = "stop"))
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
        self.load_offset_settings()
        self.set_offset_form_read_only(True)
        self.main_window.offset_save_pushButton.setEnabled(False)
        self.main_window.offset_edite_pushButton.setEnabled(True)
        self.main_window.offset_cancel_pushButton.setEnabled(False)


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
            self.load_work_queue()
           

    def mix_start_load(self):
        print("mix start load")

    def mix_cancel_load(self):
        print("mix cancel load")

    def load_work_queue(self):
        print("--- Loading Work Queue ---") 
        self.main_window.work_queue_treeWidget.clear()
        try:
            work_data = self.db.get_work_queue() 
            print(f"Data fetched from DB: {work_data}") 
            if not work_data:
                 print("No work data found matching criteria (batch_state 0 or 1 and matching formula).") 

            self.main_window.work_queue_treeWidget.setColumnWidth(0, 50)
            self.main_window.work_queue_treeWidget.setColumnWidth(1, 150)
            self.main_window.work_queue_treeWidget.setColumnWidth(2, 200)
            self.main_window.work_queue_treeWidget.setColumnWidth(3, 300)

            for (display_number, db_row) in enumerate(work_data, start=1):
                print(f"Processing row {display_number}: {db_row}")
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
                print(f"Added item to tree: {display_list}") 
            print("--- Finished Loading Work Queue ---") 
        except Exception as e:
            print(f"!!! Error during load_work_queue: {e}") 


    def cancel_selected_work(self):
        print("Cancel work")
        selected_items = self.main_window.work_queue_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกคิวงานที่ต้องการลบ")
            return

        item_to_delete = selected_items[0]
        data = item_to_delete.data(0, Qt.UserRole)
        real_id_to_delete = data[0] # id อยู่ตำแหน่งแรก

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                     f"คุณต้องการลบคิวงานนี้ (ID: {real_id_to_delete}) ใช่หรือไม่?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
               
                self.db.delete_data_in_table_customer(real_id_to_delete)
                self.load_work_queue()
                self.load_customers_to_tree()
                QMessageBox.information(self.main_window, "สำเร็จ", "ลบคิวงานเรียบร้อยแล้ว")
            except Exception as e:
                QMessageBox.warning(self.main_window, "ผิดพลาด", f"ไม่สามารถลบข้อมูลได้: {e}")

    def start_selected_work(self):
        print("Start work")
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
        self.main_window.mix_wieght_target_wather_lineEdit.setText(str(target_water)) # ui คือ wather
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
        self.main_window.mix_monitor_wather_lineEdit.clear() # ui คือ wather
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
        self.main_window.mix_wieght_Loaded_wather_lineEdit.clear() # ui คือ wather
        self.main_window.mix_wieght_Loaded_chem_1_lineEdit.clear()
        self.main_window.mix_wieght_Loaded_chem_2_lineEdit.clear()
        self.main_window.mix_result_load_lineEdit.clear()
        self.main_window.mix_result_mix_lineEdit.clear()
        self.main_window.mix_result_mix_success_lineEdit.clear()
        self.main_window.mix_monitor_status_textEdit.clear()

    


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

    def set_offset_form_read_only(self, is_read_only):
        """ตั้งค่าช่องกรอกข้อมูล Offset ทั้งหมดเป็น ReadOnly หรือ Editable"""
        self.main_window.offset_rock_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_sand_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_rock_2_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_sand_2_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_cement_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_fyash_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_water_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_chem_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_chem_2_lineEdit.setReadOnly(is_read_only)

        self.main_window.offset_converyer_silo_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_opan_cement_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_run_mixer_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_time_next_load_lineEdit.setReadOnly(is_read_only)

    def load_offset_settings(self):
        """โหลดค่าจาก DB มาแสดงในหน้า Offset"""
        data = self.db.read_offset_settings()
        if data:

            self.main_window.offset_rock_1_lineEdit.setText(str(data[1]))
            self.main_window.offset_sand_1_lineEdit.setText(str(data[2]))
            self.main_window.offset_rock_2_lineEdit.setText(str(data[3]))
            self.main_window.offset_sand_2_lineEdit.setText(str(data[4]))
            self.main_window.offset_cement_lineEdit.setText(str(data[5]))
            self.main_window.offset_fyash_lineEdit.setText(str(data[6]))
            self.main_window.offset_water_lineEdit.setText(str(data[7]))
            self.main_window.offset_chem_1_lineEdit.setText(str(data[8]))
            self.main_window.offset_chem_2_lineEdit.setText(str(data[9]))

            self.main_window.offset_converyer_silo_time_lineEdit.setText(str(data[10]))
            self.main_window.offset_opan_cement_time_lineEdit.setText(str(data[11]))
            self.main_window.offset_run_mixer_time_lineEdit.setText(str(data[12]))
            self.main_window.offset_time_next_load_lineEdit.setText(str(data[13]))

    def offset_save(self):
        print("offset save")
        try:

            rock1 = float(self.main_window.offset_rock_1_lineEdit.text())
            sand1 = float(self.main_window.offset_sand_1_lineEdit.text())
            rock2 = float(self.main_window.offset_rock_2_lineEdit.text())
            sand2 = float(self.main_window.offset_sand_2_lineEdit.text())
            cement = float(self.main_window.offset_cement_lineEdit.text())
            fyash = float(self.main_window.offset_fyash_lineEdit.text())
            water = float(self.main_window.offset_water_lineEdit.text())
            chem1 = float(self.main_window.offset_chem_1_lineEdit.text())
            chem2 = float(self.main_window.offset_chem_2_lineEdit.text())

            conv_time = float(self.main_window.offset_converyer_silo_time_lineEdit.text())
            cement_time = float(self.main_window.offset_opan_cement_time_lineEdit.text())
            mixer_time = float(self.main_window.offset_run_mixer_time_lineEdit.text())
            next_time = float(self.main_window.offset_time_next_load_lineEdit.text())


            self.db.update_offset_settings(
                rock1, sand1, rock2, sand2, cement, fyash, water,
                chem1, chem2, conv_time, cement_time, mixer_time, next_time
            )

            self.set_offset_form_read_only(True)
            self.main_window.offset_save_pushButton.setEnabled(False)
            self.main_window.offset_edite_pushButton.setEnabled(True)
            self.main_window.offset_cancel_pushButton.setEnabled(False)

            QMessageBox.information(self.main_window, "บันทึกสำเร็จ", "บันทึกค่า Offset เรียบร้อยแล้ว")

        except ValueError:
            QMessageBox.warning(self.main_window, "ข้อมูลผิดพลาด", "กรุณากรอกข้อมูลเป็นตัวเลขให้ถูกต้อง")
        except Exception as e:
            QMessageBox.warning(self.main_window, "ผิดพลาด", f"เกิดข้อผิดพลาด: {e}")

    def offset_edite(self):
        print("offset edite")

        self.set_offset_form_read_only(False)
        self.main_window.offset_save_pushButton.setEnabled(True)
        self.main_window.offset_edite_pushButton.setEnabled(False)
        self.main_window.offset_cancel_pushButton.setEnabled(True)

    def offset_cancel(self):
        print("offset cancel")
        self.load_offset_settings()

        self.set_offset_form_read_only(True)
        self.main_window.offset_save_pushButton.setEnabled(False)
        self.main_window.offset_edite_pushButton.setEnabled(True)
        self.main_window.offset_cancel_pushButton.setEnabled(False)


# REG METHODS
    def Show_main(self):
        self.main_window.Show()

    def reg_add_formula(self):#REG TAB
        self.main_window.reg_formula_treeWidget.clear()
        all_formula_data = self.db.read_data_in_table_formula()
        for (display_number, db_row) in enumerate(all_formula_data, start=1):
            real_id = db_row[0]
            display_list = [str(display_number)] + [str(item) for item in db_row[1:]]
            tree_item = QTreeWidgetItem(display_list)
            tree_item.setData(0, Qt.UserRole, real_id)
            self.main_window.reg_formula_treeWidget.addTopLevelItem(tree_item)

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

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                     f"คุณต้องการลบลูกค้านี้ (ID: {real_id_to_delete}) ออกจากระบบถาวรหรือไม่?\n(ข้อมูลนี้จะหายไปจากคิวงานด้วย)",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_data_in_table_customer(real_id_to_delete)
                self.load_customers_to_tree()
                self.load_work_queue() 
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

    def reg_on_customer_item_clicked(self, item):#REG TAB
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

    def reg_on_formula_item_clicked(self, item):#REG TAB
        self.main_window.reg_formula_name_lineEdit.clear()
        formula_name = item.text(1)
        self.main_window.reg_formula_name_lineEdit.setText(formula_name)
# END REG METHODS
# FORMULA METHODS
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
            self.reg_add_formula()
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
            self.reg_add_formula()
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
            self.reg_add_formula()

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
# FORMULA METHODS END