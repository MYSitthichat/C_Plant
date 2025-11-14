from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem
from Controller.temp_mixer import TempMixer
from Controller.Insert_to_customer_order import InsertToCustomerOrder
from datetime import datetime

class load_work_queue(QObject):
    def __init__(self, main_window, db, temp_queue, reg_tab=None):
        super(load_work_queue, self).__init__()
        self.main_window = main_window
        self.db = db
        self.temp_queue = temp_queue
        self.reg_tab = reg_tab
        self.current_mixer = None
        self.current_order_id = None  # Store database record ID
        
        # Create InsertToCustomerOrder instance
        self.order_inserter = InsertToCustomerOrder()

        self._connect_signals()

    def _connect_signals(self):
        self.main_window.work_start_pushButton.clicked.connect(self.start_selected_work)
        self.main_window.work_cancel_pushButton.clicked.connect(self.cancel_selected_work)

    def load_work_queue(self):
        """Load work queue from temporary memory"""
        self.main_window.work_queue_treeWidget.clear()
        try:
            work_data = self.temp_queue.get_all_orders()
            
            if not work_data:
                pass

            self.main_window.work_queue_treeWidget.setColumnWidth(0, 50)
            self.main_window.work_queue_treeWidget.setColumnWidth(1, 150)
            self.main_window.work_queue_treeWidget.setColumnWidth(2, 200)
            self.main_window.work_queue_treeWidget.setColumnWidth(3, 300)

            for (display_number, order) in enumerate(work_data, start=1):
                # Get formula data from database (includes age and slump)
                formula_data = self.db.get_formula_details_by_name(order['formula_name'])
                
                if not formula_data:
                    print(f"Warning: Formula '{order['formula_name']}' not found in database")
                    continue
                
                display_list = [
                    str(display_number),
                    str(order['formula_name']),
                    str(order['name']),
                    str(order['address']),
                    str(formula_data['rock1_weight']),
                    str(formula_data['sand_weight']),
                    str(formula_data['rock2_weight']),
                    str(formula_data['cement_weight']),
                    str(formula_data['fly_ash_weight']),
                    str(formula_data['water_weight']),
                    str(formula_data['chem1_weight']),
                    str(formula_data['chem2_weight'])
                ]

                tree_item = QTreeWidgetItem(display_list)
                
                # Store complete order data with formula data
                combined_data = {
                    'temp_id': order['temp_id'],
                    'customer_id': order.get('customer_id'),
                    'name': order['name'],
                    'phone_number': order['phone_number'],
                    'address': order['address'],
                    'formula_name': order['formula_name'],
                    'amount': order['amount'],
                    'car_number': order.get('car_number', ''),  # truck_number
                    'child_cement': order.get('child_cement', 0),  # keep_sample (0 or 1)
                    'comment': order.get('comment', ''),
                    # Formula data from database
                    'rock1_weight': formula_data['rock1_weight'],
                    'sand_weight': formula_data['sand_weight'],
                    'rock2_weight': formula_data['rock2_weight'],
                    'cement_weight': formula_data['cement_weight'],
                    'fly_ash_weight': formula_data['fly_ash_weight'],
                    'water_weight': formula_data['water_weight'],
                    'chem1_weight': formula_data['chem1_weight'],
                    'chem2_weight': formula_data['chem2_weight'],
                    'age': formula_data['age'],        # from concrete_formula table
                    'slump': formula_data['slump']     # from concrete_formula table
                }
                
                tree_item.setData(0, Qt.UserRole, combined_data)
                self.main_window.work_queue_treeWidget.addTopLevelItem(tree_item)
                
        except Exception as e:
            print(f"!!! Error during load_work_queue: {e}")
            import traceback
            traceback.print_exc()

    def cancel_selected_work(self):
        """Cancel selected work from queue"""
        selected_items = self.main_window.work_queue_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกคิวงานที่ต้องการยกเลิก")
            return

        item_to_cancel = selected_items[0]
        data = item_to_cancel.data(0, Qt.UserRole)
        temp_id = data['temp_id']
        customer_name = data['name']

        reply = QMessageBox.question(
            self.main_window, 
            'ยืนยันการลบ',
            f"คุณต้องการยกเลิกคิวงานของ '{customer_name}' ใช่หรือไม่?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.temp_queue.remove_order(temp_id)
                self.load_work_queue()
                QMessageBox.information(self.main_window, "สำเร็จ", "ยกเลิกคิวงานเรียบร้อยแล้ว")
            except Exception as e:
                QMessageBox.warning(self.main_window, "ผิดพลาด", f"เกิดข้อผิดพลาด: {e}")

    def start_selected_work(self):
        selected_items = self.main_window.work_queue_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.main_window, "ไม่มีรายการที่เลือก", "กรุณาเลือกคิวงานที่ต้องการเริ่ม")
            return

        item_to_start = selected_items[0]
        data = item_to_start.data(0, Qt.UserRole)

        # Extract ALL data (already from database via load_work_queue)
        customer_id = data.get('customer_id')
        customer_name = data['name']
        phone_number = data['phone_number']
        address = data['address']
        formula_name = data['formula_name']
        amount = data['amount']
        truck_number = data.get('car_number', '')      # car_number = truck_number
        
        # child_cement = keep_sample AND batch_state (0 or 1)
        # 1 = ต้องการเก็บ (want to keep sample)
        # 0 = ไม่ต้องการเก็บ (don't want to keep sample)
        keep_sample = data.get('child_cement', 0)      # This goes to both keep_sample and batch_state
        batch_state = keep_sample                       # batch_state = keep_sample value (0 or 1)
        
        # Target weights from database (concrete_formula)
        target_rock1 = data['rock1_weight']
        target_sand = data['sand_weight']
        target_rock2 = data['rock2_weight']
        target_cement = data['cement_weight']
        target_flyash = data['fly_ash_weight']
        target_water = data['water_weight']
        target_chem1 = data['chem1_weight']
        target_chem2 = data['chem2_weight']
        
        # Age and Slump from database (concrete_formula)
        age = data['age']
        slump = data['slump']

        # Create TempMixer object with ALL database values
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.current_mixer = TempMixer(
            id=None,                          # Auto-generated in database
            dTime=current_time,               # Current timestamp
            customer_id=customer_id,          # Customer ID (if exists)
            name=customer_name,               # Customer name
            phone_number=phone_number,        # Phone number
            address=address,                  # Address
            formula_name=formula_name,        # Formula name
            amount=amount,                    # Amount (cubic meters)
            keep_time=keep_sample,            # keep_sample (0 or 1)
            truck_number=truck_number,        # car_number = truck_number
            rock1_weight=target_rock1,        # Target from database
            sand_weight=target_sand,          # Target from database
            rock2_weight=target_rock2,        # Target from database
            cement_weight=target_cement,      # Target from database
            fly_ash_weight=target_flyash,     # Target from database
            water_weight=target_water,        # Target from database
            chem1_weight=target_chem1,        # Target from database
            chem2_weight=target_chem2,        # Target from database
            age=age,                          # Age from database (concrete_formula)
            slump=slump,                      # Slump from database (concrete_formula)
            batch_state=batch_state           # batch_state = keep_sample (0 or 1)
        )

        # === INSERT TO DATABASE (START) ===
        # All totals = 0, Status_load = 0, batch_state from child_cement
        try:
            record_id = self.order_inserter.insert_start(self.current_mixer)
            
            if record_id:
                self.current_order_id = record_id
                
                keep_text = "ต้องการเก็บตัวอย่าง" if batch_state == 1 else "ไม่ต้องการเก็บตัวอย่าง"
                
                QMessageBox.information(
                    self.main_window,
                    "เริ่มงานสำเร็จ",
                    f"ลูกค้า: {customer_name}\n"
                    f"สูตร: {formula_name}\n"
                )
            else:
                self.current_order_id = None
                QMessageBox.warning(
                    self.main_window,
                    "คำเตือน",
                    f"เริ่มงานแล้ว แต่ไม่สามารถบันทึกลงฐานข้อมูลได้\n"
                    f"ลูกค้า: {customer_name}"
                )
        except Exception as e:
            self.current_order_id = None
            print(f"✗ Error inserting to database: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(
                self.main_window,
                "คำเตือน",
                f"เริ่มงานแล้ว แต่เกิดข้อผิดพลาดในการบันทึก:\n{e}"
            )

        # Clear and update mixer tab UI
        self.clear_mixer_monitors()
        
        self.main_window.mix_customer_name_lineEdit.setText(customer_name)
        self.main_window.mix_customer_phone_lineEdit.setText(phone_number)
        self.main_window.mix_customer_formula_name_lineEdit.setText(formula_name)
        self.main_window.mix_number_cube_lineEdit.setText(str(amount))
        self.main_window.mix_result_load_lineEdit.setText(str(amount))
        self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(target_rock1))
        self.main_window.mix_wieght_target_sand_lineEdit.setText(str(target_sand))
        self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(target_rock2))
        self.main_window.mix_wieght_target_cement_lineEdit.setText(str(target_cement))
        self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(target_flyash))
        self.main_window.mix_wieght_target_water_lineEdit.setText(str(target_water))
        self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(target_chem1))
        self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(target_chem2))
        
        # Remove from temporary queue
        self.temp_queue.remove_order(data['temp_id'])
        self.load_work_queue()
        
        # Switch to mixer tab
        self.main_window.tab.setCurrentWidget(self.main_window.Mix_tab)

    def complete_current_work(self):
        if not self.current_mixer:
            QMessageBox.warning(
                self.main_window,
                "ไม่มีงาน",
                "ไม่มีงานที่กำลังดำเนินการอยู่"
            )
            return None
        
        if not self.current_order_id:
            QMessageBox.warning(
                self.main_window,
                "ข้อผิดพลาด",
                "ไม่พบรหัสออเดอร์ในระบบ\nไม่สามารถบันทึกผลการผลิตได้"
            )
            return None
        
        # === UPDATE DATABASE (COMPLETE) ===
        # Update with actual totals, Status_load=1
        # batch_state stays the same (0 or 1)
        try:
            success = self.order_inserter.update_complete(
                self.current_order_id,
                self.current_mixer
            )
            
            if success:
                keep_text = "ต้องการเก็บตัวอย่าง" if self.current_mixer.batch_state == 1 else "ไม่ต้องการเก็บตัวอย่าง"
                
                QMessageBox.information(
                    self.main_window,
                    "ทำงานเสร็จสิ้น",
                    f"บันทึกผลการผลิตเรียบร้อย\n"
                    f"ลูกค้า: {self.current_mixer.name}\n"
                )
                
                # Store references before clearing
                completed_mixer = self.current_mixer
                completed_order_id = self.current_order_id
                
                # Clear current work
                self.current_mixer = None
                self.current_order_id = None
                self.clear_mixer_monitors()
                
                return {
                    'mixer': completed_mixer,
                    'record_id': completed_order_id
                }
            else:
                QMessageBox.warning(
                    self.main_window,
                    "ผิดพลาด",
                    f"ไม่สามารถบันทึกผลการผลิตลงฐานข้อมูลได้\n"
                    f"รหัสออเดอร์: {self.current_order_id}"
                )
                return None
                
        except Exception as e:
            print(f"✗ Error updating complete: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(
                self.main_window,
                "ผิดพลาด",
                f"เกิดข้อผิดพลาดในการบันทึกผล:\n{e}"
            )
            return None

    def clear_mixer_monitors(self):
        """Clear all mixer weight monitors to zero"""
        self.main_window.mix_wieght_Loaded_rock_1_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_sand_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_rock_2_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_cement_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_fyash_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_water_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_chem_1_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_chem_2_lineEdit.setText("0")

    def get_current_mixer(self):
        """Get current TempMixer object"""
        return self.current_mixer
    
    def get_current_order_id(self):
        """Get current database record ID"""
        return self.current_order_id

    def update_mixer_totals(self, rock1=0, sand=0, rock2=0, cement=0, fly_ash=0, water=0, chem1=0, chem2=0):
        """Update total weights in current mixer during production"""
        if not self.current_mixer:
            return
        
        if rock1 > 0:
            self.current_mixer.rock1_total_weight += rock1
        if sand > 0:
            self.current_mixer.sand_total_weight += sand
        if rock2 > 0:
            self.current_mixer.rock2_total_weight += rock2
        if cement > 0:
            self.current_mixer.cement_total_weight += cement
        if fly_ash > 0:
            self.current_mixer.fly_ash_total_weight += fly_ash
        if water > 0:
            self.current_mixer.water_total_weight += water
        if chem1 > 0:
            self.current_mixer.chem1_total_weight += chem1
        if chem2 > 0:
            self.current_mixer.chem2_total_weight += chem2