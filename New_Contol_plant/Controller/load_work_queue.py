from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem
from Controller.temp_mixer import TempMixer
from datetime import datetime

class load_work_queue(QObject):
    def __init__(self, main_window, db, temp_queue, reg_tab=None):
        super(load_work_queue,  self).__init__()
        self.main_window = main_window
        self.db = db
        self.temp_queue = temp_queue  # Add temp_queue
        self.reg_tab = reg_tab
        self.current_mixer = None  # Store current TempMixer instance

        self._connect_signals()
        # self.load_work_queue()

    def _connect_signals(self):
        self.main_window.work_start_pushButton.clicked.connect(self.start_selected_work)
        self.main_window.work_cancel_pushButton.clicked.connect(self.cancel_selected_work)

    def load_work_queue(self):
        """Load work queue from temporary memory"""
        self.main_window.work_queue_treeWidget.clear()
        try:
            # Get orders from temporary queue instead of database
            work_data = self.temp_queue.get_all_orders()
            
            if not work_data:
                pass

            self.main_window.work_queue_treeWidget.setColumnWidth(0, 50)
            self.main_window.work_queue_treeWidget.setColumnWidth(1, 150)
            self.main_window.work_queue_treeWidget.setColumnWidth(2, 200)
            self.main_window.work_queue_treeWidget.setColumnWidth(3, 300)

            for (display_number, order) in enumerate(work_data, start=1):
                # Get formula data from database for material weights
                formula_data = self.db.get_formula_by_name(order['formula_name'])
                
                if not formula_data:
                    continue
                
                display_list = [
                    str(display_number),
                    str(order['formula_name']),
                    str(order['name']),
                    str(order['address']),
                    str(formula_data[0]),  # rock1
                    str(formula_data[1]),  # sand
                    str(formula_data[2]),  # rock2
                    str(formula_data[3]),  # cement
                    str(formula_data[4]),  # fly_ash
                    str(formula_data[5]),  # water
                    str(formula_data[6]),  # chem1
                    str(formula_data[7])   # chem2
                ]

                tree_item = QTreeWidgetItem(display_list)
                # Store order data with formula data combined
                combined_data = {
                    'temp_id': order['temp_id'],
                    'name': order['name'],
                    'phone_number': order['phone_number'],
                    'address': order['address'],
                    'formula_name': order['formula_name'],
                    'amount': order['amount'],
                    'rock1': formula_data[0],
                    'sand': formula_data[1],
                    'rock2': formula_data[2],
                    'cement': formula_data[3],
                    'fly_ash': formula_data[4],
                    'water': formula_data[5],
                    'chem1': formula_data[6],
                    'chem2': formula_data[7]
                }
                tree_item.setData(0, Qt.UserRole, combined_data)
                self.main_window.work_queue_treeWidget.addTopLevelItem(tree_item)
                
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
        temp_id = data['temp_id']
        customer_name = data['name']

        reply = QMessageBox.question(self.main_window, 'ยืนยันการลบ',
                                    f"คุณต้องการยกเลิกคิวงานของ '{customer_name}' ใช่หรือไม่?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Remove from temporary queue
                self.temp_queue.remove_order(temp_id)
                
                # Reload the tree widget
                self.load_work_queue()
                
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

        customer_name = data['name']
        phone_number = data['phone_number']
        address = data['address']
        formula_name = data['formula_name']
        amount = data['amount']
        target_rock1 = data['rock1']
        target_sand = data['sand']
        target_rock2 = data['rock2']
        target_cement = data['cement']
        target_flyash = data['fly_ash']
        target_water = data['water']
        target_chem1 = data['chem1']
        target_chem2 = data['chem2']

        # Create TempMixer object to store current work in temporary memory
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_mixer = TempMixer(
            id=data['temp_id'],
            dTime=current_time,
            customer_id=data.get('customer_id'),
            name=customer_name,
            phone_number=phone_number,
            address=address,
            formula_name=formula_name,
            amount=amount,
            keep_time=0,  # Will be updated during mixing
            truck_number=data.get('car_number', ''),
            rock1_weight=target_rock1,
            sand_weight=target_sand,
            rock2_weight=target_rock2,
            cement_weight=target_cement,
            fly_ash_weight=target_flyash,
            water_weight=target_water,
            chem1_weight=target_chem1,
            chem2_weight=target_chem2,
            age=0,  # Will be set based on formula if needed
            slump=0,  # Will be set based on formula if needed
            batch_state=2  # 2 = In production
        )

        print(f"✓ TempMixer created: {customer_name} | {formula_name} | Temp ID: {data['temp_id']}")

        # Load data to mixer UI
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
        
        # Remove from temporary queue after starting
        self.temp_queue.remove_order(data['temp_id'])
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

    def get_current_mixer(self):
        return self.current_mixer

    def update_mixer_totals(self, rock1=0, sand=0, rock2=0, cement=0, fly_ash=0, water=0, chem1=0, chem2=0):
        if self.current_mixer:
            self.current_mixer.rock1_total_weight += rock1
            self.current_mixer.sand_total_weight += sand
            self.current_mixer.rock2_total_weight += rock2
            self.current_mixer.cement_total_weight += cement
            self.current_mixer.fly_ash_total_weight += fly_ash
            self.current_mixer.water_total_weight += water
            self.current_mixer.chem1_total_weight += chem1
            self.current_mixer.chem2_total_weight += chem2
            print(f"✓ Updated totals - Rock1: {self.current_mixer.rock1_total_weight}, Cement: {self.current_mixer.cement_total_weight}")
        else:
            print("! Warning: No current mixer loaded")

    def finish_current_work(self):
        if self.current_mixer:
            completed_mixer = self.current_mixer
            print(f"✓ Work completed for: {completed_mixer.name}")
            print(f"  Total loaded - Rock1: {completed_mixer.rock1_total_weight}, "
                  f"Cement: {completed_mixer.cement_total_weight}, "
                  f"Water: {completed_mixer.water_total_weight}")
            
            # Clear current mixer
            self.current_mixer = None
            return completed_mixer
        else:
            print("! Warning: No current work to finish")
            return None