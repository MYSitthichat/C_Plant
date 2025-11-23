from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject, QTimer, Signal
from PySide6.QtWidgets import QMessageBox,QApplication
from threading import Thread
import time
import sys
from Controller.database_control import C_palne_Database
from Controller.PLC_controller import PLC_Controller
from Controller.Autoda_controller import AUTODA_Controller
from Controller.temp_queue import TempQueue
from Controller.reg_tab import reg_tab
from Controller.load_work_queue import load_work_queue
from Controller.formula_tab import formula_tab
from Controller.offset_tab import offset_tab
from Controller.debug_tab import debug_tab

class MainController(QObject):
    action = Slot(str)
    work_completed = Signal(float)
    # Signal สำหรับส่งข้อความไปยัง UI จาก Thread อย่างปลอดภัย
    status_message = Signal(str)
    # Signal สำหรับ reset UI อย่างปลอดภัยจาก worker thread
    reset_ui_signal = Signal()
    switch_to_work_tab_signal = Signal()
    # Signal สำหรับจัดการ QTimer จาก main thread อย่างปลอดภัย
    request_stop_target_monitor = Signal()
    request_start_target_monitor = Signal()
    # Signal สำหรับ finalize reset จาก worker thread
    finalize_reset_signal = Signal(float)  # ส่งค่า total_cubes
    
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()

        self.db = C_palne_Database()
        self.data_formula = []
        self.rock1_offset = 0
        self.sand_offset = 0
        self.rock2_offset = 0
        self.cement_offset = 0
        self.fyash_offset = 0
        self.water_offset = 0
        self.chem1_offset = 0
        self.chem2_offset = 0
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Rock and Sand
        self.rock1_frozen_weight = 0
        self.sand_frozen_weight = 0  # น้ำหนักรวมเมื่อ Sand เสร็จ
        self.rock2_frozen_weight = 0  # น้ำหนักรวมเมื่อ Rock2 เสร็จ
        self.sand_only_frozen = 0  # น้ำหนักเฉพาะ Sand
        self.rock2_only_frozen = 0  # น้ำหนักเฉพาะ Rock2
        self.is_rock1_frozen = False
        self.is_sand_frozen = False
        self.is_rock2_frozen = False
        
        # ตัวแปรสำหรับ stabilization delay
        self.rock1_stabilizing = False
        self.sand_stabilizing = False
        self.rock2_stabilizing = False
        self.rock1_stabilize_start_time = 0
        self.sand_stabilize_start_time = 0
        self.rock2_stabilize_start_time = 0
        self.stabilize_delay = 5  # วินาที
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Cement and Fyash
        self.cement_frozen_weight = 0
        self.fyash_frozen_weight = 0
        self.fyash_only_frozen = 0
        self.is_cement_frozen = False
        self.is_fyash_frozen = False
        self.cement_stabilizing = False
        self.fyash_stabilizing = False
        self.cement_stabilize_start_time = 0
        self.fyash_stabilize_start_time = 0
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Water
        self.water_frozen_weight = 0
        self.is_water_frozen = False
        self.water_stabilizing = False
        self.water_stabilize_start_time = 0
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Chemical
        self.chem1_frozen_weight = 0
        self.chem2_frozen_weight = 0
        self.chem2_only_frozen = 0
        self.is_chem1_frozen = False
        self.is_chem2_frozen = False
        self.chem1_stabilizing = False
        self.chem2_stabilizing = False
        self.chem1_stabilize_start_time = 0
        self.chem2_stabilize_start_time = 0
        
        # ตัวแปรเป้าหมายน้ำหนัก
        self.target_rock1_weight = 0
        self.target_sand_total_weight = 0
        self.target_rock2_total_weight = 0
        self.target_cement_weight = 0
        self.target_fyash_total_weight = 0
        self.target_water_weight = 0
        self.target_chem1_weight = 0
        self.target_chem2_total_weight = 0
        
        # ตัวแปรเป้าหมายที่แสดงใน UI (สำหรับแต่ละรอบโหลด)
        self.display_target_rock1 = 0
        self.display_target_sand = 0
        self.display_target_rock2 = 0
        self.display_target_cement = 0
        self.display_target_fyash = 0
        self.display_target_water = 0
        self.display_target_chem1 = 0
        self.display_target_chem2 = 0
        
        # ตัวแปรสำหรับจัดการคิว
        self.total_queue_count = 1  # จำนวนคิวทั้งหมดที่ต้องโหลด
        self.current_queue_loaded = 0  # จำนวนคิวที่โหลดไปแล้ว
        self.current_queue_transporting = 0  # จำนวนคิวที่กำลังลำเลียงขึ้นไปผสม
        self.completed_queue_count = 0  # จำนวนคิวที่ผสมเสร็จแล้ว (นับเป็นคิว)
        self.queue_multiplier = 1.0  # ตัวคูณสำหรับปรับจำนวนวัตถุดิบ
        self.queue_multipliers = []  # List ของ multiplier สำหรับแต่ละรอบโหลด
        self.original_rock1 = 0
        self.original_sand = 0
        self.original_rock2 = 0
        self.original_cement = 0
        self.original_fyash = 0
        self.original_water = 0
        self.original_chem1 = 0
        self.original_chem2 = 0
        self.ready_to_start_next_load = False
        self.next_queue_loaded_and_ready = False  # Flag บอกว่าคิวถัดไปโหลดเสร็จแล้วพร้อมลำเลียง
        self.lock_target_display = False  # Flag ป้องกันการ reset Target UI ระหว่างโหลด
        self.close_vale_mixer_when_waiting = False  # ปิดวาล์วมิกเซอร์ขณะรอคิวถัดไป
        self.is_tab_switching = False  # Flag ป้องกันการ access UI widgets ระหว่าง switch tab

        # Loading control variables
        # ROCK AND SAND STATE
        self.rock_and_sand_values = []
        self.is_loading_rock_and_sand_in_progress = False
        self.thread_rock_and_sand = None
        self.state_load_rock_and_sand = 0
        self.rock_and_sand_loading_success = False
        self.rock_success = False
        self.rock_and_sand_success_start_main = False
        # ROCK AND SAND STATE
        # CEMENT AND FYASH STATE
        self.cement_and_fyash_values = []
        self.is_loading_cement_and_fyash_in_progress = False
        self.thread_cement_and_fyash = None
        self.state_load_cement_and_fyash = 0
        self.cement_and_fyash_loading_success = False
        self.cement_and_fyash_success_start_main = False
        
        # new added function 
        self.reset_variable_for_cement_loaded()

        # CEMENT AND FYASH STATE
        # WATER STATE
        self.water_value = 0
        self.is_loading_water_in_progress = False
        self.thread_water = None
        self.state_load_water = 0
        self.water_loading_success = False
        self.water_success_start_main = False
        # WATER STATE
        # CHEMICAL STATE
        self.chemical_values = []
        self.is_loading_chemical_in_progress = False
        self.thread_chemical = None
        self.state_load_chemical = 0
        self.chemical_loading_success = False
        self.chemical_success = False
        self.chemical_success_start_main = False
        # CHEMICAL STATE
        # MAIN CONDITION LOAD THREAD
        self.thread_main_condition_load = None
        self.main_condition_load_running = False
        self.state_main_condition_load = 0
        # MAIN CONDITION LOAD THREAD
        self.start_button_load_enabled = False
        self.is_workflow_active = False  # Flag เพื่อบอกว่า workflow กำลังทำงานหรือไม่
        # check weight to stop control
        self.this_weight_to_stop_control = 0
        self.countdown_to_stop = 0
        self.offset_weight_to_stop_control = 200
        # Create temp queue instance
        self.temp_queue = TempQueue()

        # reg tab
        self.reg_tab = reg_tab(self.main_window, self.db, self.temp_queue)

        # work queue tab
        self.load_work_queue = load_work_queue(self.main_window, self.db, self.temp_queue, self.reg_tab)
        
        # Link them together
        self.reg_tab.set_work_queue(self.load_work_queue)

        # formula tab
        self.formula_tab = formula_tab(self.main_window, self.db, self.reg_tab)

        # offset tab
        self.offset_tab = offset_tab(self.main_window, self.db)

        # mix control tab
        self.plc_controller = PLC_Controller(self.main_window, self.db)
        self.plc_controller.comport_error.connect(self.update_status_port)
        self.plc_controller.status_loading_rock_and_sand.connect(self.check_loading_rock_and_sand)
        self.plc_controller.status_loading_cement_and_fyash.connect(self.check_loading_cement_and_fyash)
        self.plc_controller.status_loading_water.connect(self.check_loading_water)
        self.plc_controller.status_loading_chemical.connect(self.check_loading_chemical)
        self.plc_controller.device_status_changed.connect(self.update_device_status_indicator)
        self.plc_controller.initialize_connections()
        self.plc_controller.start()

        self.autoda_controller = AUTODA_Controller(self.main_window, self.db)
        self.autoda_controller.comport_error.connect(self.update_status_port)
        self.autoda_controller.weight_rock_and_sand.connect(self.update_weight_rock_and_sand)
        self.autoda_controller.weight_cement_and_fyash.connect(self.update_weight_cement_and_fyash)
        self.autoda_controller.weight_water.connect(self.update_weight_water)
        self.autoda_controller.weight_chemical.connect(self.update_weight_chemical)

        # debug tab
        self.debug_tab = debug_tab(self.main_window,self.plc_controller)

        self.autoda_controller.initialize_connections()
        self.autoda_controller.start()

        self.main_window.mix_start_load_pushButton.clicked.connect(self.mix_start_load)
        self.main_window.mix_cancel_load_pushButton.clicked.connect(self.mix_cancel_load)
        
        # Connect signal สำหรับแจ้งเตือนงานเสร็จ
        self.work_completed.connect(self._show_completion_message)
        
        # Connect signal สำหรับแสดงข้อความสถานะจาก Thread
        self.status_message.connect(self._append_status_message)
        
        # Connect signals สำหรับ reset UI และ switch tab อย่างปลอดภัย
        self.reset_ui_signal.connect(self._reset_ui_safe)
        self.switch_to_work_tab_signal.connect(self._switch_to_work_tab_safe)
        
        # Connect signals สำหรับจัดการ QTimer จาก main thread อย่างปลอดภัย
        self.request_stop_target_monitor.connect(self._stop_target_monitor_safe)
        self.request_start_target_monitor.connect(self._start_target_monitor_safe)
        
        # Connect signal สำหรับ finalize reset
        self.finalize_reset_signal.connect(self._finalize_reset)

        self.main_window.set_readonly_mix_weights()
        self.read_offset_formular_mixer()
        # self.plc_controller.off_all_device()
        
        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self.cleanup_on_exit)
        
    @Slot(list)
    @Slot(int)
    
    @Slot(str)
    def _append_status_message(self, message):
        """Slot สำหรับรับข้อความจาก Thread และแสดงใน UI อย่างปลอดภัย"""
        try:
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
                
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
                self.main_window.mix_monitor_status_textEdit.objectName()
            except RuntimeError:
                return
                
            self.main_window.mix_monitor_status_textEdit.append(message)
        except RuntimeError:
            # Qt object ถูก destroy แล้ว
            pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน crash
            pass
    
    @Slot(str, bool)
    def update_device_status_indicator(self, device_name, is_running):
        """อัพเดทสีพื้นหลังของ Label ตามสถานะอุปกรณ์"""
        try:
            # ตรวจสอบว่าไม่ได้อยู่ในช่วง tab switching
            if getattr(self, 'is_tab_switching', False):
                return
            
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
            
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                return
            
            # ตรวจสอบว่า application ยังทำงานอยู่
            app = QApplication.instance()
            if app is None or app.closingDown():
                return
            
            # ตรวจสอบว่าเรากำลังอยู่ที่ mixer_tab หรือไม่
            # ถ้าไม่ใช่ ให้ข้ามการ update เพื่อป้องกัน segfault
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'Mix_tab'):
                try:
                    current_tab = self.main_window.tab.currentWidget()
                    if current_tab != self.main_window.Mix_tab:
                        # ไม่อยู่ที่ mixer_tab ให้ข้าม
                        return
                except RuntimeError:
                    # Widget ถูก destroy แล้ว
                    return
                
            # สีเขียวเมื่อทำงาน, สีปกติเมื่อหยุด
            active_color = "background-color: #4CAF50; color: white; font-weight: bold; border: 2px solid #2E7D32; border-radius: 10px;"
            inactive_color = "border: 2px solid; border-radius: 10px;"
            
            # Dictionary สำหรับ mapping device name กับ Label widgets ใน UI
            device_labels = {
                # วัตถุดิบ
                "rock1": getattr(self.main_window, 'mix_monitor_rock_1_label', None),
                "sand": getattr(self.main_window, 'mix_monitor_sand_label', None),
                "rock2": getattr(self.main_window, 'mix_monitor_rock_2_label', None),
                "cement": getattr(self.main_window, 'mix_monitor_cement_label', None),
                "flyash": getattr(self.main_window, 'mix_monitor_fyash_label', None),
                "water": getattr(self.main_window, 'mix_monitor_water_label', None),
                "chemical1": getattr(self.main_window, 'mix_monitor_chem_1_label', None),
                "chemical2": getattr(self.main_window, 'mix_monitor_chem_2_label', None),
                
                # อุปกรณ์
                "mixer": getattr(self.main_window, 'mix_monitor_mixer_label', None),
                "conveyor_middle": getattr(self.main_window, 'mix_monitor_converyer_rock_label', None),
                "valve_cement_flyash": getattr(self.main_window, 'mix_monitor_vale_fyash_and_cement_label', None),
                "valve_water": getattr(self.main_window, 'mix_monitor_vale_wather_label', None),
                "pump_chemical": getattr(self.main_window, 'mix_monitor_pump_chem_label', None),
                "valve_mixer": getattr(self.main_window, 'mix_monitor_main_vale_label', None),
            }
            
            # ดึง label ที่ตรงกับ device_name
            label = device_labels.get(device_name)
            
            if label:
                try:
                    # ตรวจสอบว่า label ยังใช้งานได้
                    label.objectName()
                    if is_running:
                        label.setStyleSheet(active_color)
                    else:
                        label.setStyleSheet(inactive_color)
                except RuntimeError:
                    # Label ถูก destroy แล้ว
                    pass
        except RuntimeError:
            # Qt object ถูก destroy แล้ว
            pass
        except Exception as e:
            # Suppress errors to prevent crash
            pass
    
    def read_offset_formular_mixer(self):
        result_offset = self.db.read_offset_settings()
        if result_offset:
            self.rock1_offset = result_offset[1]
            self.sand_offset = result_offset[2]
            self.rock2_offset = result_offset[3]
            self.cement_offset = result_offset[5]
            self.fyash_offset = result_offset[6]
            self.water_offset = result_offset[7]
            self.chem1_offset = result_offset[8]
            self.chem2_offset = result_offset[9]
            self.converyer_time = result_offset[10]
            self.cement_release_time = result_offset[11]
            self.mixer_start_time = result_offset[12]
            self.next_load_delay_time = result_offset[13]
        else:
            print("No offset settings found in database.")

# ROCK AND SAND WEIGHT HANDLING
    def _set_weight_display(self, material, weight):
        """Set weight display - Thread Safe"""
        try:
            if not hasattr(self, 'main_window'):
                return
                
            if material == "rock1":
                self.main_window.mix_monitor_rock_1_lineEdit.setText(str(weight))
                self.main_window.mix_wieght_Loaded_rock_1_lineEdit.setText(str(weight))
            elif material == "sand":
                self.main_window.mix_monitor_sand_lineEdit.setText(str(weight))
                self.main_window.mix_wieght_Loaded_sand_lineEdit.setText(str(weight))
            elif material == "rock2":
                self.main_window.mix_monitor_rock_2_lineEdit.setText(str(weight))
                self.main_window.mix_wieght_Loaded_rock_2_lineEdit.setText(str(weight))
        except Exception as e:
            # Suppress UI update errors
            pass

    def _get_display_weight(self, material, current_weight):
        """Get display weight based on freeze status and loading sequence (Sand → Rock1 → Rock2)"""
        if material == "sand":
            # Sand โหลดก่อน จึงแสดงน้ำหนักตรง ๆ
            return self.sand_frozen_weight if self.is_sand_frozen else current_weight
        elif material == "rock1":
            # Rock1 โหลดที่ 2 จึงต้องหัก Sand ออก
            if self.is_rock1_frozen and hasattr(self, 'rock1_only_frozen'):
                return self.rock1_only_frozen
            else:
                rock1_only = current_weight - self.sand_frozen_weight if self.is_sand_frozen else current_weight
                return max(0, rock1_only)
        elif material == "rock2":
            # Rock2 โหลดสุดท้าย จึงต้องหัก Rock1 ออก (ซึ่ง Rock1 รวม Sand อยู่แล้ว)
            if self.is_rock2_frozen and hasattr(self, 'rock2_only_frozen'):
                return self.rock2_only_frozen
            else:
                rock2_only = current_weight - self.rock1_frozen_weight if self.is_rock1_frozen else 0
                return max(0, rock2_only)
        return current_weight

    def _check_freeze_conditions(self, current_weight):
        current_time = time.time()
        
        # ตรวจสอบ Sand freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize (โหลดก่อน)
        if (self.state_load_rock_and_sand == 2 and self.rock_success and not self.is_sand_frozen):
            if not self.sand_stabilizing:
                self.sand_stabilizing = True
                self.sand_stabilize_start_time = current_time
                print(f"🏖️ Sand PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.sand_stabilize_start_time >= self.stabilize_delay:
                self.sand_frozen_weight = current_weight
                self.sand_only_frozen = current_weight  # Sand โหลดก่อน จึงเป็นน้ำหนักเดี่ยว
                self.is_sand_frozen = True
                self.sand_stabilizing = False
                print(f"✅ Sand frozen at: {self.sand_frozen_weight} kg (Sand only: {self.sand_only_frozen} kg)")

        # ตรวจสอบ Rock1 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize (โหลดที่ 2)
        if (self.state_load_rock_and_sand == 4 and self.rock_success and not self.is_rock1_frozen):
            if not self.rock1_stabilizing:
                self.rock1_stabilizing = True
                self.rock1_stabilize_start_time = current_time
                print(f"🪨 Rock1 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.rock1_stabilize_start_time >= self.stabilize_delay:
                self.rock1_frozen_weight = current_weight
                self.rock1_only_frozen = max(0, current_weight - self.sand_frozen_weight if self.is_sand_frozen else current_weight)
                self.is_rock1_frozen = True
                self.rock1_stabilizing = False
                print(f"✅ Rock1 frozen at total: {self.rock1_frozen_weight} kg (Rock1 only: {self.rock1_only_frozen} kg)")

        # ตรวจสอบ Rock2 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize (โหลดสุดท้าย)
        if (self.state_load_rock_and_sand == 6 and self.rock_success and not self.is_rock2_frozen):
            if not self.rock2_stabilizing:
                self.rock2_stabilizing = True
                self.rock2_stabilize_start_time = current_time
                print(f"🪨 Rock2 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.rock2_stabilize_start_time >= self.stabilize_delay:
                self.rock2_frozen_weight = current_weight
                # Rock2 โหลดทีหลัง ต้องหัก Rock1 (ที่รวม Sand อยู่แล้ว) ออก
                rock1_total = self.rock1_frozen_weight if self.is_rock1_frozen else self.sand_frozen_weight if self.is_sand_frozen else 0
                self.rock2_only_frozen = max(0, current_weight - rock1_total)
                self.is_rock2_frozen = True
                self.rock2_stabilizing = False
                print(f"✅ Rock2 frozen at total: {self.rock2_frozen_weight} kg (Rock2 only: {self.rock2_only_frozen} kg)")

    def update_weight_rock_and_sand(self, weight):
        try:
            # ตรวจสอบว่าไม่ได้อยู่ในช่วง tab switching
            if getattr(self, 'is_tab_switching', False):
                return
            
            # ป้องกัน race condition - ถ้าไม่ได้กำลังโหลดอยู่ ให้ข้าม
            if not hasattr(self, 'is_loading_rock_and_sand_in_progress'):
                return
            
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
            
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบว่าอยู่ใน mixer_tab หรือไม่
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'Mix_tab'):
                try:
                    current_tab = self.main_window.tab.currentWidget()
                    if current_tab != self.main_window.Mix_tab:
                        return
                except RuntimeError:
                    return
            
            current_weight = int(weight)
            self.this_weight_to_stop_control = current_weight
            
            if self.is_loading_rock_and_sand_in_progress:
                self._check_freeze_conditions(current_weight)
            
            # อัพเดท display ตามลำดับใหม่: Sand → Rock1 → Rock2
            if self.state_load_rock_and_sand == 2:  # Loading Sand (state 2)
                self._set_weight_display("sand", current_weight)
                self._set_weight_display("rock1", 0)
                self._set_weight_display("rock2", 0)
            elif self.state_load_rock_and_sand == 4:  # Loading Rock1 (state 4)
                self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
                self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
                self._set_weight_display("rock2", 0)
            elif self.state_load_rock_and_sand == 6:  # Loading Rock2 (state 6)
                self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
                self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
                self._set_weight_display("rock2", self._get_display_weight("rock2", current_weight))
            elif self.state_load_rock_and_sand in [3, 5]:  # Transition states
                self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
                if self.state_load_rock_and_sand == 5:
                    self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
                else:
                    self._set_weight_display("rock1", 0)
                self._set_weight_display("rock2", 0)
            else:  # Default state (loading complete or not loading)
                self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
                self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
                self._set_weight_display("rock2", self._get_display_weight("rock2", current_weight))
        except RuntimeError:
            # Qt object ถูก destroy แล้ว ให้ข้ามไป
            pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน segmentation fault
            pass
# END ROCK AND SAND WEIGHT HANDLING

# CEMENT AND FYASH WEIGHT HANDLING
    def _set_cement_fyash_display(self, material, weight):
        if material == "cement":
            self.main_window.mix_monitor_cement_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_cement_lineEdit.setText(str(weight))
        elif material == "fyash":
            self.main_window.mix_monitor_fyash_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_fyash_lineEdit.setText(str(weight))

    def _get_cement_fyash_display_weight(self, material, current_weight):
        if material == "fyash":
            # Flyash โหลดก่อน ดังนั้นแสดงน้ำหนักเฉพาะ flyash (ไม่รวม cement)
            return getattr(self, 'fyash_frozen_weight', current_weight) if getattr(self, 'is_fyash_frozen', False) else current_weight
        elif material == "cement":
            # Cement โหลดทีหลัง ดังนั้นต้องหัก flyash ออก
            if getattr(self, 'is_cement_frozen', False) and hasattr(self, 'cement_frozen_weight'):
                # น้ำหนักรวมตอนโหลด cement เสร็จ - น้ำหนัก flyash = น้ำหนัก cement เฉพาะตัว
                fyash_frozen = getattr(self, 'fyash_frozen_weight', 0)
                cement_only = self.cement_frozen_weight - fyash_frozen if getattr(self, 'is_fyash_frozen', False) else self.cement_frozen_weight
                return max(0, cement_only)
            else:
                # กำลังโหลด cement อยู่ ต้องหัก flyash ที่โหลดไปแล้วออก
                fyash_frozen = getattr(self, 'fyash_frozen_weight', 0)
                cement_only = current_weight - fyash_frozen if getattr(self, 'is_fyash_frozen', False) else current_weight
                return max(0, cement_only)
        return current_weight

    def _check_cement_fyash_freeze_conditions(self, current_weight):
        current_time = time.time()
        
        # ตรวจสอบ Flyash freeze - โหลดก่อน (state 2)
        if (self.state_load_cement_and_fyash == 2 and 
            getattr(self, 'cement_success', False) and 
            not getattr(self, 'is_fyash_frozen', False)):
            
            if not self.fyash_stabilizing:
                self.fyash_stabilizing = True
                self.fyash_stabilize_start_time = current_time
                # print(f"Flyash PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.fyash_stabilize_start_time >= self.stabilize_delay:
                self.fyash_frozen_weight = current_weight
                self.is_fyash_frozen = True
                self.fyash_stabilizing = False
                # print(f"Flyash frozen at: {self.fyash_frozen_weight}")

        # ตรวจสอบ Cement freeze - โหลดทีหลัง (state 4)
        if (self.state_load_cement_and_fyash == 4 and
            getattr(self, 'cement_success', False) and
            not getattr(self, 'is_cement_frozen', False)):
            
            if not self.cement_stabilizing:
                self.cement_stabilizing = True
                self.cement_stabilize_start_time = current_time
                # print(f"Cement PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.cement_stabilize_start_time >= self.stabilize_delay:
                self.cement_frozen_weight = current_weight
                self.is_cement_frozen = True
                self.cement_stabilizing = False
                # print(f"Cement frozen at total: {self.cement_frozen_weight}")

    def update_weight_cement_and_fyash(self, weight):
        try:
            # ตรวจสอบว่าไม่ได้อยู่ในช่วง tab switching
            if getattr(self, 'is_tab_switching', False):
                return
            
            # ป้องกัน race condition
            if not hasattr(self, 'is_loading_cement_and_fyash_in_progress'):
                return
            
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
            
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบว่าอยู่ใน mixer_tab หรือไม่
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'Mix_tab'):
                try:
                    current_tab = self.main_window.tab.currentWidget()
                    if current_tab != self.main_window.Mix_tab:
                        return
                except RuntimeError:
                    return
                
            current_weight = int(weight)
            
            # Check freeze conditions during loading
            if getattr(self, 'is_loading_cement_and_fyash_in_progress', False):
                self._check_cement_fyash_freeze_conditions(current_weight)

            state = getattr(self, 'state_load_cement_and_fyash', 0)
            if state == 2:  # Loading Flyash ก่อน
                self._set_cement_fyash_display("fyash", current_weight)
                self._set_cement_fyash_display("cement", 0)
            elif state == 4:  # Loading Cement ทีหลัง
                self._set_cement_fyash_display("fyash", self._get_cement_fyash_display_weight("fyash", current_weight))
                self._set_cement_fyash_display("cement", self._get_cement_fyash_display_weight("cement", current_weight))
            elif state == 3:  # Transition state (เปลี่ยนจาก Flyash ไป Cement)
                self._set_cement_fyash_display("fyash", self._get_cement_fyash_display_weight("fyash", current_weight))
                self._set_cement_fyash_display("cement", 0)
            else:  # Default state (loading complete or not loading)
                self._set_cement_fyash_display("fyash", self._get_cement_fyash_display_weight("fyash", current_weight))
                self._set_cement_fyash_display("cement", self._get_cement_fyash_display_weight("cement", current_weight))
        except RuntimeError:
            # Qt object ถูก destroy แล้ว ให้ข้ามไป
            pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน segmentation fault
            pass
# END ROCK AND SAND WEIGHT HANDLING

# WATER WEIGHT HANDLING
    def _set_water_display(self, weight):
        """Helper function to set water weight display"""
        self.main_window.mix_monitor_water_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_water_lineEdit.setText(str(weight))

    def _get_water_display_weight(self, current_weight):
        """Get water display weight based on freeze status"""
        return getattr(self, 'water_frozen_weight', current_weight) if getattr(self, 'is_water_frozen', False) else current_weight

    def _check_water_freeze_conditions(self, current_weight):
        """Check and update water freeze conditions"""
        current_time = time.time()
        
        # ตรวจสอบ Water freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_water == 2 and 
            getattr(self, 'water_success', False) and 
            not getattr(self, 'is_water_frozen', False)):
            
            if not self.water_stabilizing:
                self.water_stabilizing = True
                self.water_stabilize_start_time = current_time
                # print(f"Water PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.water_stabilize_start_time >= self.stabilize_delay:
                self.water_frozen_weight = current_weight
                self.is_water_frozen = True
                self.water_stabilizing = False
                # print(f"Water frozen at: {self.water_frozen_weight}")

    def update_weight_water(self, weight):
        try:
            # ตรวจสอบว่าไม่ได้อยู่ในช่วง tab switching
            if getattr(self, 'is_tab_switching', False):
                return
            
            # ป้องกัน race condition
            if not hasattr(self, 'is_loading_water_in_progress'):
                return
            
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
            
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบว่าอยู่ใน mixer_tab หรือไม่
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'Mix_tab'):
                try:
                    current_tab = self.main_window.tab.currentWidget()
                    if current_tab != self.main_window.Mix_tab:
                        return
                except RuntimeError:
                    return
                
            current_weight = int(weight)
            
            # Check freeze conditions during loading
            if getattr(self, 'is_loading_water_in_progress', False):
                self._check_water_freeze_conditions(current_weight)

            # Always display the appropriate weight (frozen or current)
            self._set_water_display(self._get_water_display_weight(current_weight))
        except RuntimeError:
            # Qt object ถูก destroy แล้ว ให้ข้ามไป
            pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน segmentation fault
            pass
# END WATER WEIGHT HANDLING        

# CHEMICAL WEIGHT HANDLING
    def _set_chemical_display(self, material, weight):
        """Helper function to set chemical weight display"""
        if material == "chem1":
            self.chem1_weight = round(weight, 2)
            self.main_window.mix_monitor_chem_1_lineEdit.setText(str(self.chem1_weight))
            self.main_window.mix_wieght_Loaded_chem_1_lineEdit.setText(str(self.chem1_weight))
        elif material == "chem2":
            self.chem2_weight = round(weight, 2)
            self.main_window.mix_monitor_chem_2_lineEdit.setText(str(self.chem2_weight))
            self.main_window.mix_wieght_Loaded_chem_2_lineEdit.setText(str(self.chem2_weight))

    def _get_chemical_display_weight(self, material, current_weight):
        """Get chemical display weight based on freeze status"""
        if material == "chem1":
            return getattr(self, 'chem1_frozen_weight', current_weight) if getattr(self, 'is_chem1_frozen', False) else current_weight
        elif material == "chem2":
            if getattr(self, 'is_chem2_frozen', False) and hasattr(self, 'chem2_only_frozen'):
                return self.chem2_only_frozen
            else:
                chem1_frozen = getattr(self, 'chem1_frozen_weight', 0)
                chem2_only = current_weight - chem1_frozen if getattr(self, 'is_chem1_frozen', False) else current_weight
                return max(0, chem2_only)
        return current_weight

    def _check_chemical_freeze_conditions(self, current_weight):
        current_time = time.time()
        
        # ตรวจสอบ Chem1 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_chemical == 2 and 
            getattr(self, 'chemical_success', False) and 
            not getattr(self, 'is_chem1_frozen', False)):
            
            if not self.chem1_stabilizing:
                self.chem1_stabilizing = True
                self.chem1_stabilize_start_time = current_time
                # print(f"Chem1 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.chem1_stabilize_start_time >= self.stabilize_delay:
                self.chem1_frozen_weight = current_weight
                self.is_chem1_frozen = True
                self.chem1_stabilizing = False
                # print(f"Chem1 frozen at: {self.chem1_frozen_weight}")
                
        # ตรวจสอบ Chem2 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_chemical == 4 and 
            getattr(self, 'chemical_success', False) and 
            not getattr(self, 'is_chem2_frozen', False)):
            
            if not self.chem2_stabilizing:
                self.chem2_stabilizing = True
                self.chem2_stabilize_start_time = current_time
                # print(f"Chem2 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.chem2_stabilize_start_time >= self.stabilize_delay:
                self.chem2_frozen_weight = current_weight
                chem1_frozen = getattr(self, 'chem1_frozen_weight', 0)
                self.chem2_only_frozen = max(0, current_weight - chem1_frozen if getattr(self, 'is_chem1_frozen', False) else current_weight)
                self.is_chem2_frozen = True
                self.chem2_stabilizing = False
                # print(f"Chem2 frozen at total: {self.chem2_frozen_weight} (Chem2 only: {self.chem2_only_frozen})")

    def update_weight_chemical(self, weight):
        try:
            # ตรวจสอบว่าไม่ได้อยู่ในช่วง tab switching
            if getattr(self, 'is_tab_switching', False):
                return
            
            # ป้องกัน race condition
            if not hasattr(self, 'is_loading_chemical_in_progress'):
                return
            
            # ตรวจสอบว่า workflow ยังทำงานอยู่หรือไม่
            if not getattr(self, 'is_workflow_active', False):
                return
            
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบว่าอยู่ใน mixer_tab หรือไม่
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'Mix_tab'):
                try:
                    current_tab = self.main_window.tab.currentWidget()
                    if current_tab != self.main_window.Mix_tab:
                        return
                except RuntimeError:
                    return
                
            current_weight = float(weight)
            if getattr(self, 'is_loading_chemical_in_progress', False):
                self._check_chemical_freeze_conditions(current_weight)
                
            state = getattr(self, 'state_load_chemical', 0)
            if state == 2:
                self._set_chemical_display("chem1", current_weight)
                self._set_chemical_display("chem2", 0)
            elif state == 4:
                self._set_chemical_display("chem1", self._get_chemical_display_weight("chem1", current_weight))
                self._set_chemical_display("chem2", self._get_chemical_display_weight("chem2", current_weight))
            elif state == 3:
                self._set_chemical_display("chem1", self._get_chemical_display_weight("chem1", current_weight))
                self._set_chemical_display("chem2", 0)
            else:
                self._set_chemical_display("chem1", self._get_chemical_display_weight("chem1", current_weight))
                self._set_chemical_display("chem2", self._get_chemical_display_weight("chem2", current_weight))
        except RuntimeError:
            # Qt object ถูก destroy แล้ว ให้ข้ามไป
            pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน segmentation fault
            pass
# END CHEMICAL WEIGHT HANDLING

# STATUS UPDATES AND LOADING CHECKS

    def update_status_port(self, connection_data):
        status = connection_data[0]
        device_type = connection_data[1] 
        if status:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Connection Error")
            msg_box.setText(f"ไม่สามารถเชื่อมต่อกับ {device_type} ได้\nโปรแกรมจะปิดลง")
            msg_box.setStandardButtons(QMessageBox.Ok)
            result = msg_box.exec_()
            if hasattr(self, 'main_window'):
                self.main_window.close()
            app = QApplication.instance()
            if app:
                app.quit()
                QTimer.singleShot(100, lambda: sys.exit(0))
        else:
            pass

    def check_loading_rock_and_sand(self, status):
        if status == True:
            self.rock_success = True
        else:
            self.rock_success = False
        if self.rock_and_sand_loading_success == True:
            self.loaded_rock_and_sand_successfully()
            self.rock_and_sand_loading_success = False
            self.rock_and_sand_success_start_main = True
            # ตรวจสอบว่าโหลดเสร็จทั้ง 4 ประเภท แล้วหรือยัง
            self._check_all_materials_loaded()
        else:
            pass

    def check_loading_cement_and_fyash(self, status):
        if status == True:
            self.cement_success = True
        else:
            self.cement_success = False
        if self.cement_and_fyash_loading_success == True:
            self.loaded_cement_and_fyash_successfully()
            self.cement_and_fyash_loading_success = False
            self.cement_and_fyash_success_start_main = True
            # ตรวจสอบว่าโหลดเสร็จทั้ง 4 ประเภท แล้วหรือยัง
            self._check_all_materials_loaded()
        else:
            pass
    
    def check_loading_water(self, status):
        if status == True:
            self.water_success = True
        else:
            self.water_success = False
        if self.water_loading_success == True:
            self.loaded_water_successfully()
            self.water_loading_success = False
            self.water_success_start_main = True
            # ตรวจสอบว่าโหลดเสร็จทั้ง 4 ประเภท แล้วหรือยัง
            self._check_all_materials_loaded()
        else:
            pass
    
    def check_loading_chemical(self, status):
        if status == True:
            self.chemical_success = True
        else:
            self.chemical_success = False
        if self.chemical_loading_success == True:
            self.loaded_chemical_successfully()
            self.chemical_loading_success = False
            self.chemical_success_start_main = True
            # ตรวจสอบว่าโหลดเสร็จทั้ง 4 ประเภท แล้วหรือยัง
            self._check_all_materials_loaded()
        else:
            pass
    
    def _check_all_materials_loaded(self):
        """ตรวจสอบว่าวัตถุดิบทั้ง 4 ประเภทโหลดเสร็จหมดแล้วหรือยัง"""
        # แสดงสถานะการโหลดปัจจุบัน
        print(f"🔍 Checking material loading status:")
        print(f"   Rock & Sand: {'✅' if self.rock_and_sand_success_start_main else '⏳'}")
        print(f"   Cement & Flyash: {'✅' if self.cement_and_fyash_success_start_main else '⏳'}")
        print(f"   Water: {'✅' if self.water_success_start_main else '⏳'}")
        print(f"   Chemical: {'✅' if self.chemical_success_start_main else '⏳'}")
        
        if (self.rock_and_sand_success_start_main and self.cement_and_fyash_success_start_main and self.water_success_start_main and self.chemical_success_start_main):
            # ถ้าโหลดเสร็จทุกอย่างแล้ว ให้ตั้ง flag บอกว่าพร้อมลำเลียงขึ้นไป
            self.next_queue_loaded_and_ready = True
            current_queue = self.current_queue_loaded + 1
            print(f"🎉 Queue {current_queue} is fully loaded and ready for transport!")
            print(f"   All materials loaded successfully ✅")
# END STATUS UPDATES AND LOADING CHECKS

# MIX START LOAD
    def mix_start_load(self):
        # print("\n🚀 === STARTING LOADING PROCESS ===")
        # ตรวจสอบจำนวนคิว ถ้ามี error จะ return ทันที
        self.start_button_load_enabled = True
        self.is_workflow_active = True  # เปิดใช้งาน workflow
        print("✅ Workflow activated")
        
        try:
            self.check_all_result_loaded()
            print(f"📊 Queue configuration validated:")
            print(f"   Total cubes to load: {self.get_all_loaded_cube}")
            print(f"   Total queue count: {self.total_queue_count}")
            print(f"   Queue multipliers: {self.queue_multipliers}")
        except ValueError as e:
            print(f"❌ Queue validation failed: {e}")
            # Error message ถูกแสดงใน check_all_result_loaded แล้ว
            self.is_workflow_active = False
            return
        
        # print("🔄 Resetting freeze values...")
        self.reset_freeze_values()
        self.reset_sum_data()
        # print("📊 Initializing counters...")
        # รีเซ็ต counter
        self.current_queue_transporting = 0
        self.completed_queue_count = 0  # รีเซ็ตจำนวนคิวที่ผสมเสร็จ
        self.next_queue_loaded_and_ready = False
        self.lock_target_display = True  # ล็อค Target UI ตั้งแต่เริ่มโหลด
        
        # print("🎯 Resetting UI displays...")
        # รีเซ็ตการแสดงผลจำนวนคิว - ห่อด้วย try-except
        try:
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.objectName()  # ตรวจสอบว่า object ยังใช้งานได้
                self.main_window.mix_result_mix_lineEdit.setText("0")
                self.main_window.mix_result_mix_success_lineEdit.setText("0")
        except (RuntimeError, AttributeError):
            pass
        
        # อ่านค่าจากฟอร์มและเก็บค่าต้นฉบับ
        result = self.main_window.get_data_formular_in_mix_form()
        if result is None:
            try:
                QMessageBox.warning(
                    self.main_window,
                    "ไม่สามารถเริ่มโหลดได้",
                    "กรุณาเลือกคิวงานก่อนเริ่มโหลด\n(ค่า Target ว่างเปล่า)"
                )
            except:
                pass
            self.lock_target_display = False
            self.is_workflow_active = False
            return
        
        self.original_rock1, self.original_sand, self.original_rock2, self.original_cement, self.original_fyash, self.original_water, self.original_chem1, self.original_chem2 = result
        
        # คำนวณค่าที่จะใช้โหลดตาม multiplier
        self.rock1 = int(float(self.original_rock1) * self.queue_multiplier)
        self.sand = int(float(self.original_sand) * self.queue_multiplier)
        self.rock2 = int(float(self.original_rock2) * self.queue_multiplier)
        self.cement = int(float(self.original_cement) * self.queue_multiplier)
        self.fyash = int(float(self.original_fyash) * self.queue_multiplier)
        self.water = int(float(self.original_water) * self.queue_multiplier)
        self.chem1 = float(self.original_chem1) * self.queue_multiplier
        self.chem2 = float(self.original_chem2) * self.queue_multiplier
        
        # ตั้งค่า display target สำหรับรอบแรก
        self.display_target_rock1 = self.rock1
        self.display_target_sand = self.sand
        self.display_target_rock2 = self.rock2
        self.display_target_cement = self.cement
        self.display_target_fyash = self.fyash
        self.display_target_water = self.water
        self.display_target_chem1 = self.chem1
        self.display_target_chem2 = self.chem2
        
        
        
        # อัพเดต Target ใน UI ทันที - ห่อด้วย try-except
        try:
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.objectName()  # ตรวจสอบว่า object ยังใช้งานได้
                self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
                self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
                self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
                self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
                self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
                self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
                self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
                self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
        except (RuntimeError, AttributeError):
            pass
        
        # เริ่ม target monitor
        # print("🎯 Starting target monitor...")
        self._start_target_monitor()
        self.reset_variable_for_cement_loaded()
        self.rock_and_sand_values = [int(self.rock1), int(self.sand), int(self.rock2)]
        self.cement_and_fyash_values = [int(self.cement), int(self.fyash)]
        self.water_value = int(self.water)
        self.chemical_values = [float(self.chem1), float(self.chem2)]
        
        print(f"📋 Material loading targets for queue 1:")
        print(f"   Rock & Sand: {self.rock_and_sand_values} kg")
        print(f"   Cement & Flyash: {self.cement_and_fyash_values} kg") 
        print(f"   Water: {self.water_value} kg")
        print(f"   Chemical: {self.chemical_values} kg")
        
        print("🔧 Starting loading threads...")
        time.sleep(1)
        self.is_loading_rock_and_sand_in_progress = True
        self.thread_rock_and_sand = Thread(target=self.load_rock_and_sand_sequence,args=(self.rock_and_sand_values,))
        self.thread_rock_and_sand.start()
        self.state_load_rock_and_sand = 1
        print("✅ Rock & Sand thread started")
        
        time.sleep(1)
        self.is_loading_cement_and_fyash_in_progress = True
        self.thread_cement_and_fyash = Thread(target=self.load_cement_and_fyash_sequence,args=(self.cement_and_fyash_values,))
        self.thread_cement_and_fyash.start()
        self.state_load_cement_and_fyash = 1
        print("✅ Cement & Flyash thread started")
        
        time.sleep(1)
        self.is_loading_water_in_progress = True
        self.thread_water = Thread(target=self.loading_water_sequence, args=(self.water_value,))
        self.thread_water.start()
        self.state_load_water = 1
        print("✅ Water thread started")
        
        time.sleep(1)
        self.is_loading_chemical_in_progress = True
        self.thread_chemical = Thread(target=self.loading_chemical_sequence, args=(self.chemical_values,))
        self.thread_chemical.start()
        self.state_load_chemical = 1
        print("✅ Chemical thread started")
        
        # print("Started loading sequence.")
        print("🏭 Starting main condition load controller...")
        self.main_condition_load_running = True
        self.state_main_condition_load = 0  # เริ่มที่ state 0
        self.thread_main_condition_load = Thread(target=self.main_condition_load)
        self.thread_main_condition_load.start()
        print("✅ Main condition load thread started")
        print("🚀 === LOADING PROCESS INITIALIZATION COMPLETE ===\n")
# END MIX START LOAD
        
        
    def check_all_result_loaded(self):
        # ตรวจสอบว่าช่องจำนวนคิวว่างหรือไม่
        queue_text = self.main_window.mix_result_load_lineEdit.text().strip()
        if not queue_text:
            QMessageBox.warning(
                self.main_window,
                "ไม่สามารถเริ่มโหลดได้",
                "กรุณาระบุจำนวนคิวที่ต้องการโหลด\n(ช่อง 'จำนวนคิว' ว่างเปล่า)"
            )
            raise ValueError("Queue count is empty")
        
        try:
            self.get_all_loaded_cube = float(queue_text)
        except ValueError:
            QMessageBox.warning(
                self.main_window,
                "ข้อมูลไม่ถูกต้อง",
                f"จำนวนคิวต้องเป็นตัวเลขเท่านั้น\nได้รับ: '{queue_text}'"
            )
            raise ValueError(f"Invalid queue count: {queue_text}")
        
        # ตรวจสอบว่าจำนวนคิวต้องมากกว่า 0
        if self.get_all_loaded_cube <= 0:
            QMessageBox.warning(
                self.main_window,
                "ข้อมูลไม่ถูกต้อง",
                "จำนวนคิวต้องมากกว่า 0"
            )
            raise ValueError(f"Queue count must be greater than 0, got: {self.get_all_loaded_cube}")
        
        # เก็บค่าสำหรับแต่ละรอบโหลด
        self.queue_multipliers = []
        
        if self.get_all_loaded_cube > 1.0:
            # ถ้ามากกว่า 1 คิว ต้องแยกเป็นรอบ
            full_queues = int(self.get_all_loaded_cube)  # จำนวนคิวเต็ม
            remaining = self.get_all_loaded_cube - full_queues  # เศษที่เหลือ
            
            if remaining > 0:
                # มีเศษ เช่น 1.5 คิว = 1 คิวเต็ม + 0.5 คิว
                # หรือ 3.5 คิว = 3 คิวเต็ม + 0.5 คิว
                self.total_queue_count = full_queues + 1
                
                # สร้าง list ของ multiplier สำหรับแต่ละรอบ
                for i in range(full_queues):
                    self.queue_multipliers.append(1.0)  # รอบที่เป็นคิวเต็ม
                self.queue_multipliers.append(remaining)  # รอบสุดท้ายเป็นเศษ
                
                # print(f"Loading mode: Multiple queues with fraction ({full_queues} full + {remaining} partial = {self.total_queue_count} rounds)")
                # print(f"Multipliers: {self.queue_multipliers}")
            else:
                # ไม่มีเศษ เช่น 2.0, 3.0, 4.0 คิว
                self.total_queue_count = full_queues
                for i in range(full_queues):
                    self.queue_multipliers.append(1.0)
                # print(f"Loading mode: Multiple full queues ({self.total_queue_count} queues)")
            
            self.queue_multiplier = self.queue_multipliers[0]  # ตั้งค่ารอบแรก
            
        elif self.get_all_loaded_cube == 1.0:
            # โหลดเต็ม 1 คิว
            self.total_queue_count = 1
            self.queue_multiplier = 1.0
            self.queue_multipliers = [1.0]
            # print("Loading mode: Full 1 queue")
            
        elif self.get_all_loaded_cube < 1.0:
            # ถ้าน้อยกว่า 1 คิว ให้ลดจำนวนวัตถุดิบตามสัดส่วน
            self.total_queue_count = 1
            self.queue_multiplier = self.get_all_loaded_cube
            self.queue_multipliers = [self.get_all_loaded_cube]
            # print(f"Loading mode: Partial queue ({self.queue_multiplier * 100}%)")
        
        self.current_queue_loaded = 0  # รีเซ็ตจำนวนคิวที่โหลดไปแล้ว
        
    
    def start_next_load_ready(self):
        """ฟังก์ชันสำหรับเริ่มโหลดคิวถัดไป"""
        self.current_queue_loaded += 1
        # print(f"Queue {self.current_queue_loaded} loaded. Total queues: {self.total_queue_count}")
        
        if self.current_queue_loaded < self.total_queue_count:
            # ยังมีคิวที่ต้องโหลดอีก ให้เริ่มโหลดทันที (ไม่ต้องรอกระบวนการผสมเสร็จ)
            self.ready_to_start_next_load = True
            # print(f"Starting to load next queue immediately ({self.current_queue_loaded + 1}/{self.total_queue_count})")
            self._start_loading_new_queue()
        else:
            # โหลดครบทุกคิวแล้ว
            self.ready_to_start_next_load = False
            # print("All queues loaded!")

    def _start_loading_new_queue(self):
        """เริ่มโหลดคิวใหม่โดยไม่รบกวนกระบวนการผสมที่กำลังทำงานอยู่"""
        next_queue_number = self.current_queue_loaded + 1
        print(f"\n🔄 === STARTING NEW QUEUE #{next_queue_number} ===")
        
        print("📋 Resetting success flags for new queue...")
        # รีเซ็ต success flags สำหรับการโหลดใหม่
        self.rock_and_sand_loading_success = False
        self.cement_and_fyash_loading_success = False
        self.water_loading_success = False
        self.chemical_loading_success = False
        self.rock_and_sand_success_start_main = False
        self.cement_and_fyash_success_start_main = False
        self.water_success_start_main = False
        self.chemical_success_start_main = False
        self.reset_variable_for_cement_loaded()
        print("🔄 Resetting freeze values for new queue...")
        # รีเซ็ต freeze values สำหรับการโหลดใหม่
        self.reset_freeze_values()
        
        
        # ดึง multiplier สำหรับรอบถัดไป
        next_queue_index = self.current_queue_loaded  # current_queue_loaded ถูกเพิ่มแล้วใน start_next_load_ready
        if next_queue_index < len(self.queue_multipliers):
            next_multiplier = self.queue_multipliers[next_queue_index]
            print(f"📊 Queue #{next_queue_number} configuration:")
            print(f"   Queue index: {next_queue_index}")
            print(f"   Multiplier: {next_multiplier}")
            
            # อัพเดต Target UI ตาม multiplier ของรอบนี้ (ต้องทำก่อนเริ่ม threads)
            print("🎯 Updating target display...")
            self._update_target_display(next_multiplier)
            
            # คำนวณค่าใหม่ตาม multiplier ของรอบนี้
            rock1 = int(float(self.original_rock1) * next_multiplier)
            sand = int(float(self.original_sand) * next_multiplier)
            rock2 = int(float(self.original_rock2) * next_multiplier)
            cement = int(float(self.original_cement) * next_multiplier)
            fyash = int(float(self.original_fyash) * next_multiplier)
            water = int(float(self.original_water) * next_multiplier)
            chem1 = float(self.original_chem1) * next_multiplier
            chem2 = float(self.original_chem2) * next_multiplier
            
        else:
            # ใช้ค่าเดิม (กรณี fallback)
            print("⚠️ Using fallback values (queue index out of range)")
            rock1 = self.rock1
            sand = self.sand
            rock2 = self.rock2
            cement = self.cement
            fyash = self.fyash
            water = self.water
            chem1 = self.chem1
            chem2 = self.chem2
        
        # เตรียมค่าสำหรับโหลด
        self.rock_and_sand_values = [int(rock1), int(sand), int(rock2)]
        self.cement_and_fyash_values = [int(cement), int(fyash)]
        self.water_value = int(water)
        self.chemical_values = [float(chem1), float(chem2)]
        
        print(f"📋 Material loading targets for queue #{next_queue_number}:")
        print(f"   Rock & Sand: {self.rock_and_sand_values} kg")
        print(f"   Cement & Flyash: {self.cement_and_fyash_values} kg")
        print(f"   Water: {self.water_value} kg")
        print(f"   Chemical: {self.chemical_values} kg")
        
        print("🔧 Starting loading threads for new queue...")
        # เริ่มโหลดในแต่ละ thread
        time.sleep(1)
        self.is_loading_rock_and_sand_in_progress = True
        self.thread_rock_and_sand = Thread(target=self.load_rock_and_sand_sequence, args=(self.rock_and_sand_values,))
        self.thread_rock_and_sand.start()
        self.state_load_rock_and_sand = 1
        print("✅ Rock & Sand thread started for new queue")
        
        time.sleep(1)
        self.is_loading_cement_and_fyash_in_progress = True
        self.thread_cement_and_fyash = Thread(target=self.load_cement_and_fyash_sequence, args=(self.cement_and_fyash_values,))
        self.thread_cement_and_fyash.start()
        self.state_load_cement_and_fyash = 1
        print("✅ Cement & Flyash thread started for new queue")
        
        time.sleep(1)
        self.is_loading_water_in_progress = True
        self.thread_water = Thread(target=self.loading_water_sequence, args=(self.water_value,))
        self.thread_water.start()
        self.state_load_water = 1
        print("✅ Water thread started for new queue")
        
        time.sleep(1)
        self.is_loading_chemical_in_progress = True
        self.thread_chemical = Thread(target=self.loading_chemical_sequence, args=(self.chemical_values,))
        self.thread_chemical.start()
        self.state_load_chemical = 1
        print("✅ Chemical thread started for new queue")
        
        self.ready_to_start_next_load = False
        print(f"🔄 === NEW QUEUE #{next_queue_number} LOADING STARTED ===\n")

    def _update_target_display(self, multiplier):
        """อัพเดตค่าเป้าหมาย (Target) ใน UI ตาม multiplier"""
        try:
            # ตรวจสอบว่า main_window ยังพร้อมใช้งาน
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                return
            
            # คำนวณค่า Target ใหม่ตาม multiplier
            self.display_target_rock1 = int(float(self.original_rock1) * multiplier)
            self.display_target_sand = int(float(self.original_sand) * multiplier)
            self.display_target_rock2 = int(float(self.original_rock2) * multiplier)
            self.display_target_cement = int(float(self.original_cement) * multiplier)
            self.display_target_fyash = int(float(self.original_fyash) * multiplier)
            self.display_target_water = int(float(self.original_water) * multiplier)
            self.display_target_chem1 = round(float(self.original_chem1) * multiplier, 1)
            self.display_target_chem2 = round(float(self.original_chem2) * multiplier, 1)
            
            # Lock การเปลี่ยนแปลง Target UI
            self.lock_target_display = True
            
            # อัพเดต UI หลายครั้งเพื่อให้แน่ใจว่าค่าถูกต้อง - ห่อด้วย try-except
            for _ in range(3):  # อัพเดต 3 ครั้งเพื่อความแน่ใจ
                try:
                    # ตรวจสอบอีกครั้งก่อนอัพเดท UI
                    self.main_window.objectName()
                    
                    self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
                    self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
                    self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
                    self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
                    self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
                    self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
                    self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
                    self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
                    time.sleep(0.1)  # หน่วงเวลาเล็กน้อย
                except (RuntimeError, AttributeError):
                    # Qt object ถูก destroy ระหว่างอัพเดท ให้หยุด
                    break
            
            # เริ่ม timer เพื่อตรวจสอบและรักษาค่า Target
            self._start_target_monitor()
            
        except (RuntimeError, AttributeError):
            # Qt object ถูก destroy แล้ว
            pass
        except Exception as e:
            print(f"⚠️ Error in _update_target_display: {e}")
    
    def _start_target_monitor(self):
        """เริ่ม timer เพื่อตรวจสอบและรักษาค่า Target UI (เรียกจาก main thread เท่านั้น)"""
        if not hasattr(self, 'target_monitor_timer'):
            self.target_monitor_timer = QTimer()
            self.target_monitor_timer.timeout.connect(self._maintain_target_display)
        
        if self.lock_target_display:
            self.target_monitor_timer.start(500)  # ตรวจสอบทุก 500ms
            # print("▶️ Target monitor started")
    
    @Slot()
    def _start_target_monitor_safe(self):
        """Slot สำหรับเริ่ม timer จาก worker thread อย่างปลอดภัย"""
        self._start_target_monitor()
    
    def _stop_target_monitor(self):
        """หยุด timer ตรวจสอบ Target UI (เรียกจาก main thread เท่านั้น)"""
        if hasattr(self, 'target_monitor_timer'):
            self.target_monitor_timer.stop()
            # print("⏹️ Target monitor stopped")
    
    @Slot()
    def _stop_target_monitor_safe(self):
        """Slot สำหรับหยุด timer จาก worker thread อย่างปลอดภัย"""
        self._stop_target_monitor()
    
    def _maintain_target_display(self):
        """รักษาค่า Target UI ให้คงที่ตามที่ตั้งไว้"""
        try:
            if not self.lock_target_display:
                self._stop_target_monitor()
                return
            
            # ตรวจสอบว่า main_window ยังพร้อมใช้งาน
            if not hasattr(self, 'main_window') or self.main_window is None:
                self._stop_target_monitor()
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                # Object ถูก destroy แล้ว
                self._stop_target_monitor()
                return
            
            # ตรวจสอบและแก้ไขค่าถ้ามีการเปลี่ยนแปลง - ห่อด้วย try-except แต่ละตัว
            try:
                current_rock1 = self.main_window.mix_wieght_target_rock_1_lineEdit.text()
                if current_rock1 != str(self.display_target_rock1):
                    self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_sand = self.main_window.mix_wieght_target_sand_lineEdit.text()
                if current_sand != str(self.display_target_sand):
                    self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_rock2 = self.main_window.mix_wieght_target_rock_2_lineEdit.text()
                if current_rock2 != str(self.display_target_rock2):
                    self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_cement = self.main_window.mix_wieght_target_cement_lineEdit.text()
                if current_cement != str(self.display_target_cement):
                    self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_fyash = self.main_window.mix_wieght_target_fyash_lineEdit.text()
                if current_fyash != str(self.display_target_fyash):
                    self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_water = self.main_window.mix_wieght_target_water_lineEdit.text()
                if current_water != str(self.display_target_water):
                    self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_chem1 = self.main_window.mix_wieght_target_chem_1_lineEdit.text()
                if current_chem1 != str(self.display_target_chem1):
                    self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
            except (RuntimeError, AttributeError):
                pass
            
            try:
                current_chem2 = self.main_window.mix_wieght_target_chem_2_lineEdit.text()
                if current_chem2 != str(self.display_target_chem2):
                    self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
            except (RuntimeError, AttributeError):
                pass
                
        except Exception as e:
            # หยุด timer ถ้าเกิด error
            self._stop_target_monitor()
            print(f"⚠️ Error in _maintain_target_display: {e}")
    
    def main_condition_load(self):
        while self.main_condition_load_running:
            try:
                # state 0
                if self.state_main_condition_load == 0:
                    if self.next_queue_loaded_and_ready:
                        self.next_queue_loaded_and_ready = False  # รีเซ็ต flag
                        self.current_queue_transporting += 1
                        self.state_main_condition_load = 1
                    else:
                        pass
                
                # state 1
                elif self.state_main_condition_load == 1:
                    self.update_sum_data()
                    current_queue_index = self.current_queue_transporting - 1
                    if current_queue_index < len(self.queue_multipliers):
                        current_mixing_amount = self.queue_multipliers[current_queue_index]
                        self.main_window.mix_result_mix_lineEdit.setText(str(current_mixing_amount))
                    self.status_message.emit("state 1")
                    self.plc_controller.mixer("start") #run mixer
                    self.status_message.emit("เริ่มผสมคิวที่ {}".format(self.current_queue_transporting))
                    self.status_message.emit("เปิดมอเตอร์ผสม")
                    time.sleep(7)
                    self.plc_controller.converyer_top("start") #run converyer top
                    self.status_message.emit("เปิดสายพานบน")
                    time.sleep(3)
                    self.plc_controller.converyer_midle("start")
                    self.status_message.emit("เปิดสายพานล่าง")
                    time.sleep(0.5)
                    self.state_main_condition_load = 2
                
                # state 2
                elif self.state_main_condition_load == 2:
                    time.sleep(5)
                    self.status_message.emit("เปิดปั้มน้ำยาขึ้น")
                    self.plc_controller.pump_chemical_up("start")
                    time.sleep(5)
                    self.status_message.emit("state 2")
                    self.plc_controller.vale_water("start")
                    self.status_message.emit("เปิดวาล์วน้ำ")
                    time.sleep(int(self.cement_release_time))
                    self.plc_controller.vale_cement_and_fyash("start")
                    self.status_message.emit("เปิดวาล์วปูนซีเมนต์และเถ้าลอย")
                    #time.sleep(4)
                    self.plc_controller.pump_chemical_up("stop")
                    #time.sleep(3)
                    self.state_main_condition_load = 3

                # state 3   
                elif self.state_main_condition_load == 3:
                    self.status_message.emit("state 3 - ติดตามน้ำหนัก Rock & Sand")
                    self.plc_controller.pump_chemical_up("start")
                    
                    if self.this_weight_to_stop_control <= self.offset_weight_to_stop_control and self.countdown_to_stop < 3:
                        self.countdown_to_stop += 1
                        time.sleep(1)
                        self.status_message.emit(f"น้ำหนักต่ำกว่า {self.offset_weight_to_stop_control} kg - นับถอยหลัง {self.countdown_to_stop}/3")
                        
                    elif self.countdown_to_stop >= 3:
                        if not hasattr(self, 'converyer_stop_timer_start'):
                            self.converyer_stop_timer_start = time.time()
                            self.status_message.emit(f"เริ่มหน่วงเวลา {self.converyer_time} วินาที ก่อนปิดสายพาน")
                        
                        elapsed_time = time.time() - self.converyer_stop_timer_start
                        remaining_time = max(0, int(self.converyer_time) - int(elapsed_time))
                        
                        if elapsed_time >= int(self.converyer_time):
                            self.status_message.emit("หมดเวลาหน่วง เริ่มปิดอุปกรณ์")
                            self.plc_controller.vale_cement_and_fyash("stop")
                            self.status_message.emit("ปิดวาล์วปูนซีเมนต์และเถ้าลอย")
                            time.sleep(2)
                            self.plc_controller.converyer_midle("stop")
                            self.status_message.emit("ปิดสายพานด้านล่าง")
                            time.sleep(2)
                            self.plc_controller.converyer_top("stop")
                            self.status_message.emit("ปิดสายพานด้านบน")
                            time.sleep(0.5)
                            self.plc_controller.vale_water("stop")
                            self.status_message.emit("ปิดวาล์วน้ำ")
                            time.sleep(0.5)
                            self.plc_controller.pump_chemical_up("stop")
                            time.sleep(5)
                            
                            del self.converyer_stop_timer_start
                            self.start_next_load_ready()
                            self.countdown_to_stop = 0
                            self.state_main_condition_load = 4
                        else:
                            if int(time.time()) % 2 == 0:
                                self.status_message.emit(f"รอเวลาหน่วง: เหลือ {remaining_time} วินาที")
                            
                    else:
                        if self.countdown_to_stop > 0:
                            self.status_message.emit("น้ำหนักกลับมาสูงกว่าเกณฑ์ - ยกเลิกการนับถอยหลัง")
                            self.countdown_to_stop = 0
                # state 4
                elif self.state_main_condition_load == 4:
                    self.status_message.emit("state 4")
                    for i in range(int(self.mixer_start_time)):
                        time.sleep(1)
                    
                    # open first step
                    self.plc_controller.vale_mixer_open("start")
                    time.sleep(1)
                    self.plc_controller.vale_mixer_open("start")
                    self.status_message.emit("เริ่มเปิดปาก first step")
                    time.sleep(1)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(0.5)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(5)

                    # open gate second step
                    self.plc_controller.vale_mixer_open("start")
                    time.sleep(1)
                    self.plc_controller.vale_mixer_open("start")
                    self.status_message.emit("เริ่มเปิดปากโม่ครึ่งนึง")
                    time.sleep(1)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(0.5)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(5)

                    # open gate third step
                    self.plc_controller.vale_mixer_open("start")
                    time.sleep(0.5)
                    self.plc_controller.vale_mixer_open("start")
                    self.status_message.emit("เปิดปากโม่จนสุด")
                    time.sleep(7)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(0.5)
                    self.plc_controller.off_coil_vale_mixer("start")
                    time.sleep(0.5)
                    self.plc_controller.pump_chemical_up("stop")
                    self.status_message.emit("ปิดปั้มน้ำยาเคมี")
                    self.close_vale_mixer_when_waiting = True
                    self.state_main_condition_load = 5
                    # self._update_database_after_loading()

                # state 5   
                elif self.state_main_condition_load == 5:
                    self.status_message.emit("state 5")
                    for i in range(18):
                        time.sleep(1)
                    has_more_queues = (self.next_queue_loaded_and_ready or self.current_queue_transporting < self.total_queue_count)
                    
                    if not has_more_queues:
                        self.status_message.emit("ไม่มีคิวเหลือแล้ว จบกระบวนการผสม กำลังปิดปากโม่")
                        self.plc_controller.vale_mixer_close("start")
                        time.sleep(0.5)
                        self.plc_controller.vale_mixer_close("start")
                        time.sleep(7)
                        self.plc_controller.off_coil_vale_mixer("start")
                        time.sleep(0.5)
                        self.plc_controller.off_coil_vale_mixer("start")
                        time.sleep(2)
                        self.plc_controller.mixer("stop")
                        self.state_main_condition_load = 8
                    else:
                        # print("More queues pending - keeping mixer running")
                        self.state_main_condition_load = 7
                    
                # state 6      
                elif self.state_main_condition_load == 6:
                    # State รอคิวถัดไปโหลดเสร็จ
                    self.status_message.emit("state 6")
                    if self.next_queue_loaded_and_ready:
                        self.status_message.emit("คิวถัดไปพร้อมสำหรับการลำเลียงแล้ว")
                        self.close_vale_mixer_when_waiting = True
                        # คิวถัดไปโหลดเสร็จแล้ว เริ่มลำเลียงได้
                        self.state_main_condition_load = 0  # กลับไป state 0 เพื่อเริ่มลำเลียงคิวถัดไป
                    else:
                        if self.close_vale_mixer_when_waiting == True:
                            self.status_message.emit("คิวถัดไปยังไม่พร้อม ปิดปากโม่ก่อน")
                            self.plc_controller.vale_mixer_close("start")
                            time.sleep(0.5)
                            self.plc_controller.vale_mixer_close("start")
                            time.sleep(7)
                            self.plc_controller.off_coil_vale_mixer("start")
                            time.sleep(0.5)
                            self.plc_controller.off_coil_vale_mixer("start")
                            self.close_vale_mixer_when_waiting = False
                        pass

                # state 7
                elif self.state_main_condition_load == 7:
                    # self._accumulate_batch_weights()
                    current_queue_index = self.current_queue_transporting - 1
                    if current_queue_index < len(self.queue_multipliers):
                        completed_amount = self.queue_multipliers[current_queue_index]
                        self.completed_queue_count += completed_amount
                        self._update_queue_display()
                    
                    if self.next_queue_loaded_and_ready:
                        self.close_vale_mixer_when_waiting = True
                        self.status_message.emit("คิวถัดไปพร้อมสำหรับการลำเลียงแล้ว")
                        if self.close_vale_mixer_when_waiting == True:
                            self.status_message.emit("ปิดปากโม่ก่อนเริ่มกระบวนการลำเลียงคิวถัดไป")
                            self.plc_controller.vale_mixer_close("start")
                            time.sleep(0.5)
                            self.plc_controller.vale_mixer_close("start")
                            time.sleep(7)
                            self.plc_controller.off_coil_vale_mixer("start")
                            time.sleep(0.5)
                            self.plc_controller.off_coil_vale_mixer("start")
                            self.close_vale_mixer_when_waiting = False
                            
                        self.state_main_condition_load = 0  # กลับไป state 0 เพื่อเริ่มลำเลียงคิวถัดไป
                    elif self.current_queue_transporting < self.total_queue_count:
                        # ยังมีคิวที่ต้องลำเลียงอีก แต่ยังโหลดไม่เสร็จ รอที่ state 6
                        self.close_vale_mixer_when_waiting = True
                        self.state_main_condition_load = 6
                        self.close_vale_mixer_when_waiting = True
                        self.status_message.emit("ยังมีคิวเหลือกำลังรอโหลด")

                # state 8 ===> close all process
                elif self.state_main_condition_load == 8:
                    self.lock_target_display = False  # ปลดล็อค Target
                    self.request_stop_target_monitor.emit()  # หยุด monitor จาก main thread
                    self.main_condition_load_running = False
                    self.state_main_condition_load = 0
                    self.start_button_load_enabled = False
                        
                    # print("💾 Starting database update...")
                    # อัพเดต database ด้วยน้ำหนักจริงที่โหลดได้
                    # self._update_database_after_loading()
                    
                    self.reset_variable_for_cement_loaded()
                    self._update_database_from_sum_data()
                    
                    
                    # print("🎨 Resetting device indicators...")
                    # รีเซ็ตสี label ทั้งหมดกลับเป็นสีเดิมเมื่อเสร็จสิ้นกระบวนการ
                    self._reset_all_device_indicators()
                        
                    # print("🔄 Resetting for new customer...")
                    # รีเซ็ตค่าทั้งหมดเพื่อเตรียมพร้อมสำหรับลูกค้ารายใหม่
                    self._reset_all_for_new_customer()
                    self.status_message.emit("เสร็จสิ้นกระบวนการ")
                    # print("✅ === COMPLETE PROCESS FINISHED ===\n")

                # out of state
                else:
                    print("Machine run out of state")
                        
            except Exception as e:
                print(f"Error in main condition load: {e}")
            time.sleep(1)

# ============================================================================================
# update sum data เพื่อเก็บไว้และนำไปรวมกันจนครบคิวที่สั่งแล้วค่อยบันทึกลง data base

    def update_sum_data(self): # function นี้ให้นำไปใส่ในส่วนที่โหลดวัสดุเสร็จและเริ่มกระบวนการเปิด mixer
        """ get ค่า defualt จาก UI เริ่มต้นก่อนโหลด"""
        self.current_sand_sum = int(self.main_window.mix_wieght_sum_sand_lineEdit.text())
        self.current_rock1_sum = int(self.main_window.mix_wieght_sum_rock_1_lineEdit.text())
        self.current_rock2_sum = int(self.main_window.mix_wieght_sum_rock_2_lineEdit.text())
        self.current_cement_sum = int(self.main_window.mix_wieght_sum_cement_lineEdit.text())
        self.current_fyash_sum = int(self.main_window.mix_wieght_sum_fyash_lineEdit.text())
        self.current_water_sum = int(self.main_window.mix_wieght_sum_water_lineEdit.text())
        self.current_chem1_sum = float(self.main_window.mix_wieght_sum_chem_1_lineEdit.text())
        self.current_chem2_sum = float(self.main_window.mix_wieght_sum_chem_2_lineEdit.text())
        
        """อัพเดตค่าน้ำหนักรวมที่โหลดได้จาก UI"""
        self.sand_sum_data = int(self.main_window.mix_wieght_Loaded_sand_lineEdit.text())
        self.sand_sum_data = self.sand_sum_data + self.current_sand_sum
        
        self.rock1_sum_data = int(self.main_window.mix_wieght_Loaded_rock_1_lineEdit.text())
        self.rock1_sum_data = self.rock1_sum_data + self.current_rock1_sum
        
        self.rock2_sum_data = int(self.main_window.mix_wieght_Loaded_rock_2_lineEdit.text())
        self.rock2_sum_data = self.rock2_sum_data + self.current_rock2_sum
        
        self.cement_sum_data = int(self.main_window.mix_wieght_Loaded_cement_lineEdit.text())
        self.cement_sum_data = self.cement_sum_data + self.current_cement_sum
        
        self.fyash_sum_data = int(self.main_window.mix_wieght_Loaded_fyash_lineEdit.text())
        self.fyash_sum_data = self.fyash_sum_data + self.current_fyash_sum
        
        self.water_sum_data = int(self.main_window.mix_wieght_Loaded_water_lineEdit.text())
        self.water_sum_data = self.water_sum_data + self.current_water_sum
        
        self.chem1_sum_data = float(self.main_window.mix_wieght_Loaded_chem_1_lineEdit.text())
        self.chem1_sum_data = self.chem1_sum_data + self.current_chem1_sum
        
        self.chem2_sum_data = float(self.main_window.mix_wieght_Loaded_chem_2_lineEdit.text())
        self.chem2_sum_data = self.chem2_sum_data + self.current_chem2_sum
        
    
        """อัพเดตจำนวนน้ำหนักผลรวมที่แสดงใน UI"""
        self.main_window.mix_wieght_sum_sand_lineEdit.setText(str(self.sand_sum_data))
        self.main_window.mix_wieght_sum_rock_1_lineEdit.setText(str(self.rock1_sum_data))
        self.main_window.mix_wieght_sum_rock_2_lineEdit.setText(str(self.rock2_sum_data))
        self.main_window.mix_wieght_sum_cement_lineEdit.setText(str(self.cement_sum_data))
        self.main_window.mix_wieght_sum_fyash_lineEdit.setText(str(self.fyash_sum_data))
        self.main_window.mix_wieght_sum_water_lineEdit.setText(str(self.water_sum_data))
        self.main_window.mix_wieght_sum_chem_1_lineEdit.setText(str(self.chem1_sum_data))
        self.main_window.mix_wieght_sum_chem_2_lineEdit.setText(str(self.chem2_sum_data))


# รีเซ็ตค่าน้ำหนักรวมใน UI เป็น 0 เมื่อเริ่มโหลดคิวใหม่ของลูกค้าใหม่หรือเมื่อโหลดเสร็จทั้งหมด
    def reset_sum_data(self): # function นี้ให้นำไปใส่ในกระบวนการตอนกดปุ่ม start เพื่อให้ set ค่าเริ่มต้นเป็น 0 สำหรับลูกค้าใหม่
        """รีเซ็ตค่าน้ำหนักรวมใน UI เป็น 0"""
        self.main_window.mix_wieght_sum_sand_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_rock_1_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_rock_2_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_cement_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_fyash_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_water_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_chem_1_lineEdit.setText("0")
        self.main_window.mix_wieght_sum_chem_2_lineEdit.setText("0")
        
# ============================================================================================

    def _update_queue_display(self):
        """อัพเดทจำนวนคิวที่แสดงใน UI อย่างปลอดภัย"""
        try:
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                return
            
            # อัพเดท UI
            try:
                self.main_window.mix_result_mix_success_lineEdit.setText(str(round(self.completed_queue_count, 1)))
                self.main_window.mix_result_mix_lineEdit.setText("0")
            except (RuntimeError, AttributeError):
                pass
        except Exception as e:
            # Suppress errors เพื่อป้องกัน crash
            pass
    
    def load_rock_and_sand_sequence(self,data_loaded):
        rock_1, sand_real, rock_2 = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_rock1 = rock_1
        original_sand = sand_real
        original_rock2 = rock_2
        
        # รอให้ weight signal อัพเดทและอ่านน้ำหนักปัจจุบัน (ที่ค้างอยู่)
        time.sleep(5)  # รอให้ Autoda อัพเดทค่า
        try:
            current_weight = int(self.main_window.mix_monitor_sand_lineEdit.text())
        except:
            try:
                current_weight = int(self.main_window.mix_monitor_rock_1_lineEdit.text())
            except:
                current_weight = 0
        
        # คำนวณ setpoint (หักลบ offset) - ลำดับ: Sand → Rock1 → Rock2
        # Sand: โหลดแค่ sand เฉย ๆ ไม่มีอะไรก่อนหน้า
        sand = int(sand_real) - int(self.sand_offset)
        
        # Rock1: โหลด rock1 + น้ำหนัก sand ที่โหลดไปแล้ว (ไม่ใช่สูตร sand!)
        rock_1 = int(rock_1) + sand - int(self.rock1_offset) + int(self.sand_offset)
        
        # Rock2: โหลด rock2 + น้ำหนัก rock1 ที่โหลดไปแล้ว (ซึ่งรวม sand อยู่แล้ว)
        rock_2 = int(rock_2) + rock_1 - int(self.rock2_offset) + int(self.rock1_offset)
        
        if current_weight > 0:
            sand += current_weight
            rock_1 += current_weight
            rock_2 += current_weight
        else:
            pass
        
        self.target_sand_total_weight = sand
        self.target_rock1_weight = rock_1
        self.target_rock2_total_weight = rock_2
        
        while self.is_loading_rock_and_sand_in_progress:
            if self.state_load_rock_and_sand == 0:
                pass
            
            # STATE 1: เริ่มโหลด Sand ก่อน
            elif self.state_load_rock_and_sand == 1:
                if original_sand <= 0:
                    self.is_sand_frozen = True
                    self.sand_frozen_weight = current_weight
                    self.sand_only_frozen = 0
                    self.state_load_rock_and_sand = 3
                else:
                    # print(f"sand  {sand}")
                    self.autoda_controller.write_set_point_rock_and_sand(sand)
                    time.sleep(0.5)           
                    self.plc_controller.start_vibrater_rock_and_sand("start")
                    time.sleep(0.5)
                    self.plc_controller.loading_sand("start")
                    self.state_load_rock_and_sand = 2
            
            # STATE 2: รอ Sand โหลดเสร็จ
            elif self.state_load_rock_and_sand == 2:
                if self.is_sand_frozen:
                    self.plc_controller.loading_sand("stop")
                    time.sleep(1)
                    self.plc_controller.start_vibrater_rock_and_sand("stop")
                    # เช็คว่า Rock1 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_rock1 > 0:
                        # print(f"Rock 1 3/8 {rock_1}")
                        self.autoda_controller.write_set_point_rock_and_sand(rock_1)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 3
            
            # STATE 3: เริ่มโหลด Rock1
            elif self.state_load_rock_and_sand == 3:
                self.plc_controller.loading_sand("stop")
                time.sleep(0.5)
                self.plc_controller.start_vibrater_rock_and_sand("stop")
                time.sleep(1)
                if original_rock1 <= 0:
                    self.is_rock1_frozen = True
                    self.rock1_frozen_weight = current_weight if current_weight > 0 else self.sand_frozen_weight
                    self.rock1_only_frozen = 0
                    # เช็คว่า Rock2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_rock2 > 0:
                        # print(f"in state 3 Rock 2 3/4 {rock_2}")
                        self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
                else:
                    self.plc_controller.loading_rock1("start")
                    self.state_load_rock_and_sand = 4
            
            # STATE 4: รอ Rock1 โหลดเสร็จ
            elif self.state_load_rock_and_sand == 4:
                if self.is_rock1_frozen:
                    self.plc_controller.loading_rock1("stop")
                    # เช็คว่า Rock2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_rock2 > 0:
                        # print(f"in state 4 Rock 2 3/4 {rock_2}")
                        self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
            
            # STATE 5: เริ่มโหลด Rock2
            elif self.state_load_rock_and_sand == 5:
                if original_rock2 <= 0:
                    self.is_rock2_frozen = True
                    self.rock2_frozen_weight = current_weight if current_weight > 0 else self.rock1_frozen_weight
                    self.rock2_only_frozen = 0
                    self.state_load_rock_and_sand = 0
                    self.rock_and_sand_loading_success = True
                    self.is_loading_rock_and_sand_in_progress = False
                else:
                    self.plc_controller.loading_rock2("start")
                    time.sleep(0.5)
                    self.plc_controller.loading_rock1("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_sand("stop")
                    self.state_load_rock_and_sand = 6
            
            # STATE 6: รอ Rock2 โหลดเสร็จ
            elif self.state_load_rock_and_sand == 6:
                # เมื่อ PLC ส่งสัญญาณว่าถึงน้ำหนักแล้ว ให้หยุดโหลดทันที
                if self.rock_success and not self.is_rock2_frozen:
                    # print("⚠️ Rock2 reached target, stopping loading immediately...")
                    self.plc_controller.loading_rock2("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_rock1("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_sand("stop")
                    # รอให้ freeze (จะ freeze ใน _check_freeze_conditions)
                
                # เมื่อ freeze เสร็จแล้ว จึงจบกระบวนการโหลด
                if self.is_rock2_frozen:
                    # print("✅ Rock2 loading complete!")
                    self.state_load_rock_and_sand = 0
                    self.rock_and_sand_loading_success = True
                    self.is_loading_rock_and_sand_in_progress = False
            # print(f"{self.state_load_rock_and_sand} loading state")

            time.sleep(0.1)
    
    def load_cement_and_fyash_sequence(self,data_loaded):
        cement, fyash = data_loaded
        original_cement = cement
        original_fyash = fyash
        
        # รอให้ weight signal อัพเดทและอ่านน้ำหนักปัจจุบัน (ที่ค้างอยู่)
        time.sleep(0.5)
        try:
            current_weight = int(self.main_window.mix_monitor_cement_lineEdit.text())
        except:
            current_weight = 0
        
        # print(f"🔍 Cement/Flyash initial weight: {current_weight} kg")
        
        # คำนวณ setpoint ตามลำดับใหม่: Flyash ก่อน แล้วค่อย Cement
        # Flyash โหลดก่อน (ไม่มีอะไรก่อนหน้า)
        fyash_setpoint = int(fyash) - int(self.fyash_offset)
        # Cement โหลดทีหลัง (บวก flyash เข้าไป)
        cement_setpoint = ((int(cement) + int(fyash)) - int(self.cement_offset)) + int(self.fyash_offset)
        
        if current_weight > 0:
            fyash_setpoint += current_weight
            cement_setpoint += current_weight
            # print(f"   Flyash setpoint: {fyash_setpoint} kg")
            # print(f"   Cement setpoint: {cement_setpoint} kg")
        
        self.target_fyash_weight = fyash_setpoint
        self.target_cement_total_weight = cement_setpoint
        
        while self.is_loading_cement_and_fyash_in_progress:
            if self.state_load_cement_and_fyash == 0:
                pass
                    
            # STATE 1: เริ่มโหลด Flyash ก่อน
            elif self.state_load_cement_and_fyash == 1:
                if original_fyash <= 0:
                    self.is_fyash_frozen = True
                    self.fyash_frozen_weight = current_weight
                    self.fyash_only_frozen = 0
                    # เช็คว่า Cement ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_cement > 0:
                        self.autoda_controller.write_set_point_cement_and_fyash(cement_setpoint)
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 3
                else:
                    # print(f"Setting Flyash setpoint: {fyash_setpoint}")
                    self.autoda_controller.write_set_point_cement_and_fyash(fyash_setpoint)
                    time.sleep(1)
                    self.plc_controller.loading_flyash("start")
                    self.state_load_cement_and_fyash = 2
                    
            # STATE 2: รอ Flyash โหลดเสร็จ
            elif self.state_load_cement_and_fyash == 2:
                if self.is_fyash_frozen:
                    self.plc_controller.loading_flyash("stop")
                    # เช็คว่า Cement ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_cement > 0:
                        self.autoda_controller.write_set_point_cement_and_fyash(cement_setpoint)
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 3
            
            # STATE 3: เริ่มโหลด Cement
            elif self.state_load_cement_and_fyash == 3:
                self.plc_controller.loading_flyash("stop")
                time.sleep(1)
                self.retry_count = 0  # ตัวนับสำหรับการเติมปูนซ้ำ
                if original_cement <= 0:
                    self.is_cement_frozen = True
                    self.cement_frozen_weight = current_weight if current_weight > 0 else self.fyash_frozen_weight
                    self.state_load_cement_and_fyash = 0
                    self.cement_and_fyash_loading_success = True
                    self.is_loading_cement_and_fyash_in_progress = False
                else:
                    # print(f"Setting Cement setpoint: {cement_setpoint}")
                    # self.plc_controller.loading_cement("start")
                    # self.state_load_cement_and_fyash = 4
                    self.cement_start_time = time.time()
                    self.cement_start_weight = int(self.main_window.mix_monitor_cement_lineEdit.text()) 
                    self.plc_controller.loading_cement("start")
                    self.state_load_cement_and_fyash = 100

            elif self.state_load_cement_and_fyash == 100:
                self.cement_follow_weight = int(self.main_window.mix_monitor_cement_lineEdit.text()) 
                cutoff_offset = 20  # กำหนด offset สำหรับการหยุดโหลดรอบแรก
                if self.cement_follow_weight >= self.target_cement_total_weight - cutoff_offset:
                    self.plc_controller.loading_cement("stop")
                    time.sleep(3)
                    self.end_cement_time = time.time()
                    self.cement_follow_weight = int(self.main_window.mix_monitor_cement_lineEdit.text())
                    self.loading_duration = self.end_cement_time - self.cement_start_time
                    self.status_message.emit(f"โหลดปูนซีเมนต์รอบแรกเสร็จสิ้น ใช้เวลา {self.loading_duration:.2f} วินาที")
                    self.state_load_cement_and_fyash = 101
                else:
                    self.status_message.emit("กำลังโหลดปูนซีเมนต์...")

            elif self.state_load_cement_and_fyash == 101:
                try:
                    self.now_weight = int(self.main_window.mix_monitor_cement_lineEdit.text())
                except:
                    self.now_weight = 0

                self.remain = self.target_cement_total_weight - self.now_weight
                # 3. คำนวณอัตราการโหลดต่อวินาทีจากรอบแรก
                # self.first_weight_loaded = self.cement_follow_weight  # น้ำหนักที่ได้รอบแรก
                self.first_weight_loaded = self.cement_follow_weight - self.cement_start_weight
                
                self.time_loaded_duration = self.end_cement_time - self.cement_start_time
                if self.time_loaded_duration > 1.0 and self.first_weight_loaded > 5:
                    self.rate_loaded = self.first_weight_loaded / self.time_loaded_duration if self.time_loaded_duration > 0 else 0
                else:
                    self.rate_loaded = 0
                # 4. คำนวณเวลาที่ต้องเติมเพิ่ม
                self.extra_time = self.remain / self.rate_loaded if self.rate_loaded > 0 else 0
                
                # 5. เติมต่อถ้ายังขาด
                if self.rate_loaded == 0 or self.extra_time <= 0:
                    self.status_message.emit("ไม่สามารถคำนวณอัตราการโหลดหรือเวลาที่ต้องเติมเพิ่มได้ ข้ามไปขั้นตอนถัดไป")
                    self.state_load_cement_and_fyash = 102
                    
                elif self.remain > 0 and self.extra_time > 0:
                    self.safe_fill_time = min(self.extra_time, 5)
                    self.status_message.emit(f"เติมปูนซีเมนต์เพิ่มอีก {self.remain:.1f} กก. (ประมาณ {self.extra_time:.2f} วินาที)")
                    self.plc_controller.loading_cement("start")
                    time.sleep(self.safe_fill_time)
                    self.plc_controller.loading_cement("stop")
                    self.status_message.emit("เติมปูนซีเมนต์ครบตามเป้าหมายแล้ว")
                    self.state_load_cement_and_fyash = 102
                else:
                    self.status_message.emit("ค่า remain หรือ extra_time ไม่ถูกต้อง ไม่เติมปูนซีเมนต์เพิ่ม")
                    self.state_load_cement_and_fyash = 4

            elif self.state_load_cement_and_fyash == 102:
                time.sleep(2) # รอให้น้ำหนักนิ่ง
                try:
                    self.tried_weight = int(self.main_window.mix_monitor_cement_lineEdit.text())
                    if self.tried_weight == 0:
                        self.state_load_cement_and_fyash = 4
                except ValueError:
                    self.tried_weight = 0
                    self.state_load_cement_and_fyash = 4

                self.target = self.target_cement_total_weight
                self.diff = self.tried_weight - self.target

                if abs(self.diff) <= 2:
                    self.status_message.emit(f"OK: น้ำหนักตรงเป้า (Diff: {self.diff})")
                    self.state_load_cement_and_fyash = 4
                    self.retry_count = 0  # รีเซ็ตตัวนับ
                elif self.tried_weight > (self.target + 2):
                    self.status_message.emit(f"Error: น้ำหนักเกิน! (Got: {self.tried_weight}) หยุดทันที")
                    self.state_load_cement_and_fyash = 4
                else:
                    if self.retry_count > 10:  # ยอมให้เติมทีละนิดได้ไม่เกิน 10 ครั้ง
                        self.status_message.emit("Critical Error: เติมปูนหลายรอบแล้วน้ำหนักไม่ถึงเป้า (เช็คปูนหมด/เซนเซอร์เสีย)")
                        self.state_load_cement_and_fyash = 4  # สั่งจบการทำงาน
                    else:
                        self.status_message.emit(f"Filling: ขาด {abs(self.diff)} กก. (รอบที่ {self.retry_count})")
                        self.state_load_cement_and_fyash = 103
                        self.retry_count += 1  # บวกตัวนับเพิ่ม
            
            elif self.state_load_cement_and_fyash == 103:
                self.plc_controller.loading_cement("start")
                time.sleep(1)
                self.plc_controller.loading_cement("stop")
                self.state_load_cement_and_fyash = 102
                
            # STATE 4: Cement โหลดเสร็จ
            elif self.state_load_cement_and_fyash == 4:
                if self.is_cement_frozen:
                    self.plc_controller.loading_cement("stop")
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 0
                    self.cement_and_fyash_loading_success = True
                    self.is_loading_cement_and_fyash_in_progress = False
                    
            time.sleep(0.1)

    def loading_water_sequence(self,data_loaded):
        water = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_water = water
        
        # รอให้ weight signal อัพเดทและอ่านน้ำหนักปัจจุบัน
        time.sleep(0.5)
        try:
            current_weight = int(self.main_window.mix_monitor_water_lineEdit.text())
        except:
            current_weight = 0
        # คำนวณ setpoint (หักลบ offset)
        water = int(water) - int(self.water_offset)
        
        if current_weight > 0:
            water += current_weight
        
        self.target_water_weight = water
        
        while self.is_loading_water_in_progress:
            if self.state_load_water == 0:
                pass
            elif self.state_load_water == 1:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_water <= 0:
                    self.is_water_frozen = True
                    self.water_frozen_weight = current_weight
                    self.state_load_water = 0
                    self.water_loading_success = True
                    self.is_loading_water_in_progress = False
                else:
                    print(water)
                    self.autoda_controller.write_set_point_water(water)
                    time.sleep(0.5)
                    self.plc_controller.loading_water("start")
                    time.sleep(0.5)
                    self.state_load_water = 2
            elif self.state_load_water == 2:
                if self.is_water_frozen:
                    self.plc_controller.loading_water("stop")
                    time.sleep(0.5)
                    self.state_load_water = 3
            elif self.state_load_water == 3:
                    self.state_load_water = 0
                    self.water_loading_success = True
                    self.is_loading_water_in_progress = False
            time.sleep(0.1)

    def loading_chemical_sequence(self, data_loaded):
        chem1, chem2 = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_chem1 = float(chem1)
        original_chem2 = float(chem2)
        
        # รอให้ weight signal อัพเดทและอ่านน้ำหนักปัจจุบัน
        time.sleep(0.5)
        try:
            current_weight = float(self.main_window.mix_monitor_chem_1_lineEdit.text())
        except:
            current_weight = 0.0
        
        print(f"🔍 Chemical initial weight: {current_weight} kg")
        
        # คำนวณ setpoint (หักลบ offset)
        chem1 = float(chem1) - float(self.chem1_offset)
        chem2 = ((float(chem2)+float(chem1)) - float(self.chem2_offset)) + float(self.chem1_offset)
        chem1 = round(chem1, 1)
        chem2 = round(chem2, 1)
        
        if current_weight > 0:
            chem1 += current_weight
            chem2 += current_weight
            chem1 = round(chem1, 1)
            chem2 = round(chem2, 1)
            print(f"✅ Chemical setpoints:")
            print(f"   Chem1: {chem1} kg")
            print(f"   Chem2: {chem2} kg")
            
        if original_chem1 <= 0 and original_chem2 <= 0:
            self.is_chem1_frozen = True
            self.is_chem2_frozen = True
            self.chem1_frozen_weight = current_weight
            self.chem2_frozen_weight = current_weight
            self.chem2_only_frozen = 0  # ทั้งคู่ถูก skip
            self.chemical_loading_success = True
            self.is_loading_chemical_in_progress = False
            return
        
        self.target_chem1_weight = chem1
        self.target_chem2_total_weight = chem2
        while self.is_loading_chemical_in_progress:
            if self.state_load_chemical == 0:
                pass
            elif self.state_load_chemical == 1:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_chem1 <= 0:
                    self.is_chem1_frozen = True
                    self.chem1_frozen_weight = current_weight
                    self.state_load_chemical = 3
                else:
                    self.autoda_controller.write_set_point_chemical(chem1)
                    time.sleep(0.5)
                    self.plc_controller.loading_chemical_1("start")
                    time.sleep(0.5)
                    self.state_load_chemical = 2

            elif self.state_load_chemical == 2:
                if self.is_chem1_frozen:
                    self.plc_controller.loading_chemical_1("stop")
                    # เช็คว่า Chem2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_chem2 > 0:
                        self.autoda_controller.write_set_point_chemical(chem2)
                    time.sleep(0.5)
                    self.state_load_chemical = 3

            elif self.state_load_chemical == 3:
                self.plc_controller.loading_chemical_1("stop")
                time.sleep(0.5)
                if original_chem2 <= 0:
                    self.is_chem2_frozen = True
                    self.chem2_frozen_weight = current_weight if current_weight > 0 else self.chem1_frozen_weight
                    self.chem2_only_frozen = 0  # Chem2 ถูก skip
                    self.state_load_chemical = 0
                    self.chemical_loading_success = True
                    self.is_loading_chemical_in_progress = False
                else:
                    self.autoda_controller.write_set_point_chemical(chem2)
                    time.sleep(0.5)
                    self.plc_controller.loading_chemical_2("start")
                    self.state_load_chemical = 4

            elif self.state_load_chemical == 4:
                if self.is_chem2_frozen:
                    self.plc_controller.loading_chemical_2("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_chemical_1("stop")
                    self.state_load_chemical = 0
                    self.chemical_loading_success = True
                    self.is_loading_chemical_in_progress = False
            time.sleep(0.1)

    def loaded_rock_and_sand_successfully(self):
        if self.thread_rock_and_sand and self.thread_rock_and_sand.is_alive():
            self.thread_rock_and_sand.join()

    def loaded_cement_and_fyash_successfully(self):
        if self.thread_cement_and_fyash and self.thread_cement_and_fyash.is_alive():
            self.thread_cement_and_fyash.join()

    def loaded_water_successfully(self):
        if self.thread_water and self.thread_water.is_alive():
            self.thread_water.join()

    def loaded_chemical_successfully(self):
        if self.thread_chemical and self.thread_chemical.is_alive():
            self.thread_chemical.join()

    def mix_cancel_load(self):
        print("Cancelling load operation...")
        self.start_button_load_enabled = False
        self.is_workflow_active = False  # ปิด workflow
        self.reset_freeze_values()
        self.lock_target_display = False  # ปลดล็อค Target UI เมื่อยกเลิก
        self._stop_target_monitor()  # หยุด monitor
        self.reset_variable_for_cement_loaded()
        # รีเซ็ตสี label ทั้งหมดกลับเป็นสีเดิม
        self._reset_all_device_indicators()
        
        # หยุด threads
        if self.is_loading_rock_and_sand_in_progress:
            self.is_loading_rock_and_sand_in_progress = False
            if hasattr(self, 'thread_rock_and_sand') and self.thread_rock_and_sand.is_alive():
                self.thread_rock_and_sand.join()
        if self.is_loading_cement_and_fyash_in_progress:
            self.is_loading_cement_and_fyash_in_progress = False
            if hasattr(self, 'thread_cement_and_fyash') and self.thread_cement_and_fyash.is_alive():
                self.thread_cement_and_fyash.join()
        if self.is_loading_water_in_progress:
            self.is_loading_water_in_progress = False
            if hasattr(self, 'thread_water') and self.thread_water.is_alive():
                self.thread_water.join()
        if self.is_loading_chemical_in_progress:
            self.is_loading_chemical_in_progress = False
            if hasattr(self, 'thread_chemical') and self.thread_chemical.is_alive():
                self.thread_chemical.join()
        if hasattr(self, 'thread_main_condition_load') and self.thread_main_condition_load.is_alive():
            self.main_condition_load_running = False
            self.thread_main_condition_load.join()
        

    def Show_main(self):
        self.main_window.Show()

    def _reset_all_device_indicators(self):
        """รีเซ็ตสี label ของอุปกรณ์และวัตถุดิบทั้งหมดกลับเป็นสีเดิม"""
        try:
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                return
            
            inactive_color = "border: 2px solid; border-radius: 10px;"
            
            # รายการอุปกรณ์และวัตถุดิบทั้งหมด
            all_devices = [
                # วัตถุดิบ
                "rock1", "sand", "rock2", "cement", "flyash", "water", "chemical1", "chemical2",
                # อุปกรณ์
                "mixer", "conveyor_middle", "conveyor_top", "valve_cement_flyash", 
                "valve_water", "pump_chemical", "valve_mixer"
            ]
            
            # ส่ง signal เพื่อรีเซ็ตสีทั้งหมด
            for device in all_devices:
                self.update_device_status_indicator(device, False)
                
            print("✅ Reset all device indicators to inactive state")
            
        except Exception as e:
            print(f"Error resetting device indicators: {e}")

    def reset_freeze_values(self):
        """Reset all freeze values for all materials"""
        # Rock and Sand
        self.rock1_frozen_weight = 0
        self.sand_frozen_weight = 0
        self.rock2_frozen_weight = 0
        self.sand_only_frozen = 0
        self.rock2_only_frozen = 0
        self.is_rock1_frozen = False
        self.is_sand_frozen = False
        self.is_rock2_frozen = False
        # Reset stabilization states - Rock and Sand
        self.rock1_stabilizing = False
        self.sand_stabilizing = False
        self.rock2_stabilizing = False
        self.rock1_stabilize_start_time = 0
        self.sand_stabilize_start_time = 0
        self.rock2_stabilize_start_time = 0
        # Cement and Fyash
        self.cement_frozen_weight = 0
        self.fyash_frozen_weight = 0
        self.fyash_only_frozen = 0
        self.is_cement_frozen = False
        self.is_fyash_frozen = False
        self.cement_stabilizing = False
        self.fyash_stabilizing = False
        self.cement_stabilize_start_time = 0
        self.fyash_stabilize_start_time = 0
        # Water
        self.water_frozen_weight = 0
        self.is_water_frozen = False
        self.water_stabilizing = False
        self.water_stabilize_start_time = 0
        # Chemical
        self.chem1_frozen_weight = 0
        self.chem2_frozen_weight = 0
        self.chem2_only_frozen = 0
        self.is_chem1_frozen = False
        self.is_chem2_frozen = False
        self.chem1_stabilizing = False
        self.chem2_stabilizing = False
        self.chem1_stabilize_start_time = 0
        self.chem2_stabilize_start_time = 0
    
    def get_freeze_status(self):
        return {
            'rock1': {'frozen': self.is_rock1_frozen, 'weight_total': self.rock1_frozen_weight, 'weight_only': self.rock1_frozen_weight},
            'sand': {'frozen': self.is_sand_frozen, 'weight_total': self.sand_frozen_weight, 'weight_only': getattr(self, 'sand_only_frozen', 0)},
            'rock2': {'frozen': self.is_rock2_frozen, 'weight_total': self.rock2_frozen_weight, 'weight_only': getattr(self, 'rock2_only_frozen', 0)},
            'current_state': self.state_load_rock_and_sand
        }
    
    
    def _update_database_from_sum_data(self):
        """อัพเดตฐานข้อมูลด้วยน้ำหนักรวมจาก sum_lineEdit หลังจากเสร็จสิ้นกระบวนการ"""
        try:
            # print("\n💾 === DATABASE UPDATE FROM SUM DATA STARTED ===")
            order_id = self.load_work_queue.get_current_order_id()
            # print(f"   Order ID: {order_id}")
            if not order_id:
                # print("❌ No order ID found - cannot update database")
                return
            # ตรวจสอบว่า main_window ยังมีอยู่
            if not hasattr(self, 'main_window') or self.main_window is None:
                # print("❌ main_window not available - cannot read sum data")
                return
            
            try:
                # อ่านค่าจาก sum_lineEdit fields
                sand_total = int(self.main_window.mix_wieght_sum_sand_lineEdit.text() or "0")
                rock1_total = int(self.main_window.mix_wieght_sum_rock_1_lineEdit.text() or "0")
                rock2_total = int(self.main_window.mix_wieght_sum_rock_2_lineEdit.text() or "0")
                cement_total = int(self.main_window.mix_wieght_sum_cement_lineEdit.text() or "0")
                flyash_total = int(self.main_window.mix_wieght_sum_fyash_lineEdit.text() or "0")
                water_total = int(self.main_window.mix_wieght_sum_water_lineEdit.text() or "0")
                chem1_total = float(self.main_window.mix_wieght_sum_chem_1_lineEdit.text() or "0")
                chem2_total = float(self.main_window.mix_wieght_sum_chem_2_lineEdit.text() or "0")
            except (ValueError, RuntimeError, AttributeError) as e:
                print(f"❌ Error reading sum data from UI: {e}")
                return
            
            # แสดงข้อมูลก่อนบันทึก
            print(f"   Final sum weights to be saved:")
            print(f"   Total cubes loaded: {self.get_all_loaded_cube}")
            print(f"   Total queues completed: {self.completed_queue_count}")
            print(f"   Sand: {sand_total} kg")
            print(f"   Rock1: {rock1_total} kg")
            print(f"   Rock2: {rock2_total} kg")
            print(f"   Cement: {cement_total} kg")
            print(f"   Flyash: {flyash_total} kg")
            print(f"   Water: {water_total} kg")
            print(f"   Chem1: {chem1_total} kg")
            print(f"   Chem2: {chem2_total} kg")
            
            # สร้าง mixer object จากข้อมูล sum
            current_mixer = self.load_work_queue.current_mixer
            current_mixer.sand_total_weight = sand_total
            current_mixer.rock1_total_weight = rock1_total
            current_mixer.rock2_total_weight = rock2_total
            current_mixer.cement_total_weight = cement_total
            current_mixer.fly_ash_total_weight = flyash_total
            current_mixer.water_total_weight = water_total
            current_mixer.chem1_total_weight = chem1_total
            current_mixer.chem2_total_weight = chem2_total
            
            if not hasattr(self.load_work_queue, 'order_inserter'):
                print("No order_inserter found - cannot update database")
                return
            
            print("⏳ Saving sum data to database...")
            success = self.load_work_queue.order_inserter.update_complete(order_id, current_mixer)

            if success:
                print("✅ Database updated successfully with sum data!")
                print(f"   Order {order_id} marked as complete")
            else:
                print("❌ Database update failed!")
            
            print("💾 === DATABASE UPDATE FROM SUM DATA COMPLETED ===\n")
            
        except Exception as e:
            print(f"❌ Error updating database from sum data: {e}")
            import traceback
            traceback.print_exc()


    def _accumulate_batch_weights(self):
        """สะสมน้ำหนักจริงที่โหลดได้จาก batch ปัจจุบันเข้าไปใน TempMixer"""
        try:
            current_mixer = self.load_work_queue.current_mixer
            if not current_mixer:
                print("No current mixer found for weight accumulation")
                return
            
            # แสดงข้อมูลก่อนเริ่มสะสม
            current_queue_index = self.current_queue_transporting - 1
            multiplier = self.queue_multipliers[current_queue_index] if current_queue_index < len(self.queue_multipliers) else 1.0
            print(f"\n📊 === ACCUMULATING BATCH #{self.current_queue_transporting} ===")
            print(f"   Queue multiplier: {multiplier}")
            print(f"   Progress: {self.current_queue_transporting}/{self.total_queue_count} queues")
            
            # Sand (only sand, โหลดก่อนในลำดับใหม่)
            sand_this_batch = getattr(self, 'sand_only_frozen', 0)
            old_sand_total = current_mixer.sand_total_weight
            current_mixer.sand_total_weight += sand_this_batch
            
            # Rock1 (only rock1, โหลดที่ 2)
            rock1_this_batch = getattr(self, 'rock1_only_frozen', 0)
            old_rock1_total = current_mixer.rock1_total_weight
            current_mixer.rock1_total_weight += rock1_this_batch
            
            # Rock2 (only rock2, โหลดสุดท้าย)
            rock2_this_batch = getattr(self, 'rock2_only_frozen', 0)
            old_rock2_total = current_mixer.rock2_total_weight
            current_mixer.rock2_total_weight += rock2_this_batch
            
            # Flyash (โหลดก่อน Cement ในลำดับใหม่)
            flyash_this_batch = getattr(self, 'fyash_frozen_weight', 0)
            old_flyash_total = current_mixer.fly_ash_total_weight
            current_mixer.fly_ash_total_weight += flyash_this_batch
            
            # Cement (โหลดทีหลัง - ต้องหัก flyash ออก)
            cement_frozen_total = getattr(self, 'cement_frozen_weight', 0)
            fyash_frozen = getattr(self, 'fyash_frozen_weight', 0)
            cement_this_batch = max(0, cement_frozen_total - fyash_frozen if getattr(self, 'is_fyash_frozen', False) else cement_frozen_total)
            old_cement_total = current_mixer.cement_total_weight
            current_mixer.cement_total_weight += cement_this_batch
            
            # Water
            water_this_batch = getattr(self, 'water_frozen_weight', 0)
            old_water_total = current_mixer.water_total_weight
            current_mixer.water_total_weight += water_this_batch
            
            # Chem1
            chem1_this_batch = getattr(self, 'chem1_frozen_weight', 0)
            old_chem1_total = current_mixer.chem1_total_weight
            current_mixer.chem1_total_weight += chem1_this_batch
            
            # Chem2 (only chem2, not total)
            chem2_this_batch = getattr(self, 'chem2_only_frozen', 0)
            old_chem2_total = current_mixer.chem2_total_weight
            current_mixer.chem2_total_weight += chem2_this_batch
            
            print("=" * 70)
            print(f"   Batch #{self.current_queue_transporting} weights accumulated:")
            print(f"   Sand: {old_sand_total} + {sand_this_batch} → {current_mixer.sand_total_weight} kg")
            print(f"   Rock1: {old_rock1_total} + {rock1_this_batch} → {current_mixer.rock1_total_weight} kg")
            print(f"   Rock2: {old_rock2_total} + {rock2_this_batch} → {current_mixer.rock2_total_weight} kg")
            print(f"   Cement: {old_cement_total} + {cement_this_batch} → {current_mixer.cement_total_weight} kg")
            print(f"   Flyash: {old_flyash_total} + {flyash_this_batch} → {current_mixer.fly_ash_total_weight} kg")
            print(f"   Water: {old_water_total} + {water_this_batch} → {current_mixer.water_total_weight} kg")
            print(f"   Chem1: {old_chem1_total} + {chem1_this_batch} → {current_mixer.chem1_total_weight} kg")
            print(f"   Chem2: {old_chem2_total} + {chem2_this_batch} → {current_mixer.chem2_total_weight} kg")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ Error accumulating batch weights: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_database_after_loading(self):
        """อัพเดตฐานข้อมูลด้วยน้ำหนักจริงที่โหลดได้หลังจากเสร็จสิ้นกระบวนการ"""
        try:
            print("\n💾 === DATABASE UPDATE STARTED ===")
            
            order_id = self.load_work_queue.get_current_order_id()
            print(f"   Order ID: {order_id}")
            
            if not order_id:
                print("❌ No order ID found - cannot update database")
                return
                
            current_mixer = self.load_work_queue.current_mixer
            
            if not current_mixer:
                print("❌ No current mixer found - cannot update database")
                return
            
            # แสดงข้อมูลก่อนบันทึก
            print(f"   Final accumulated weights to be saved:")
            print(f"   Total cubes loaded: {self.get_all_loaded_cube}")
            print(f"   Total queues completed: {self.completed_queue_count}")
            print(f"   Sand: {current_mixer.sand_total_weight} kg")
            print(f"   Rock1: {current_mixer.rock1_total_weight} kg") 
            print(f"   Rock2: {current_mixer.rock2_total_weight} kg")
            print(f"   Cement: {current_mixer.cement_total_weight} kg")
            print(f"   Flyash: {current_mixer.fly_ash_total_weight} kg")
            print(f"   Water: {current_mixer.water_total_weight} kg")
            print(f"   Chem1: {current_mixer.chem1_total_weight} kg")
            print(f"   Chem2: {current_mixer.chem2_total_weight} kg")
            
            if not hasattr(self.load_work_queue, 'order_inserter'):
                print("No order_inserter found - cannot update database")
                return
                
            print("⏳ Saving to database...")
            success = self.load_work_queue.order_inserter.update_complete(order_id, current_mixer)
            
            if success:
                print("✅ Database updated successfully!")
                print(f"   Order {order_id} marked as complete")
            else:
                print("❌ Database update failed!")
                
            print("💾 === DATABASE UPDATE COMPLETED ===\n")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            import traceback
            traceback.print_exc()
    
    def _reset_all_for_new_customer(self):
        """Reset ค่าทั้งหมดเพื่อเตรียมพร้อมสำหรับลูกค้าใหม่ - Thread Safe"""
        print("🔄 Starting reset for new customer...")
        
        # ตรวจสอบว่าถูกเรียกจาก main_condition_load thread หรือไม่
        import threading
        current_thread = threading.current_thread()
        is_main_condition_thread = (hasattr(self, 'thread_main_condition_load') and 
                                    self.thread_main_condition_load and 
                                    current_thread == self.thread_main_condition_load)
        
        if is_main_condition_thread:
            print("   ℹ️ Called from main_condition_load thread - will not join self")
        
        # 🚨 CRITICAL: ปิด workflow ก่อนอื่นหมดเพื่อหยุด ALL signals
        self.is_workflow_active = False
        self.is_tab_switching = True  # บล็อกการอัพเดท UI ทันที
        print("   ✓ Workflow deactivated and UI updates blocked")
        
        # 0. หยุด Threads ทั้งหมดก่อนเป็นอันดับแรก
        self.is_loading_rock_and_sand_in_progress = False
        self.is_loading_cement_and_fyash_in_progress = False
        self.is_loading_water_in_progress = False
        self.is_loading_chemical_in_progress = False
        self.main_condition_load_running = False
        print("   ✓ All loading flags set to False")
        
        # รอให้ Threads หยุดสนิท พร้อม join threads (ยกเว้น current thread)
        threads_to_join = []
        if hasattr(self, 'thread_rock_and_sand') and self.thread_rock_and_sand and self.thread_rock_and_sand.is_alive():
            threads_to_join.append(('Rock&Sand', self.thread_rock_and_sand))
        if hasattr(self, 'thread_cement_and_fyash') and self.thread_cement_and_fyash and self.thread_cement_and_fyash.is_alive():
            threads_to_join.append(('Cement&Flyash', self.thread_cement_and_fyash))
        if hasattr(self, 'thread_water') and self.thread_water and self.thread_water.is_alive():
            threads_to_join.append(('Water', self.thread_water))
        if hasattr(self, 'thread_chemical') and self.thread_chemical and self.thread_chemical.is_alive():
            threads_to_join.append(('Chemical', self.thread_chemical))
        
        # ไม่ join main_condition_load ถ้าเรากำลังรันอยู่ในมัน
        if not is_main_condition_thread:
            if hasattr(self, 'thread_main_condition_load') and self.thread_main_condition_load and self.thread_main_condition_load.is_alive():
                threads_to_join.append(('MainCondition', self.thread_main_condition_load))
        else:
            print("   ⚠️ Skipping join of MainCondition thread (current thread)")
        
        for thread_name, thread in threads_to_join:
            print(f"   ⏳ Waiting for {thread_name} thread to finish...")
            try:
                thread.join(timeout=3.0)  # รอสูงสุด 3 วินาทีต่อ thread
                if thread.is_alive():
                    print(f"   ⚠️ {thread_name} thread still alive after timeout")
                else:
                    print(f"   ✓ {thread_name} thread stopped")
            except RuntimeError as e:
                print(f"   ⚠️ Cannot join {thread_name} thread: {e}")
        
        time.sleep(0.5)  # รอเพิ่มเติม
        print("   ✓ All threads cleanup completed")
        
        # 1. หยุด timer และปลดล็อค Target
        self.lock_target_display = False  # ปลดล็อค Target
        
        # หยุด timer อย่างปลอดภัย
        try:
            if hasattr(self, 'target_monitor_timer') and self.target_monitor_timer:
                self.target_monitor_timer.stop()
                print("   ✓ Timer stopped")
            time.sleep(0.3)  # รอให้ timer หยุดสนิท
        except Exception as e:
            print(f"   ⚠️ Error stopping timer: {e}")
        
        # 2. หยุด AutoDA และ PLC Controller threads อย่างสมบูรณ์
        print("   🛑 Stopping AutoDA and PLC controller threads...")
        try:
            # หยุด AutoDA Controller
            if hasattr(self, 'autoda_controller') and self.autoda_controller:
                print("   ⏳ Stopping AutoDA Controller...")
                self.autoda_controller.stop_controller()  # ตั้งค่า running = False
                time.sleep(0.8)  # รอให้ loop หยุด (เพิ่มเวลา)
                # ตรวจสอบว่า thread หยุดแล้วหรือยัง
                if self.autoda_controller.isRunning():
                    print("   ⏳ Waiting for AutoDA thread to stop...")
                    self.autoda_controller.wait(3000)  # รอสูงสุด 3 วินาที (เพิ่มเวลา)
                    if self.autoda_controller.isRunning():
                        print("   ⚠️ AutoDA thread still running after timeout")
                        # Force terminate if needed
                        self.autoda_controller.terminate()
                        self.autoda_controller.wait(1000)
                        print("   ⚠️ AutoDA thread force terminated")
                    else:
                        print("   ✓ AutoDA Controller stopped")
                else:
                    print("   ✓ AutoDA Controller already stopped")
            
            # หยุด PLC Controller
            if hasattr(self, 'plc_controller') and self.plc_controller:
                print("   ⏳ Stopping PLC Controller...")
                self.plc_controller.stop_controller()  # ตั้งค่า running = False
                time.sleep(0.8)  # รอให้ loop หยุด (เพิ่มเวลา)
                # ตรวจสอบว่า thread หยุดแล้วหรือยัง
                if self.plc_controller.isRunning():
                    print("   ⏳ Waiting for PLC thread to stop...")
                    self.plc_controller.wait(3000)  # รอสูงสุด 3 วินาที (เพิ่มเวลา)
                    if self.plc_controller.isRunning():
                        print("   ⚠️ PLC thread still running after timeout")
                        # Force terminate if needed
                        self.plc_controller.terminate()
                        self.plc_controller.wait(1000)
                        print("   ⚠️ PLC thread force terminated")
                    else:
                        print("   ✓ PLC Controller stopped")
                else:
                    print("   ✓ PLC Controller already stopped")
            
            time.sleep(1.5)  # รอให้ทุกอย่างหยุดสนิทและ signal queue ว่าง (เพิ่มเวลา)
            print("   ✓ All controller threads stopped")
            
        except Exception as e:
            print(f"   ⚠️ Error stopping controller threads: {e}")
        
        # 3. Disconnect และ Block signals ชั่วคราว
        try:
            # Disconnect PLC signals
            if hasattr(self, 'plc_controller'):
                try:
                    self.plc_controller.device_status_changed.disconnect(self.update_device_status_indicator)
                    print("   ✓ Disconnected device_status_changed signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect device_status_changed: {e}")
                
                try:
                    self.plc_controller.status_loading_rock_and_sand.disconnect(self.check_loading_rock_and_sand)
                    print("   ✓ Disconnected status_loading_rock_and_sand signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect status_loading_rock_and_sand: {e}")
                
                try:
                    self.plc_controller.status_loading_cement_and_fyash.disconnect(self.check_loading_cement_and_fyash)
                    print("   ✓ Disconnected status_loading_cement_and_fyash signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect status_loading_cement_and_fyash: {e}")
                
                try:
                    self.plc_controller.status_loading_water.disconnect(self.check_loading_water)
                    print("   ✓ Disconnected status_loading_water signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect status_loading_water: {e}")
                
                try:
                    self.plc_controller.status_loading_chemical.disconnect(self.check_loading_chemical)
                    print("   ✓ Disconnected status_loading_chemical signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect status_loading_chemical: {e}")
            
            # Disconnect AutoDA weight signals - CRITICAL!
            if hasattr(self, 'autoda_controller'):
                try:
                    self.autoda_controller.weight_rock_and_sand.disconnect(self.update_weight_rock_and_sand)
                    print("   ✓ Disconnected weight_rock_and_sand signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect weight_rock_and_sand: {e}")
                
                try:
                    self.autoda_controller.weight_cement_and_fyash.disconnect(self.update_weight_cement_and_fyash)
                    print("   ✓ Disconnected weight_cement_and_fyash signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect weight_cement_and_fyash: {e}")
                
                try:
                    self.autoda_controller.weight_water.disconnect(self.update_weight_water)
                    print("   ✓ Disconnected weight_water signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect weight_water: {e}")
                
                try:
                    self.autoda_controller.weight_chemical.disconnect(self.update_weight_chemical)
                    print("   ✓ Disconnected weight_chemical signal")
                except (TypeError, RuntimeError) as e:
                    print(f"   ℹ️ Could not disconnect weight_chemical: {e}")
            
            # Block signals จาก controllers
            if hasattr(self, 'autoda_controller'):
                self.autoda_controller.blockSignals(True)
            if hasattr(self, 'plc_controller'):
                self.plc_controller.blockSignals(True)
            
            print("   ✓ Blocked all controller signals")
            time.sleep(1.5)  # รอให้ signal queue ว่างสนิท (เพิ่มเวลามาก)
            
        except Exception as e:
            print(f"   ⚠️ Error disconnecting/blocking signals: {e}")
        
        # 3. Reset state variables (ปลอดภัย ไม่กระทบ UI)
        self.current_queue_loaded = 0
        self.current_queue_transporting = 0
        self.completed_queue_count = 0
        self.total_queue_count = 1
        self.rock_and_sand_loading_success = False
        self.cement_and_fyash_loading_success = False
        self.water_loading_success = False
        self.chemical_loading_success = False
        self.rock_and_sand_success_start_main = False
        self.cement_and_fyash_success_start_main = False
        self.water_success_start_main = False
        self.chemical_success_start_main = False
        self.next_queue_loaded_and_ready = False
        self.ready_to_start_next_load = False
        self.reset_freeze_values()
        self.state_load_rock_and_sand = 0
        self.state_load_cement_and_fyash = 0
        self.state_load_water = 0
        self.state_load_chemical = 0
        self.state_main_condition_load = 0
        print("   ✓ All state variables reset")
        
        # 4. Process pending events to clear signal queue (ระมัดระวังมาก)
        try:
            app = QApplication.instance()
            if app:
                app.processEvents()
                time.sleep(0.3)
                app.processEvents()
                print("   ✓ Processed pending events")
        except Exception as e:
            print(f"   ⚠️ Error processing events: {e}")
        
        # 5. เก็บค่า total_cubes สำหรับแสดงผล
        total_cubes = self.get_all_loaded_cube
        print(f"   ✓ Total cubes completed: {total_cubes}")
        
        # 6. ใช้ Signal เพื่อ emit ไปยัง main thread (ไม่ใช้ QTimer เพราะไม่สามารถสร้างจาก worker thread)
        print("   ✓ Emitting finalize_reset_signal...")
        try:
            # Emit signal ไปยัง main thread โดยตรง (Qt จะจัดการ thread safety ให้)
            self.finalize_reset_signal.emit(total_cubes)
            print("   ✓ Signal emitted successfully - finalize will run in main thread")
        except Exception as e:
            print(f"   ⚠️ Error emitting finalize_reset_signal: {e}")
            # Fallback: ลองทำแบบปกติ
            try:
                self.reset_ui_signal.emit()
                time.sleep(0.3)
                if hasattr(self, 'autoda_controller'):
                    self.autoda_controller.blockSignals(False)
                if hasattr(self, 'plc_controller'):
                    self.plc_controller.blockSignals(False)
                self.work_completed.emit(total_cubes)
            except Exception as e2:
                print(f"   ⚠️ Fallback also failed: {e2}")
    
    @Slot(float)
    def _finalize_reset(self, total_cubes):
        """Finalize reset ใน main thread - ถูกเรียกผ่าน Signal"""
        print("   🔧 Finalizing reset in main thread...")
        
        # รอสักครู่เพื่อให้ main_condition_load thread มีเวลาจบ
        time.sleep(0.8)
        
        try:
            # Reset UI
            self.reset_ui_signal.emit()
            time.sleep(0.8)  # รอให้ UI reset เสร็จ (เพิ่มเวลา)
            print("   ✓ UI reset completed")
        except Exception as e:
            print(f"   ⚠️ Error emitting reset_ui_signal: {e}")
        
        # Process events เพื่อให้แน่ใจว่า UI reset เสร็จสมบูรณ์
        try:
            app = QApplication.instance()
            if app:
                app.processEvents()
                time.sleep(0.3)
                print("   ✓ UI events processed")
        except Exception as e:
            print(f"   ⚠️ Error processing UI events: {e}")
        
        # 🔄 เริ่ม AutoDA และ PLC Controller threads ใหม่
        print("   🔄 Restarting AutoDA and PLC controller threads...")
        try:
            # เริ่ม AutoDA Controller ใหม่
            if hasattr(self, 'autoda_controller') and self.autoda_controller:
                if not self.autoda_controller.isRunning():
                    print("   ⏳ Restarting AutoDA Controller...")
                    # Reset running flag และเริ่มใหม่
                    self.autoda_controller.running = True
                    self.autoda_controller.start()
                    time.sleep(0.5)  # เพิ่มเวลารอ
                    if self.autoda_controller.isRunning():
                        print("   ✓ AutoDA Controller restarted")
                    else:
                        print("   ⚠️ AutoDA Controller failed to restart")
                else:
                    print("   ℹ️ AutoDA Controller already running")
            
            # เริ่ม PLC Controller ใหม่
            if hasattr(self, 'plc_controller') and self.plc_controller:
                if not self.plc_controller.isRunning():
                    print("   ⏳ Restarting PLC Controller...")
                    # Reset running flag และเริ่มใหม่
                    self.plc_controller.running = True
                    self.plc_controller.start()
                    time.sleep(0.5)  # เพิ่มเวลารอ
                    if self.plc_controller.isRunning():
                        print("   ✓ PLC Controller restarted")
                    else:
                        print("   ⚠️ PLC Controller failed to restart")
                else:
                    print("   ℹ️ PLC Controller already running")
            
            time.sleep(1.0)  # รอให้ controllers เริ่มทำงานสนิทและเสถียร (เพิ่มเวลา)
            print("   ✓ All controller threads restarted")
            
        except Exception as e:
            print(f"   ⚠️ Error restarting controller threads: {e}")
        
        # Reconnect และ Unblock signals
        try:
            # Reconnect PLC signals (ไม่ต้อง disconnect เพราะถูก disconnect ไปแล้วใน _reset_all_for_new_customer)
            if hasattr(self, 'plc_controller'):
                # Connect signal ใหม่โดยตรง
                self.plc_controller.device_status_changed.connect(self.update_device_status_indicator)
                print("   ✓ Reconnected device_status_changed signal")
                
                self.plc_controller.status_loading_rock_and_sand.connect(self.check_loading_rock_and_sand)
                print("   ✓ Reconnected status_loading_rock_and_sand signal")
                
                self.plc_controller.status_loading_cement_and_fyash.connect(self.check_loading_cement_and_fyash)
                print("   ✓ Reconnected status_loading_cement_and_fyash signal")
                
                self.plc_controller.status_loading_water.connect(self.check_loading_water)
                print("   ✓ Reconnected status_loading_water signal")
                
                self.plc_controller.status_loading_chemical.connect(self.check_loading_chemical)
                print("   ✓ Reconnected status_loading_chemical signal")
            
            # Reconnect AutoDA weight signals (ไม่ต้อง disconnect เพราะถูก disconnect ไปแล้ว)
            if hasattr(self, 'autoda_controller'):
                self.autoda_controller.weight_rock_and_sand.connect(self.update_weight_rock_and_sand)
                print("   ✓ Reconnected weight_rock_and_sand signal")
                
                self.autoda_controller.weight_cement_and_fyash.connect(self.update_weight_cement_and_fyash)
                print("   ✓ Reconnected weight_cement_and_fyash signal")
                
                self.autoda_controller.weight_water.connect(self.update_weight_water)
                print("   ✓ Reconnected weight_water signal")
                
                self.autoda_controller.weight_chemical.connect(self.update_weight_chemical)
                print("   ✓ Reconnected weight_chemical signal")
            
            # Unblock signals
            if hasattr(self, 'autoda_controller'):
                self.autoda_controller.blockSignals(False)
            if hasattr(self, 'plc_controller'):
                self.plc_controller.blockSignals(False)
            print("   ✓ Unblocked controller signals")
        except Exception as e:
            print(f"   ⚠️ Error reconnecting/unblocking signals: {e}")
        
        # รอให้ทุกอย่างพร้อมก่อนแสดงผล
        time.sleep(1.0)  # เพิ่มเวลารอให้ทุกอย่างเสถียร
        
        # ปลดบล็อก is_tab_switching เพื่อให้ weight updates ทำงานได้อีกครั้ง
        self.is_tab_switching = False
        print("   ✓ UI updates re-enabled")
        
        # Emit work_completed signal
        try:
            self.work_completed.emit(total_cubes)
            print("✅ Reset complete - ready for new customer")
        except Exception as e:
            print(f"   ⚠️ Error emitting work_completed signal: {e}")
            
    def reset_variable_for_cement_loaded(self):
        self.cement_start_time = 0
        self.cement_start_weight = 0
        self.cement_follow_weight = 0
        self.end_cement_time = 0
        self.loading_duration = 0
        self.now_weight = 0
        self.remain = 0
        self.first_weight_loaded = 0
        self.time_loaded_duration = 0
        self.rate_loaded = 0
        self.extra_time = 0
        self.tried_weight = 0
        self.retry_count = 0
        self.target = 0
        self.diff = 0
        self.safe_fill_time = 0
        
        
        
    @Slot()
    def _reset_ui_safe(self):
        """Reset UI อย่างปลอดภัยใน main thread"""
        try:
            # ตรวจสอบว่า main_window ยังมีอยู่และไม่ถูก destroy
            if not hasattr(self, 'main_window') or self.main_window is None:
                print("   ⚠️ main_window is None in _reset_ui_safe")
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                print("   ⚠️ main_window has been destroyed in _reset_ui_safe")
                return
            
            # Reset แต่ละ field ด้วย try-except แยกเพื่อป้องกัน crash
            fields_to_reset = [
                ('mix_result_mix_lineEdit', '0'),
                ('mix_result_mix_success_lineEdit', '0'),
                ('mix_monitor_rock_1_lineEdit', '0'),
                ('mix_monitor_sand_lineEdit', '0'),
                ('mix_monitor_rock_2_lineEdit', '0'),
                ('mix_monitor_cement_lineEdit', '0'),
                ('mix_monitor_fyash_lineEdit', '0'),
                ('mix_monitor_water_lineEdit', '0'),
                ('mix_monitor_chem_1_lineEdit', '0'),
                ('mix_monitor_chem_2_lineEdit', '0'),
                ('mix_wieght_Loaded_rock_1_lineEdit', '0'),
                ('mix_wieght_Loaded_sand_lineEdit', '0'),
                ('mix_wieght_Loaded_rock_2_lineEdit', '0'),
                ('mix_wieght_Loaded_cement_lineEdit', '0'),
                ('mix_wieght_Loaded_fyash_lineEdit', '0'),
                ('mix_wieght_Loaded_water_lineEdit', '0'),
                ('mix_wieght_Loaded_chem_1_lineEdit', '0'),
                ('mix_wieght_Loaded_chem_2_lineEdit', '0'),
            ]
            
            for field_name, value in fields_to_reset:
                try:
                    if hasattr(self.main_window, field_name):
                        field = getattr(self.main_window, field_name)
                        field.setText(value)
                except (RuntimeError, AttributeError) as e:
                    # ข้าม field นี้ถ้า error
                    pass
                    
            print("   ✓ UI fields reset completed")
            
        except RuntimeError as e:
            # Qt object ถูก destroy แล้ว ไม่ต้องทำอะไร
            print(f"   ⚠️ Warning: Qt object already destroyed in reset UI: {e}")
        except Exception as e:
            print(f"   ⚠️ Warning: Error resetting UI: {e}")
    
    @Slot(float)
    
    def cleanup_on_exit(self):
        print("Cleaning up before application exit...")
        
        # 1. หยุด Thread main_condition_load (ถ้ามี)
        self.main_condition_load_running = False

        # 2. หยุด PLC Controller ก่อน
        if hasattr(self, 'plc_controller'):
            print("Stopping PLC controller...")
            try:
                if hasattr(self.plc_controller, 'stop_controller'):
                    self.plc_controller.stop_controller()  # 1. เรียกเมธอดที่เราสร้าง
                self.plc_controller.quit()                 # 2. สั่งหยุด QThread
                if not self.plc_controller.wait(3000):     # 3. รอให้หยุดสนิท (timeout 3 วินาที)
                    print("⚠️ PLC controller did not stop gracefully, forcing termination")
                    self.plc_controller.terminate()
                print("✅ PLC controller stopped.")
            except Exception as e:
                print(f"❌ Error stopping PLC controller: {e}")

        # 3. หยุด AutoDA Controller
        if hasattr(self, 'autoda_controller'):
            print("Stopping AutoDA controller...")
            try:
                if hasattr(self.autoda_controller, 'stop_controller'):
                    self.autoda_controller.stop_controller()  # 1. เรียกเมธอดที่เราสร้าง
                self.autoda_controller.quit()                 # 2. สั่งหยุด QThread
                if not self.autoda_controller.wait(3000):     # 3. รอให้หยุดสนิท (timeout 3 วินาที)
                    print("⚠️ AutoDA controller did not stop gracefully, forcing termination")
                    self.autoda_controller.terminate()
                print("✅ AutoDA controller stopped.")
            except Exception as e:
                print(f"❌ Error stopping AutoDA controller: {e}")
            
        # 4. หยุด Loading Threads (ถ้ามีการโหลดอยู่)
        if self.start_button_load_enabled == True:
            print("Stopping loading threads...")
            self.reset_freeze_values()
            self.lock_target_display = False  # ปลดล็อค Target UI เมื่อยกเลิก
            self._stop_target_monitor()  # หยุด monitor
            
            if self.is_loading_rock_and_sand_in_progress:
                self.is_loading_rock_and_sand_in_progress = False
                if hasattr(self, 'thread_rock_and_sand') and self.thread_rock_and_sand.is_alive():
                    self.thread_rock_and_sand.join(timeout=2)
                    
            if self.is_loading_cement_and_fyash_in_progress:
                self.is_loading_cement_and_fyash_in_progress = False
                if hasattr(self, 'thread_cement_and_fyash') and self.thread_cement_and_fyash.is_alive():
                    self.thread_cement_and_fyash.join(timeout=2)
                    
            if self.is_loading_water_in_progress:
                self.is_loading_water_in_progress = False
                if hasattr(self, 'thread_water') and self.thread_water.is_alive():
                    self.thread_water.join(timeout=2)
                    
            if self.is_loading_chemical_in_progress:
                self.is_loading_chemical_in_progress = False
                if hasattr(self, 'thread_chemical') and self.thread_chemical.is_alive():
                    self.thread_chemical.join(timeout=2)
                    
            if hasattr(self, 'thread_main_condition_load') and self.thread_main_condition_load.is_alive():
                self.main_condition_load_running = False
                self.thread_main_condition_load.join(timeout=2)
                
            print("✅ All loading threads stopped.")
            
        print("=" * 60)
        print("✅ Cleanup complete. Application will now exit.")
        print("=" * 60)
    # ===================================================
    
    @Slot(float)
    def _show_completion_message(self, total_cubes):
        """แสดง MessageBox แจ้งเตือนว่างานเสร็จและกลับไปหน้า Work Tab - Thread Safe"""
        # ใช้ QTimer.singleShot เพื่อ defer การแสดง MessageBox
        # เพื่อให้ signal อื่น ๆ ทำงานเสร็จก่อน
        QTimer.singleShot(500, lambda: self._do_show_completion(total_cubes))  # เพิ่มเวลารอเป็น 500ms
    
    def _do_show_completion(self, total_cubes):
        """ฟังก์ชันจริงที่แสดง completion message - ถูกเรียกผ่าน QTimer"""
        try:
            # ตรวจสอบว่า main_window ยังมีอยู่และไม่ถูก destroy
            if not hasattr(self, 'main_window') or self.main_window is None:
                print("⚠️ main_window is None, skipping completion message")
                return
            
            # ตรวจสอบ Qt application ยังทำงานอยู่
            app = QApplication.instance()
            if app is None or app.closingDown():
                print("⚠️ Application is closing, skipping completion message")
                return
            
            # ตรวจสอบ Qt object
            try:
                self.main_window.objectName()
            except RuntimeError:
                print("⚠️ main_window has been destroyed, skipping completion message")
                return
                
            msg_box = QMessageBox(self.main_window)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("งานเสร็จสมบูรณ์")
            msg_box.setText(f"✅ การผสมคอนกรีตเสร็จสมบูรณ์แล้ว\n\n"
                           f"จำนวนที่ผสม: {round(total_cubes, 1)} คิว\n"
                           f"สถานะ: เสร็จสิ้น")
            msg_box.setInformativeText("กรุณาเลือกลูกค้ารายใหม่เพื่อเริ่มงานต่อไป")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setDefaultButton(QMessageBox.Ok)
            
            # เล่นเสียงแจ้งเตือน (ถ้ามี)
            try:
                QApplication.beep()
            except:
                pass
            
            # แสดง MessageBox (blocking call)
            result = msg_box.exec()
            
            # ตรวจสอบก่อนลบ msg_box
            try:
                msg_box.objectName()  # ตรวจสอบว่ายังมีอยู่
                msg_box.deleteLater()
            except RuntimeError:
                # msg_box ถูกลบแล้ว ไม่ต้องทำอะไร
                pass
            
            # รอสักครู่ให้ MessageBox cleanup เสร็จ
            time.sleep(0.5)
            
            # หลังจากกด OK ให้ switch tab ด้วย Signal
            if result == QMessageBox.Ok:
                # ตรวจสอบอีกครั้งก่อน emit signal
                try:
                    self.main_window.objectName()
                    app = QApplication.instance()
                    if app and not app.closingDown():
                        self.switch_to_work_tab_signal.emit()
                    else:
                        print("⚠️ Application closing, skipping tab switch")
                except RuntimeError:
                    print("⚠️ main_window destroyed before tab switch")
                
        except RuntimeError as e:
            # Qt object ถูก destroy แล้ว
            print(f"⚠️ Warning: Qt object already destroyed in completion message: {e}")
        except Exception as e:
            print(f"⚠️ Error showing completion message: {e}")
            import traceback
            traceback.print_exc()
    
    @Slot()
    def _switch_to_work_tab_safe(self):
        """Switch ไปหน้า Work Tab อย่างปลอดภัย"""
        print("🔄 _switch_to_work_tab_safe called")
        
        # Set flag เพื่อป้องกันการ access UI widgets ระหว่างที่กำลัง switch
        self.is_tab_switching = True
        print("   ✓ Tab switching flag set to True")
        
        # ใช้ QTimer.singleShot เพื่อ defer การ switch tab ไปยัง event loop ถัดไป
        # เพื่อให้ Qt ทำ cleanup และ reconnect signals เสร็จก่อน
        # เพิ่มเวลารอเป็น 800ms เพื่อให้แน่ใจว่า signals reconnect เสร็จ
        QTimer.singleShot(800, self._do_switch_tab)
    
    def _do_switch_tab(self):
        """ฟังก์ชันจริงที่ทำการ switch tab - ถูกเรียกผ่าน QTimer"""
        try:
            # ตรวจสอบหลายชั้น
            if not hasattr(self, 'main_window') or self.main_window is None:
                print("   ⚠️ main_window is None or doesn't exist")
                return
            
            # ตรวจสอบว่า Qt application ยังทำงานอยู่
            app = QApplication.instance()
            if app is None or app.closingDown():
                print("   ⚠️ Application is closing down")
                return
            
            print("   ✓ main_window exists and app is running")
            
            # ตรวจสอบ Qt object ก่อนทำอะไร
            try:
                self.main_window.objectName()  # ทดสอบว่า object ยังใช้งานได้
            except RuntimeError:
                print("   ⚠️ main_window object has been destroyed")
                return
                
            if hasattr(self.main_window, 'tab') and hasattr(self.main_window, 'work_tab'):
                print("   ✓ tab and work_tab exist, verifying widgets...")
                
                # ตรวจสอบ widget ก่อนใช้งาน
                try:
                    self.main_window.tab.objectName()
                    self.main_window.work_tab.objectName()
                    print("   ✓ Widgets are valid, switching...")
                except RuntimeError:
                    print("   ⚠️ tab or work_tab widget has been destroyed")
                    return
                
                # Switch tab อย่างปลอดภัย พร้อม exception handling
                try:
                    self.main_window.tab.setCurrentWidget(self.main_window.work_tab)
                    print("📋 Switched to Work Tab - Ready for new customer")
                    
                    # Clear flag หลัง switch เสร็จ
                    self.is_tab_switching = False
                    print("   ✓ Tab switching flag cleared")
                    
                    # รอให้ Qt process event
                    time.sleep(0.1)
                    
                    print("=" * 60)
                    print("🎉 System is ready for next customer!")
                    print("=" * 60)
                except RuntimeError as e:
                    print(f"   ⚠️ Error during tab switch: {e}")
                    self.is_tab_switching = False  # Clear flag แม้ error
                    return
                except Exception as e:
                    print(f"   ⚠️ Unexpected error during tab switch: {e}")
                    self.is_tab_switching = False  # Clear flag แม้ error
                    return
            else:
                print("   ⚠️ tab or work_tab doesn't exist")
                self.is_tab_switching = False  # Clear flag
                
        except RuntimeError as e:
            # Qt object ถูก destroy แล้ว
            print(f"⚠️ Warning: Qt object already destroyed during switch: {e}")
            self.is_tab_switching = False  # Clear flag
        except Exception as e:
            print(f"⚠️ Error switching to work tab: {e}")
            self.is_tab_switching = False  # Clear flag
            import traceback
            traceback.print_exc()



