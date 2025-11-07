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
        self.stabilize_delay = 2.5  # วินาที
        
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

        self.main_window.set_readonly_mix_weights()
        self.read_offset_formular_mixer()
        # self.plc_controller.off_all_device()
        
    @Slot(list)
    @Slot(int)
    
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

    def _set_weight_display(self, material, weight):
        if material == "rock1":
            self.main_window.mix_monitor_rock_1_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_rock_1_lineEdit.setText(str(weight))
        elif material == "sand":
            self.main_window.mix_monitor_sand_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_sand_lineEdit.setText(str(weight))
        elif material == "rock2":
            self.main_window.mix_monitor_rock_2_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_rock_2_lineEdit.setText(str(weight))

    def _get_display_weight(self, material, current_weight):
        if material == "rock1":
            return self.rock1_frozen_weight if self.is_rock1_frozen else current_weight
        elif material == "sand":
            if self.is_sand_frozen and hasattr(self, 'sand_only_frozen'):
                return self.sand_only_frozen
            else:
                sand_only = current_weight - self.rock1_frozen_weight if self.is_rock1_frozen else current_weight
                return max(0, sand_only)
        elif material == "rock2":
            if self.is_rock2_frozen and hasattr(self, 'rock2_only_frozen'):
                return self.rock2_only_frozen
            else:
                rock2_only = current_weight - self.sand_frozen_weight if self.is_sand_frozen else 0
                return max(0, rock2_only)
        return current_weight

    def _check_freeze_conditions(self, current_weight):
        import time
        current_time = time.time()
        
        # ตรวจสอบ Rock1 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_rock_and_sand == 2 and self.rock_success and not self.is_rock1_frozen):
            if not self.rock1_stabilizing:
                self.rock1_stabilizing = True
                self.rock1_stabilize_start_time = current_time
                print(f"🪨 Rock1 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.rock1_stabilize_start_time >= self.stabilize_delay:
                self.rock1_frozen_weight = current_weight
                self.is_rock1_frozen = True
                self.rock1_stabilizing = False
                print(f"✅ Rock1 frozen at: {self.rock1_frozen_weight} kg")

        # ตรวจสอบ Sand freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_rock_and_sand == 4 and self.rock_success and not self.is_sand_frozen):
            if not self.sand_stabilizing:
                self.sand_stabilizing = True
                self.sand_stabilize_start_time = current_time
                print(f"🏖️ Sand PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.sand_stabilize_start_time >= self.stabilize_delay:
                self.sand_frozen_weight = current_weight
                self.sand_only_frozen = max(0, current_weight - self.rock1_frozen_weight if self.is_rock1_frozen else current_weight)
                self.is_sand_frozen = True
                self.sand_stabilizing = False
                print(f"✅ Sand frozen at total: {self.sand_frozen_weight} kg (Sand only: {self.sand_only_frozen} kg)")

        # ตรวจสอบ Rock2 freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_rock_and_sand == 6 and self.rock_success and not self.is_rock2_frozen):
            if not self.rock2_stabilizing:
                self.rock2_stabilizing = True
                self.rock2_stabilize_start_time = current_time
                print(f"🪨 Rock2 PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.rock2_stabilize_start_time >= self.stabilize_delay:
                self.rock2_frozen_weight = current_weight
                self.rock2_only_frozen = max(0, current_weight - self.sand_frozen_weight if self.is_sand_frozen else 0)
                self.is_rock2_frozen = True
                self.rock2_stabilizing = False
                print(f"✅ Rock2 frozen at total: {self.rock2_frozen_weight} kg (Rock2 only: {self.rock2_only_frozen} kg)")

    def update_weight_rock_and_sand(self, weight):
        current_weight = int(weight)
        if self.is_loading_rock_and_sand_in_progress:
            self._check_freeze_conditions(current_weight)
        if self.state_load_rock_and_sand == 2:  # Loading Rock1
            self._set_weight_display("rock1", current_weight)
            self._set_weight_display("sand", 0)
            self._set_weight_display("rock2", 0)
        elif self.state_load_rock_and_sand == 4:  # Loading Sand
            self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
            self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
            self._set_weight_display("rock2", 0)
        elif self.state_load_rock_and_sand == 6:  # Loading Rock2
            self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
            self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
            self._set_weight_display("rock2", self._get_display_weight("rock2", current_weight))
        elif self.state_load_rock_and_sand in [3, 5]:  # Transition states
            self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
            if self.state_load_rock_and_sand == 5:
                self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
            else:
                self._set_weight_display("sand", 0)
            self._set_weight_display("rock2", 0)
        else:  # Default state (loading complete or not loading)
            self._set_weight_display("rock1", self._get_display_weight("rock1", current_weight))
            self._set_weight_display("sand", self._get_display_weight("sand", current_weight))
            self._set_weight_display("rock2", self._get_display_weight("rock2", current_weight))

    def _set_cement_fyash_display(self, material, weight):
        """Helper function to set cement/fyash weight display"""
        if material == "cement":
            self.main_window.mix_monitor_cement_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_cement_lineEdit.setText(str(weight))
        elif material == "fyash":
            self.main_window.mix_monitor_fyash_lineEdit.setText(str(weight))
            self.main_window.mix_wieght_Loaded_fyash_lineEdit.setText(str(weight))

    def _get_cement_fyash_display_weight(self, material, current_weight):
        """Get cement/fyash display weight based on freeze status"""
        if material == "cement":
            return getattr(self, 'cement_frozen_weight', current_weight) if getattr(self, 'is_cement_frozen', False) else current_weight
        elif material == "fyash":
            if getattr(self, 'is_fyash_frozen', False) and hasattr(self, 'fyash_only_frozen'):
                return self.fyash_only_frozen
            else:
                cement_frozen = getattr(self, 'cement_frozen_weight', 0)
                fyash_only = current_weight - cement_frozen if getattr(self, 'is_cement_frozen', False) else current_weight
                return max(0, fyash_only)
        return current_weight

    def _check_cement_fyash_freeze_conditions(self, current_weight):
        """Check and update cement/fyash freeze conditions"""
        import time
        current_time = time.time()
        
        # ตรวจสอบ Cement freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_cement_and_fyash == 2 and 
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
                # print(f"Cement frozen at: {self.cement_frozen_weight}")

        # ตรวจสอบ Fyash freeze - รอให้ PLC ส่งสัญญาณเสร็จก่อน จึงค่อย stabilize
        if (self.state_load_cement_and_fyash == 4 and
            getattr(self, 'cement_success', False) and
            not getattr(self, 'is_fyash_frozen', False)):
            
            if not self.fyash_stabilizing:
                self.fyash_stabilizing = True
                self.fyash_stabilize_start_time = current_time
                # print(f"Fyash PLC finished, stabilizing... Current weight: {current_weight}")
            elif current_time - self.fyash_stabilize_start_time >= self.stabilize_delay:
                self.fyash_frozen_weight = current_weight
                cement_frozen = getattr(self, 'cement_frozen_weight', 0)
                self.fyash_only_frozen = max(0, current_weight - cement_frozen if getattr(self, 'is_cement_frozen', False) else current_weight)
                self.is_fyash_frozen = True
                self.fyash_stabilizing = False
                # print(f"Fyash frozen at total: {self.fyash_frozen_weight} (Fyash only: {self.fyash_only_frozen})")

    def update_weight_cement_and_fyash(self, weight):
        current_weight = int(weight)
        
        # Check freeze conditions during loading
        if getattr(self, 'is_loading_cement_and_fyash_in_progress', False):
            self._check_cement_fyash_freeze_conditions(current_weight)

        # Update displays based on current state
        state = getattr(self, 'state_load_cement_and_fyash', 0)
        if state == 2:  # Loading Cement
            self._set_cement_fyash_display("cement", current_weight)
            self._set_cement_fyash_display("fyash", 0)
        elif state == 4:  # Loading Fyash
            self._set_cement_fyash_display("cement", self._get_cement_fyash_display_weight("cement", current_weight))
            self._set_cement_fyash_display("fyash", self._get_cement_fyash_display_weight("fyash", current_weight))
        elif state == 3:  # Transition state
            self._set_cement_fyash_display("cement", self._get_cement_fyash_display_weight("cement", current_weight))
            self._set_cement_fyash_display("fyash", 0)
        else:  # Default state (loading complete or not loading)
            self._set_cement_fyash_display("cement", self._get_cement_fyash_display_weight("cement", current_weight))
            self._set_cement_fyash_display("fyash", self._get_cement_fyash_display_weight("fyash", current_weight))

    def _set_water_display(self, weight):
        """Helper function to set water weight display"""
        self.main_window.mix_monitor_water_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_water_lineEdit.setText(str(weight))

    def _get_water_display_weight(self, current_weight):
        """Get water display weight based on freeze status"""
        return getattr(self, 'water_frozen_weight', current_weight) if getattr(self, 'is_water_frozen', False) else current_weight

    def _check_water_freeze_conditions(self, current_weight):
        """Check and update water freeze conditions"""
        import time
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
        current_weight = int(weight)
        
        # Check freeze conditions during loading
        if getattr(self, 'is_loading_water_in_progress', False):
            self._check_water_freeze_conditions(current_weight)

        # Always display the appropriate weight (frozen or current)
        self._set_water_display(self._get_water_display_weight(current_weight))

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
        import time
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
        if (self.rock_and_sand_success_start_main and 
            self.cement_and_fyash_success_start_main and 
            self.water_success_start_main and 
            self.chemical_success_start_main):
            # ถ้าโหลดเสร็จทุกอย่างแล้ว ให้ตั้ง flag บอกว่าพร้อมลำเลียงขึ้นไป
            self.next_queue_loaded_and_ready = True
            # print(f"Queue {self.current_queue_loaded} is fully loaded and ready for transport!")

    def mix_start_load(self):
        # ตรวจสอบจำนวนคิว ถ้ามี error จะ return ทันที
        try:
            self.check_all_result_loaded()
        except ValueError as e:
            # Error message ถูกแสดงใน check_all_result_loaded แล้ว
            return
        
        self.reset_freeze_values()
        
        # รีเซ็ต counter
        self.current_queue_transporting = 0
        self.completed_queue_count = 0  # รีเซ็ตจำนวนคิวที่ผสมเสร็จ
        self.next_queue_loaded_and_ready = False
        self.lock_target_display = True  # ล็อค Target UI ตั้งแต่เริ่มโหลด
        
        # รีเซ็ตการแสดงผลจำนวนคิว
        self.main_window.mix_result_mix_lineEdit.setText("0")
        self.main_window.mix_result_mix_success_lineEdit.setText("0")
        
        # อ่านค่าจากฟอร์มและเก็บค่าต้นฉบับ
        result = self.main_window.get_data_formular_in_mix_form()
        if result is None:
            # print("❌ Error: Target values are empty. Please select a work order first.")
            QMessageBox.warning(
                self.main_window,
                "ไม่สามารถเริ่มโหลดได้",
                "กรุณาเลือกคิวงานก่อนเริ่มโหลด\n(ค่า Target ว่างเปล่า)"
            )
            self.lock_target_display = False
            return
        
        self.original_rock1, self.original_sand, self.original_rock2, self.original_cement, self.original_fyash, self.original_water, self.original_chem1, self.original_chem2 = result
        
        # print(f"📋 Original values from UI:")
        # print(f"   Rock1={self.original_rock1}, Sand={self.original_sand}, Rock2={self.original_rock2}")
        # print(f"   Cement={self.original_cement}, Fyash={self.original_fyash}, Water={self.original_water}")
        # print(f"   Chem1={self.original_chem1}, Chem2={self.original_chem2}")
        
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
        
        # อัพเดต Target ใน UI ทันที
        self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
        self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
        self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
        self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
        self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
        self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
        self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
        self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
        
        # เริ่ม target monitor
        self._start_target_monitor()
        
        # print(f"🔒 Target UI LOCKED at start")
        # print(f"Loading with multiplier: {self.queue_multiplier}")
        # print(f"Rock1: {self.rock1}, Sand: {self.sand}, Rock2: {self.rock2}")
        # print(f"Cement: {self.cement}, Fyash: {self.fyash}, Water: {self.water}")
        # print(f"Chem1: {self.chem1}, Chem2: {self.chem2}")
        
        self.rock_and_sand_values = [int(self.rock1), int(self.sand), int(self.rock2)]
        self.cement_and_fyash_values = [int(self.cement), int(self.fyash)]
        self.water_value = int(self.water)
        self.chemical_values = [float(self.chem1), float(self.chem2)]
        
        time.sleep(1)
        self.is_loading_rock_and_sand_in_progress = True
        self.thread_rock_and_sand = Thread(target=self.load_rock_and_sand_sequence,args=(self.rock_and_sand_values,))
        self.thread_rock_and_sand.start()
        self.state_load_rock_and_sand = 1
        time.sleep(1)
        self.is_loading_cement_and_fyash_in_progress = True
        self.thread_cement_and_fyash = Thread(target=self.load_cement_and_fyash_sequence,args=(self.cement_and_fyash_values,))
        self.thread_cement_and_fyash.start()
        self.state_load_cement_and_fyash = 1
        time.sleep(1)
        self.is_loading_water_in_progress = True
        self.thread_water = Thread(target=self.loading_water_sequence, args=(self.water_value,))
        self.thread_water.start()
        self.state_load_water = 1
        time.sleep(1)
        self.is_loading_chemical_in_progress = True
        self.thread_chemical = Thread(target=self.loading_chemical_sequence, args=(self.chemical_values,))
        self.thread_chemical.start()
        self.state_load_chemical = 1
        
        # print("Started loading sequence.")
        self.main_condition_load_running = True
        self.state_main_condition_load = 0  # เริ่มที่ state 0
        self.thread_main_condition_load = Thread(target=self.main_condition_load)
        self.thread_main_condition_load.start()
        
        
        
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
        # print("Starting new loading sequence...")
        
        # รีเซ็ต success flags สำหรับการโหลดใหม่
        self.rock_and_sand_loading_success = False
        self.cement_and_fyash_loading_success = False
        self.water_loading_success = False
        self.chemical_loading_success = False
        self.rock_and_sand_success_start_main = False
        self.cement_and_fyash_success_start_main = False
        self.water_success_start_main = False
        self.chemical_success_start_main = False
        
        # รีเซ็ต freeze values สำหรับการโหลดใหม่
        self.reset_freeze_values()
        
        # ดึง multiplier สำหรับรอบถัดไป
        next_queue_index = self.current_queue_loaded  # current_queue_loaded ถูกเพิ่มแล้วใน start_next_load_ready
        if next_queue_index < len(self.queue_multipliers):
            next_multiplier = self.queue_multipliers[next_queue_index]
            
            # อัพเดต Target UI ตาม multiplier ของรอบนี้ (ต้องทำก่อนเริ่ม threads)
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
        
        # เริ่มโหลดในแต่ละ thread
        time.sleep(1)
        self.is_loading_rock_and_sand_in_progress = True
        self.thread_rock_and_sand = Thread(target=self.load_rock_and_sand_sequence, args=(self.rock_and_sand_values,))
        self.thread_rock_and_sand.start()
        self.state_load_rock_and_sand = 1
        
        time.sleep(1)
        self.is_loading_cement_and_fyash_in_progress = True
        self.thread_cement_and_fyash = Thread(target=self.load_cement_and_fyash_sequence, args=(self.cement_and_fyash_values,))
        self.thread_cement_and_fyash.start()
        self.state_load_cement_and_fyash = 1
        
        time.sleep(1)
        self.is_loading_water_in_progress = True
        self.thread_water = Thread(target=self.loading_water_sequence, args=(self.water_value,))
        self.thread_water.start()
        self.state_load_water = 1
        
        time.sleep(1)
        self.is_loading_chemical_in_progress = True
        self.thread_chemical = Thread(target=self.loading_chemical_sequence, args=(self.chemical_values,))
        self.thread_chemical.start()
        self.state_load_chemical = 1
        
        self.ready_to_start_next_load = False

    def _update_target_display(self, multiplier):
        """อัพเดตค่าเป้าหมาย (Target) ใน UI ตาม multiplier"""
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
        
        # อัพเดต UI หลายครั้งเพื่อให้แน่ใจว่าค่าถูกต้อง
        for _ in range(3):  # อัพเดต 3 ครั้งเพื่อความแน่ใจ
            self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
            self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
            self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
            self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
            self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
            self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
            self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
            self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
            time.sleep(0.1)  # หน่วงเวลาเล็กน้อย
        
        # เริ่ม timer เพื่อตรวจสอบและรักษาค่า Target
        self._start_target_monitor()
    
    def _start_target_monitor(self):
        """เริ่ม timer เพื่อตรวจสอบและรักษาค่า Target UI"""
        if not hasattr(self, 'target_monitor_timer'):
            self.target_monitor_timer = QTimer()
            self.target_monitor_timer.timeout.connect(self._maintain_target_display)
        
        if self.lock_target_display:
            self.target_monitor_timer.start(500)  # ตรวจสอบทุก 500ms
    
    def _stop_target_monitor(self):
        """หยุด timer ตรวจสอบ Target UI"""
        if hasattr(self, 'target_monitor_timer'):
            self.target_monitor_timer.stop()
            # print("⏹️ Target monitor stopped")
    
    def _maintain_target_display(self):
        """รักษาค่า Target UI ให้คงที่ตามที่ตั้งไว้"""
        if not self.lock_target_display:
            self._stop_target_monitor()
            return
        
        # ตรวจสอบและแก้ไขค่าถ้ามีการเปลี่ยนแปลง
        current_rock1 = self.main_window.mix_wieght_target_rock_1_lineEdit.text()
        if current_rock1 != str(self.display_target_rock1):
            self.main_window.mix_wieght_target_rock_1_lineEdit.setText(str(self.display_target_rock1))
        
        current_sand = self.main_window.mix_wieght_target_sand_lineEdit.text()
        if current_sand != str(self.display_target_sand):
            self.main_window.mix_wieght_target_sand_lineEdit.setText(str(self.display_target_sand))
        
        current_rock2 = self.main_window.mix_wieght_target_rock_2_lineEdit.text()
        if current_rock2 != str(self.display_target_rock2):
            self.main_window.mix_wieght_target_rock_2_lineEdit.setText(str(self.display_target_rock2))
        
        current_cement = self.main_window.mix_wieght_target_cement_lineEdit.text()
        if current_cement != str(self.display_target_cement):
            self.main_window.mix_wieght_target_cement_lineEdit.setText(str(self.display_target_cement))
        
        current_fyash = self.main_window.mix_wieght_target_fyash_lineEdit.text()
        if current_fyash != str(self.display_target_fyash):
            self.main_window.mix_wieght_target_fyash_lineEdit.setText(str(self.display_target_fyash))
        
        current_water = self.main_window.mix_wieght_target_water_lineEdit.text()
        if current_water != str(self.display_target_water):
            self.main_window.mix_wieght_target_water_lineEdit.setText(str(self.display_target_water))
        
        current_chem1 = self.main_window.mix_wieght_target_chem_1_lineEdit.text()
        if current_chem1 != str(self.display_target_chem1):
            self.main_window.mix_wieght_target_chem_1_lineEdit.setText(str(self.display_target_chem1))
        
        current_chem2 = self.main_window.mix_wieght_target_chem_2_lineEdit.text()
        if current_chem2 != str(self.display_target_chem2):
            self.main_window.mix_wieght_target_chem_2_lineEdit.setText(str(self.display_target_chem2))
    
    def main_condition_load(self):
        while self.main_condition_load_running:
            try:
                if self.state_main_condition_load == 0:
                    # รอให้วัตถุดิบทั้ง 4 ประเภทโหลดเสร็จ
                    if self.next_queue_loaded_and_ready:
                        self.next_queue_loaded_and_ready = False  # รีเซ็ต flag
                        self.current_queue_transporting += 1
                        self.state_main_condition_load = 1
                    else:
                        pass
                    
                elif self.state_main_condition_load == 1:
                    
                    # อัพเดตจำนวนคิวที่กำลังผสม (ใช้ multiplier ของคิวปัจจุบัน)
                    current_queue_index = self.current_queue_transporting - 1
                    if current_queue_index < len(self.queue_multipliers):
                        current_mixing_amount = self.queue_multipliers[current_queue_index]
                        # อัพเดตช่องที่กำลังผสม
                        self.main_window.mix_result_mix_lineEdit.setText(str(current_mixing_amount))
                    
                    self.plc_controller.converyer_top("start")
                    self.plc_controller.mixer("start")
                    time.sleep(3)
                    time.sleep(int(self.converyer_time))
                    self.plc_controller.converyer_midle("start")
                    self.state_main_condition_load = 2
                    
                elif self.state_main_condition_load == 2:
                    self.plc_controller.vibrater_cement_and_fyash("start")
                    time.sleep(1)
                    self.plc_controller.vale_water("start")
                    time.sleep(int(self.cement_release_time))
                    self.plc_controller.vale_cement_and_fyash("start")
                    time.sleep(3)
                    self.plc_controller.pump_chemical_up("start")
                    time.sleep(1)
                    self.state_main_condition_load = 3
                    
                elif self.state_main_condition_load == 3:
                    for i in range(10):
                        pass
                    self.plc_controller.converyer_midle("stop")
                    time.sleep(1)
                    self.plc_controller.converyer_top("stop")
                    time.sleep(1)
                    self.plc_controller.vale_water("stop")
                    time.sleep(1)
                    self.plc_controller.vale_cement_and_fyash("stop")
                    time.sleep(1)
                    self.plc_controller.vibrater_cement_and_fyash("stop")
                    time.sleep(1)
                    self.plc_controller.pump_chemical_up("stop")
                    time.sleep(1)
                    # เรียก start_next_load_ready เพื่อเริ่มโหลดคิวถัดไป (ขณะที่กระบวนการผสมยังทำงานอยู่)
                    self.start_next_load_ready()
                    self.state_main_condition_load = 4  # ไปต่อกระบวนการผสม
                
                elif self.state_main_condition_load == 4:
                    for i in range(int(self.mixer_start_time)-17):
                        time.sleep(1)
                    self.plc_controller.vale_mixer("start")
                    time.sleep(5)
                    self.plc_controller.vale_mixer("stop")
                    time.sleep(5)
                    self.plc_controller.vale_mixer("start")
                    time.sleep(5)
                    self.plc_controller.vale_mixer("stop")
                    self.state_main_condition_load = 5
                    
                elif self.state_main_condition_load == 5:
                    for i in range(15):
                        time.sleep(1)
                    # ตรวจสอบว่ามีคิวรอโหลดอยู่หรือไม่
                    has_more_queues = (self.next_queue_loaded_and_ready or 
                                      self.current_queue_transporting < self.total_queue_count)
                    
                    if not has_more_queues:
                        # ไม่มีคิวรออีกแล้ว ปิด mixer ตามปกติ
                        self.plc_controller.mixer("stop")
                        time.sleep(1)
                    else:
                        pass  # Keep mixer running
                    
                    # สะสมน้ำหนักจาก batch ปัจจุบันเข้าไปใน TempMixer (ก่อนไป batch ถัดไป)
                    self._accumulate_batch_weights()
                    
                    # อัพเดตจำนวนคิวที่ผสมเสร็จแล้ว
                    current_queue_index = self.current_queue_transporting - 1
                    if current_queue_index < len(self.queue_multipliers):
                        completed_amount = self.queue_multipliers[current_queue_index]
                        self.completed_queue_count += completed_amount
                        self._update_queue_display()
                    
                    # ตรวจสอบว่ามีคิวถัดไปที่โหลดเสร็จและพร้อมลำเลียงหรือไม่
                    if self.next_queue_loaded_and_ready:
                        # มีคิวถัดไปพร้อมแล้ว เริ่มลำเลียงทันที
                        self.state_main_condition_load = 0  # กลับไป state 0 เพื่อเริ่มลำเลียงคิวถัดไป
                    elif self.current_queue_transporting < self.total_queue_count:
                        # ยังมีคิวที่ต้องลำเลียงอีก แต่ยังโหลดไม่เสร็จ รอที่ state 6
                        self.state_main_condition_load = 6
                    else:
                        # ไม่มีคิวเหลือแล้ว จบกระบวนการ
                        self.lock_target_display = False  # ปลดล็อค Target
                        self._stop_target_monitor()  # หยุด monitor
                        self.main_condition_load_running = False
                        self.state_main_condition_load = 0
                        
                        # อัพเดต database ด้วยน้ำหนักจริงที่โหลดได้
                        self._update_database_after_loading()
                        
                        # รีเซ็ตค่าทั้งหมดเพื่อเตรียมพร้อมสำหรับลูกค้ารายใหม่
                        self._reset_all_for_new_customer()
                        
                elif self.state_main_condition_load == 6:
                    # State รอคิวถัดไปโหลดเสร็จ
                    if self.next_queue_loaded_and_ready:
                        # คิวถัดไปโหลดเสร็จแล้ว เริ่มลำเลียงได้
                        self.state_main_condition_load = 0  # กลับไป state 0 เพื่อเริ่มลำเลียงคิวถัดไป
                    else:
                        pass
                    
            except Exception as e:
                print(f"Error in main condition load: {e}")
            time.sleep(1)
            
    def _update_queue_display(self):
        self.main_window.mix_result_mix_success_lineEdit.setText(str(round(self.completed_queue_count, 1)))
        self.main_window.mix_result_mix_lineEdit.setText("0")
    
    def load_rock_and_sand_sequence(self,data_loaded):
        rock_1, sand_real, rock_2 = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_rock1 = rock_1
        original_sand = sand_real
        original_rock2 = rock_2
        
        try:
            current_weight = int(self.main_window.mix_monitor_rock_1_lineEdit.text())
        except:
            current_weight = 0
        
        # คำนวณ setpoint (หักลบ offset)
        rock_1 = int(rock_1) - int(self.rock1_offset)
        sand = ((int(sand_real)+int(rock_1)) - int(self.sand_offset)) + int(self.rock1_offset) 
        rock_2 = ((int(rock_2)+int(sand_real)+int(rock_1)) - int(self.rock2_offset)) + int(self.sand_offset) + int(self.rock1_offset)
        
        if current_weight > 0:
            rock_1 += current_weight
            sand += current_weight
            rock_2 += current_weight
        
        self.target_rock1_weight = rock_1
        self.target_sand_total_weight = sand
        self.target_rock2_total_weight = rock_2
        
        print(f"🎯 Rock and Sand Loading Targets:")
        print(f"   Original: Rock1={original_rock1}, Sand={original_sand}, Rock2={original_rock2}")
        print(f"   Setpoint: Rock1={rock_1}, Sand={sand}, Rock2={rock_2}")
        
        while self.is_loading_rock_and_sand_in_progress:
            if self.state_load_rock_and_sand == 0:
                pass
            elif self.state_load_rock_and_sand == 1:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_rock1 <= 0:
                    print(f"⏭️ Skip Rock1 (target = {original_rock1})")
                    self.is_rock1_frozen = True
                    self.rock1_frozen_weight = current_weight
                    self.state_load_rock_and_sand = 3
                else:
                    print(f"🪨 Loading Rock1 to {rock_1} kg")
                    self.autoda_controller.write_set_point_rock_and_sand(rock_1)
                    self.plc_controller.loading_rock1("start")
                    self.state_load_rock_and_sand = 2
                
            elif self.state_load_rock_and_sand == 2:
                if self.is_rock1_frozen:
                    self.plc_controller.loading_rock1("stop")
                    # เช็คว่า Sand ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_sand > 0:
                        self.autoda_controller.write_set_point_rock_and_sand(sand)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 3
                    
            elif self.state_load_rock_and_sand == 3:
                self.plc_controller.loading_rock1("stop")
                time.sleep(1)
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_sand <= 0:
                    print(f"⏭️ Skip Sand (target = {original_sand})")
                    self.is_sand_frozen = True
                    self.sand_frozen_weight = current_weight if current_weight > 0 else self.rock1_frozen_weight
                    self.sand_only_frozen = 0  # Sand ถูก skip
                    # เช็คว่า Rock2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_rock2 > 0:
                        self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
                else:
                    print(f"🏖️ Loading Sand to {sand} kg")
                    self.plc_controller.loading_sand("start")
                    self.state_load_rock_and_sand = 4
            
            elif self.state_load_rock_and_sand == 4:
                if self.is_sand_frozen:
                    self.plc_controller.loading_sand("stop")
                    # เช็คว่า Rock2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    if original_rock2 > 0:
                        self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
            
            elif self.state_load_rock_and_sand == 5:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_rock2 <= 0:
                    print(f"⏭️ Skip Rock2 (target = {original_rock2})")
                    self.is_rock2_frozen = True
                    self.rock2_frozen_weight = current_weight if current_weight > 0 else self.sand_frozen_weight
                    self.rock2_only_frozen = 0  # Rock2 ถูก skip
                    self.state_load_rock_and_sand = 0
                    self.rock_and_sand_loading_success = True
                    self.is_loading_rock_and_sand_in_progress = False
                else:
                    print(f"🪨 Loading Rock2 to {rock_2} kg")
                    self.plc_controller.loading_rock2("start")
                    time.sleep(0.5)
                    self.plc_controller.loading_rock1("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_sand("stop")
                    self.state_load_rock_and_sand = 6
            
            elif self.state_load_rock_and_sand == 6:
                if self.is_rock2_frozen:
                    self.plc_controller.loading_rock2("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_rock1("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_sand("stop")
                    self.state_load_rock_and_sand = 0
                    self.rock_and_sand_loading_success = True
                    self.is_loading_rock_and_sand_in_progress = False
            time.sleep(0.1)
    
    def load_cement_and_fyash_sequence(self,data_loaded):
        cement, fyash = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_cement = cement
        original_fyash = fyash
        
        try:
            current_weight = int(self.main_window.mix_monitor_cement_lineEdit.text())
        except:
            current_weight = 0
        
        # คำนวณ setpoint (หักลบ offset)
        cement = int(cement) - int(self.cement_offset)
        fyash = ((int(fyash)+int(cement)) - int(self.fyash_offset)) + int(self.cement_offset)
        
        if current_weight > 0:
            cement += current_weight
            fyash += current_weight
        
        self.target_cement_weight = cement
        self.target_fyash_total_weight = fyash
        
        print(f"🎯 Cement and Flyash Loading Targets:")
        print(f"   Original: Cement={original_cement}, Flyash={original_fyash}")
        print(f"   Setpoint: Cement={cement}, Flyash={fyash}")
        
        while self.is_loading_cement_and_fyash_in_progress:
            if self.state_load_cement_and_fyash == 0:
                pass
            elif self.state_load_cement_and_fyash == 1:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_cement <= 0:
                    print(f"⏭️ Skip Cement (target = {original_cement})")
                    self.is_cement_frozen = True
                    self.cement_frozen_weight = current_weight
                    self.state_load_cement_and_fyash = 3
                else:
                    print(f"🏗️ Loading Cement to {cement} kg")
                    # self.autoda_controller.write_set_point_cement_and_fyash(cement)
                    self.plc_controller.loading_cement("start")
                    self.state_load_cement_and_fyash = 2
            elif self.state_load_cement_and_fyash == 2:
                if self.is_cement_frozen:
                    self.plc_controller.loading_cement("stop")
                    # เช็คว่า Flyash ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    # if original_fyash > 0:
                    #     self.autoda_controller.write_set_point_cement_and_fyash(fyash)
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 3
            elif self.state_load_cement_and_fyash == 3:
                self.plc_controller.loading_cement("stop")
                time.sleep(0.5)
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_fyash <= 0:
                    print(f"⏭️ Skip Flyash (target = {original_fyash})")
                    self.is_fyash_frozen = True
                    self.fyash_frozen_weight = current_weight if current_weight > 0 else self.cement_frozen_weight
                    self.fyash_only_frozen = 0  # Flyash ถูก skip
                    self.state_load_cement_and_fyash = 0
                    self.cement_and_fyash_loading_success = True
                    self.is_loading_cement_and_fyash_in_progress = False
                else:
                    print(f"🌫️ Loading Flyash to {fyash} kg")
                    self.plc_controller.loading_flyash("start")
                    self.state_load_cement_and_fyash = 4
            elif self.state_load_cement_and_fyash == 4:
                if self.is_fyash_frozen:
                    self.plc_controller.loading_flyash("stop")
                    time.sleep(0.5)
                    self.plc_controller.loading_cement("stop")
                    self.state_load_cement_and_fyash = 0
                    self.cement_and_fyash_loading_success = True
                    self.is_loading_cement_and_fyash_in_progress = False
            time.sleep(0.1)

    def loading_water_sequence(self,data_loaded):
        water = data_loaded
        
        # เก็บค่าต้นฉบับก่อนคำนวณ setpoint
        original_water = water
        
        try:
            current_weight = int(self.main_window.mix_monitor_water_lineEdit.text())
        except:
            current_weight = 0
        
        # คำนวณ setpoint (หักลบ offset)
        water = int(water) - int(self.water_offset)
        
        if current_weight > 0:
            water += current_weight
        
        self.target_water_weight = water
        
        print(f"🎯 Water Loading Target:")
        print(f"   Original: Water={original_water}")
        print(f"   Setpoint: Water={water}")
        
        while self.is_loading_water_in_progress:
            if self.state_load_water == 0:
                pass
            elif self.state_load_water == 1:
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_water <= 0:
                    print(f"⏭️ Skip Water (target = {original_water})")
                    self.is_water_frozen = True
                    self.water_frozen_weight = current_weight
                    self.state_load_water = 0
                    self.water_loading_success = True
                    self.is_loading_water_in_progress = False
                else:
                    print(f"💧 Loading Water to {water} kg")
                    # self.autoda_controller.write_set_point_water(water)
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
        
        try:
            current_weight = float(self.main_window.mix_monitor_chem_1_lineEdit.text())
        except:
            current_weight = 0.0
        
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
        
        print(f"🎯 Chemical Loading Targets:")
        print(f"   Original: Chem1={original_chem1}, Chem2={original_chem2}")
        print(f"   Setpoint: Chem1={chem1}, Chem2={chem2}")
            
        if original_chem1 <= 0 and original_chem2 <= 0:
            print(f"⏭️ Skip All Chemicals (Chem1={original_chem1}, Chem2={original_chem2})")
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
                    print(f"⏭️ Skip Chem1 (target = {original_chem1})")
                    self.is_chem1_frozen = True
                    self.chem1_frozen_weight = current_weight
                    self.state_load_chemical = 3
                else:
                    print(f"🧪 Loading Chem1 to {chem1} kg")
                    # self.autoda_controller.write_set_point_chemical(chem1)
                    time.sleep(0.5)
                    self.plc_controller.loading_chemical_1("start")
                    time.sleep(0.5)
                    self.state_load_chemical = 2
            elif self.state_load_chemical == 2:
                if self.is_chem1_frozen:
                    self.plc_controller.loading_chemical_1("stop")
                    # เช็คว่า Chem2 ต้องโหลดหรือไม่ก่อนเซ็ต setpoint
                    # if original_chem2 > 0:
                    #     self.autoda_controller.write_set_point_chemical(chem2)
                    time.sleep(0.5)
                    self.state_load_chemical = 3
            elif self.state_load_chemical == 3:
                self.plc_controller.loading_chemical_1("stop")
                time.sleep(0.5)
                # เช็คจากค่าต้นฉบับ ไม่ใช่ค่า setpoint
                if original_chem2 <= 0:
                    print(f"⏭️ Skip Chem2 (target = {original_chem2})")
                    self.is_chem2_frozen = True
                    self.chem2_frozen_weight = current_weight if current_weight > 0 else self.chem1_frozen_weight
                    self.chem2_only_frozen = 0  # Chem2 ถูก skip
                    self.state_load_chemical = 0
                    self.chemical_loading_success = True
                    self.is_loading_chemical_in_progress = False
                else:
                    print(f"🧪 Loading Chem2 to {chem2} kg")
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
        self.reset_freeze_values()
        self.lock_target_display = False  # ปลดล็อค Target UI เมื่อยกเลิก
        self._stop_target_monitor()  # หยุด monitor
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
    
    def _accumulate_batch_weights(self):
        """สะสมน้ำหนักจริงที่โหลดได้จาก batch ปัจจุบันเข้าไปใน TempMixer"""
        try:
            current_mixer = self.load_work_queue.current_mixer
            if not current_mixer:
                print("⚠️ Warning: No current_mixer for weight accumulation")
                return
            
            # สะสมน้ำหนักจาก frozen weights ของ batch ปัจจุบัน
            # Rock1
            rock1_this_batch = getattr(self, 'rock1_frozen_weight', 0)
            current_mixer.rock1_total_weight += rock1_this_batch
            
            # Sand (only sand, not total)
            sand_this_batch = getattr(self, 'sand_only_frozen', 0)
            current_mixer.sand_total_weight += sand_this_batch
            
            # Rock2 (only rock2, not total)
            rock2_this_batch = getattr(self, 'rock2_only_frozen', 0)
            current_mixer.rock2_total_weight += rock2_this_batch
            
            # Cement
            cement_this_batch = getattr(self, 'cement_frozen_weight', 0)
            current_mixer.cement_total_weight += cement_this_batch
            
            # Flyash (only flyash, not total)
            flyash_this_batch = getattr(self, 'fyash_only_frozen', 0)
            current_mixer.fly_ash_total_weight += flyash_this_batch
            
            # Water
            water_this_batch = getattr(self, 'water_frozen_weight', 0)
            current_mixer.water_total_weight += water_this_batch
            
            # Chem1
            chem1_this_batch = getattr(self, 'chem1_frozen_weight', 0)
            current_mixer.chem1_total_weight += chem1_this_batch
            
            # Chem2 (only chem2, not total)
            chem2_this_batch = getattr(self, 'chem2_only_frozen', 0)
            current_mixer.chem2_total_weight += chem2_this_batch
            
            print("=" * 70)
            print(f"📊 Batch #{self.current_queue_transporting} weights accumulated:")
            print(f"   Rock1: +{rock1_this_batch} kg → Total: {current_mixer.rock1_total_weight} kg")
            print(f"   Sand: +{sand_this_batch} kg → Total: {current_mixer.sand_total_weight} kg")
            print(f"   Rock2: +{rock2_this_batch} kg → Total: {current_mixer.rock2_total_weight} kg")
            print(f"   Cement: +{cement_this_batch} kg → Total: {current_mixer.cement_total_weight} kg")
            print(f"   Flyash: +{flyash_this_batch} kg → Total: {current_mixer.fly_ash_total_weight} kg")
            print(f"   Water: +{water_this_batch} kg → Total: {current_mixer.water_total_weight} kg")
            print(f"   Chem1: +{chem1_this_batch} kg → Total: {current_mixer.chem1_total_weight} kg")
            print(f"   Chem2: +{chem2_this_batch} kg → Total: {current_mixer.chem2_total_weight} kg")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ Error accumulating batch weights: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_database_after_loading(self):
        """อัพเดต database ด้วยน้ำหนักจริงที่โหลดได้และตั้ง Status_load = 1"""
        print("=" * 60)
        print("🔄 Starting database update after loading...")
        print("=" * 60)
        
        try:
            # ดึง order_id จาก load_work_queue
            order_id = self.load_work_queue.get_current_order_id()
            print(f"📌 Order ID: {order_id}")
            
            if not order_id:
                print("⚠️ Warning: No order_id found, cannot update database")
                return
            
            # ดึงข้อมูล TempMixer ปัจจุบัน (ที่สะสมน้ำหนักมาแล้ว)
            current_mixer = self.load_work_queue.current_mixer
            print(f"📦 Current Mixer: {current_mixer}")
            
            if not current_mixer:
                print("⚠️ Warning: No current_mixer found, cannot update database")
                return
            
            # แสดงน้ำหนักรวมที่สะสมได้ทั้งหมด (จากทุกรอบ batch)
            print("\n📊 Total accumulated weights from all batches:")
            print(f"   Rock1: {current_mixer.rock1_total_weight} kg")
            print(f"   Sand: {current_mixer.sand_total_weight} kg")
            print(f"   Rock2: {current_mixer.rock2_total_weight} kg")
            print(f"   Cement: {current_mixer.cement_total_weight} kg")
            print(f"   Flyash: {current_mixer.fly_ash_total_weight} kg")
            print(f"   Water: {current_mixer.water_total_weight} kg")
            print(f"   Chem1: {current_mixer.chem1_total_weight} kg")
            print(f"   Chem2: {current_mixer.chem2_total_weight} kg")
            
            # ตรวจสอบว่ามี order_inserter หรือไม่
            if not hasattr(self.load_work_queue, 'order_inserter'):
                print("❌ Error: load_work_queue does not have order_inserter!")
                return
            
            print(f"\n💾 Calling update_complete() with order_id={order_id}")
            # เรียกใช้ update_complete เพื่ออัพเดต database
            success = self.load_work_queue.order_inserter.update_complete(order_id, current_mixer)
            
            if success:
                print(f"✅ Database updated successfully!")
                print(f"   Status_load: 1 (Completed)")
            else:
                print(f"❌ Failed to update database for order_id: {order_id}")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            import traceback
            traceback.print_exc()
        
        print("=" * 60)
    
    def _reset_all_for_new_customer(self):
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
        self.main_window.mix_result_mix_lineEdit.setText("0")
        self.main_window.mix_result_mix_success_lineEdit.setText("0")
        self.main_window.mix_monitor_rock_1_lineEdit.setText("0")
        self.main_window.mix_monitor_sand_lineEdit.setText("0")
        self.main_window.mix_monitor_rock_2_lineEdit.setText("0")
        self.main_window.mix_monitor_cement_lineEdit.setText("0")
        self.main_window.mix_monitor_fyash_lineEdit.setText("0")
        self.main_window.mix_monitor_water_lineEdit.setText("0")
        self.main_window.mix_monitor_chem_1_lineEdit.setText("0")
        self.main_window.mix_monitor_chem_2_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_rock_1_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_sand_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_rock_2_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_cement_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_fyash_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_water_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_chem_1_lineEdit.setText("0")
        self.main_window.mix_wieght_Loaded_chem_2_lineEdit.setText("0")
        total_cubes = self.get_all_loaded_cube
        self.work_completed.emit(total_cubes)
    
    @Slot(float)
    def _show_completion_message(self, total_cubes):
        """แสดง MessageBox แจ้งเตือนว่างานเสร็จและกลับไปหน้า Work Tab"""
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
        QApplication.beep()
        result = msg_box.exec()
        if result == QMessageBox.Ok:
            self.main_window.tab.setCurrentWidget(self.main_window.work_tab)
            # print("📋 Switched to Work Tab - Ready for new customer")


