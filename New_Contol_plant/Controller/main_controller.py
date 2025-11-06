from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject, Qt, QTimer
from PySide6.QtWidgets import QFileDialog,QMessageBox,QTreeWidgetItem,QApplication
from threading import Thread
import time
import sys
from datetime import datetime
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
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()

        self.db = C_palne_Database()
        # self.plc_controller = PLC_Controller()
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
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Cement and Fyash
        self.cement_frozen_weight = 0
        self.fyash_frozen_weight = 0
        self.fyash_only_frozen = 0
        self.is_cement_frozen = False
        self.is_fyash_frozen = False
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Water
        self.water_frozen_weight = 0
        self.is_water_frozen = False
        
        # ตัวแปรสำหรับ freeze น้ำหนักแต่ละวัสดุ - Chemical
        self.chem1_frozen_weight = 0
        self.chem2_frozen_weight = 0
        self.chem2_only_frozen = 0
        self.is_chem1_frozen = False
        self.is_chem2_frozen = False
        
        # ตัวแปรเป้าหมายน้ำหนัก
        self.target_rock1_weight = 0
        self.target_sand_total_weight = 0
        self.target_rock2_total_weight = 0
        self.target_cement_weight = 0
        self.target_fyash_total_weight = 0
        self.target_water_weight = 0
        self.target_chem1_weight = 0
        self.target_chem2_total_weight = 0
        
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
        if (hasattr(self, 'target_rock1_weight') and 
            current_weight >= self.target_rock1_weight and 
            not self.is_rock1_frozen):
            self.rock1_frozen_weight = current_weight
            self.is_rock1_frozen = True
        if (hasattr(self, 'target_sand_total_weight') and 
            current_weight >= self.target_sand_total_weight and 
            not self.is_sand_frozen):
            self.sand_frozen_weight = current_weight
            self.sand_only_frozen = max(0, current_weight - self.rock1_frozen_weight if self.is_rock1_frozen else current_weight)
            self.is_sand_frozen = True
        if (hasattr(self, 'target_rock2_total_weight') and 
            current_weight >= self.target_rock2_total_weight and 
            not self.is_rock2_frozen):
            self.rock2_frozen_weight = current_weight
            self.rock2_only_frozen = max(0, current_weight - self.sand_frozen_weight if self.is_sand_frozen else 0)
            self.is_rock2_frozen = True

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
        # Check cement freeze
        if (hasattr(self, 'target_cement_weight') and 
            current_weight >= self.target_cement_weight and 
            not getattr(self, 'is_cement_frozen', False)):
            self.cement_frozen_weight = current_weight
            self.is_cement_frozen = True

        # Check fyash freeze
        if (hasattr(self, 'target_fyash_total_weight') and 
            current_weight >= self.target_fyash_total_weight and 
            not getattr(self, 'is_fyash_frozen', False)):
            self.fyash_frozen_weight = current_weight
            cement_frozen = getattr(self, 'cement_frozen_weight', 0)
            self.fyash_only_frozen = max(0, current_weight - cement_frozen if getattr(self, 'is_cement_frozen', False) else current_weight)
            self.is_fyash_frozen = True

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
        if (hasattr(self, 'target_water_weight') and 
            current_weight >= self.target_water_weight and 
            not getattr(self, 'is_water_frozen', False)):
            self.water_frozen_weight = current_weight
            self.is_water_frozen = True

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
        if (hasattr(self, 'target_chem1_weight') and 
            current_weight >= self.target_chem1_weight and 
            not getattr(self, 'is_chem1_frozen', False)):
            self.chem1_frozen_weight = current_weight
            self.is_chem1_frozen = True
        if (hasattr(self, 'target_chem2_total_weight') and 
            current_weight >= self.target_chem2_total_weight and 
            not getattr(self, 'is_chem2_frozen', False)):
            self.chem2_frozen_weight = current_weight
            chem1_frozen = getattr(self, 'chem1_frozen_weight', 0)
            self.chem2_only_frozen = max(0, current_weight - chem1_frozen if getattr(self, 'is_chem1_frozen', False) else current_weight)
            self.is_chem2_frozen = True

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
        else:
            pass

    def mix_start_load(self):
        self.reset_freeze_values()
        self.rock1, self.sand, self.rock2, self.cement, self.fyash, self.water, self.chem1, self.chem2 = self.main_window.get_data_formular_in_mix_form()
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
        
        print("Started loading sequence.")
        self.main_condition_load_running = True
        self.thread_main_condition_load = Thread(target=self.main_condition_load)
        self.thread_main_condition_load.start()
        

    def main_condition_load(self):
        while self.main_condition_load_running:
            try:
                if self.state_main_condition_load == 0:
                    if self.rock_and_sand_success_start_main == True and self.cement_and_fyash_success_start_main == True and self.water_success_start_main == True and self.chemical_success_start_main == True:
                        self.state_main_condition_load = 1
                    else:
                        pass
                    
                elif self.state_main_condition_load == 1:
                    print("All loading sequences completed successfully.")
                    self.plc_controller.converyer_top("start")
                    self.plc_controller.mixer("start")
                    time.sleep(3)
                    time.sleep(int(self.converyer_time))
                    self.plc_controller.converyer_midle("start")
                    self.state_main_condition_load = 2
                    
                elif self.state_main_condition_load == 2:
                    self.plc_controller.vibrater_cement_and_fyash("start")
                    time.sleep(5)
                    self.plc_controller.vale_water("start")
                    time.sleep(int(self.cement_release_time))
                    self.plc_controller.vale_cement_and_fyash("start")
                    time.sleep(3)
                    self.state_main_condition_load = 3
                    
                elif self.state_main_condition_load == 3:
                    for i in range(10):
                        pass
                    self.plc_controller.vibrater_cement_and_fyash("stop")
                    time.sleep(1)
                    self.plc_controller.converyer_midle("stop")
                    time.sleep(1)
                    self.plc_controller.converyer_top("stop")
                    time.sleep(1)
                    self.plc_controller.vale_water("stop")
                    time.sleep(1)
                    self.plc_controller.vale_cement_and_fyash("stop")
                    self.state_main_condition_load = 4
                
                elif self.state_main_condition_load == 4:
                    for i in range(int(self.mixer_start_time)-13):
                        pass
                    self.plc_controller.vale_mixer("start")
                    time.sleep(5)
                    self.plc_controller.mixer("stop")
                    time.sleep(5)
                    self.plc_controller.vale_mixer("start")
                    time.sleep(5)
                    self.plc_controller.vale_mixer("stop")
                    self.state_main_condition_load = 5
                    
                elif self.state_main_condition_load == 5:
                    self.plc_controller.mixer("stop")
                    time.sleep(1)
                    self.state_main_condition_load = 6
                
                elif self.state_main_condition_load == 6:
                    print("Mixing process completed.")
                    
                print(self.state_main_condition_load)
            except Exception as e:
                print(f"Error in main condition load: {e}")
            time.sleep(1)

    def load_rock_and_sand_sequence(self,data_loaded):
        rock_1, sand_real, rock_2 = data_loaded
        rock_1 = int(rock_1) - int(self.rock1_offset)
        sand = ((int(sand_real)+int(rock_1)) - int(self.sand_offset)) + int(self.rock1_offset) 
        rock_2 = ((int(rock_2)+int(sand_real)+int(rock_1)) - int(self.rock2_offset)) + int(self.sand_offset) + int(self.rock1_offset)
        self.target_rock1_weight = rock_1
        self.target_sand_total_weight = sand
        self.target_rock2_total_weight = rock_2
        while self.is_loading_rock_and_sand_in_progress:
            if self.state_load_rock_and_sand == 0:
                pass
            elif self.state_load_rock_and_sand == 1:
                self.autoda_controller.write_set_point_rock_and_sand(rock_1)
                self.plc_controller.loading_rock1("start")
                self.state_load_rock_and_sand = 2
                
            elif self.state_load_rock_and_sand == 2:
                if self.is_rock1_frozen:
                    self.plc_controller.loading_rock1("stop")
                    self.autoda_controller.write_set_point_rock_and_sand(sand)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 3
                    
            elif self.state_load_rock_and_sand == 3:
                self.plc_controller.loading_rock1("stop")
                time.sleep(1)
                self.plc_controller.loading_sand("start")
                self.state_load_rock_and_sand = 4
            
            elif self.state_load_rock_and_sand == 4:
                if self.is_sand_frozen:
                    self.plc_controller.loading_sand("stop")
                    self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
            
            elif self.state_load_rock_and_sand == 5:
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
        cement = int(cement) - int(self.cement_offset)
        fyash = ((int(fyash)+int(cement)) - int(self.fyash_offset)) + int(self.cement_offset)
        self.target_cement_weight = cement
        self.target_fyash_total_weight = fyash
        while self.is_loading_cement_and_fyash_in_progress:
            if self.state_load_cement_and_fyash == 0:
                pass
            elif self.state_load_cement_and_fyash == 1:
                self.autoda_controller.write_set_point_cement_and_fyash(cement)
                self.plc_controller.loading_cement("start")
                self.state_load_cement_and_fyash = 2
            elif self.state_load_cement_and_fyash == 2:
                if self.is_cement_frozen:
                    self.plc_controller.loading_cement("stop")
                    self.autoda_controller.write_set_point_cement_and_fyash(fyash)
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 3
            elif self.state_load_cement_and_fyash == 3:
                self.plc_controller.loading_cement("stop")
                time.sleep(0.5)
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
        water = int(water) - int(self.water_offset)
        self.target_water_weight = water
        while self.is_loading_water_in_progress:
            if self.state_load_water == 0:
                pass
            elif self.state_load_water == 1:
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
        chem1 = float(chem1) - float(self.chem1_offset)
        chem2 = ((float(chem2)+float(chem1)) - float(self.chem2_offset)) + float(self.chem1_offset)
        chem1 = round(chem1, 1)
        chem2 = round(chem2, 1)
        self.target_chem1_weight = chem1
        self.target_chem2_total_weight = chem2
        while self.is_loading_chemical_in_progress:
            if self.state_load_chemical == 0:
                pass
            elif self.state_load_chemical == 1:
                self.autoda_controller.write_set_point_chemical(chem1)
                time.sleep(0.5)
                self.plc_controller.loading_chemical_1("start")
                time.sleep(0.5)
                self.state_load_chemical = 2
            elif self.state_load_chemical == 2:
                if self.is_chem1_frozen:
                    self.plc_controller.loading_chemical_1("stop")
                    self.autoda_controller.write_set_point_chemical(chem2)
                    time.sleep(0.5)
                    self.state_load_chemical = 3
            elif self.state_load_chemical == 3:
                self.plc_controller.loading_chemical_1("stop")
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
        self.reset_freeze_values()
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
        print("Loading cancelled and freeze values reset")

    def Show_main(self):
        self.main_window.Show()

    def reset_freeze_values(self):
        # Rock and Sand
        self.rock1_frozen_weight = 0
        self.sand_frozen_weight = 0
        self.rock2_frozen_weight = 0
        self.sand_only_frozen = 0
        self.rock2_only_frozen = 0
        self.is_rock1_frozen = False
        self.is_sand_frozen = False
        self.is_rock2_frozen = False
        # Cement and Fyash
        self.cement_frozen_weight = 0
        self.fyash_frozen_weight = 0
        self.fyash_only_frozen = 0
        self.is_cement_frozen = False
        self.is_fyash_frozen = False
        # Water
        self.water_frozen_weight = 0
        self.is_water_frozen = False
        # Chemical
        self.chem1_frozen_weight = 0
        self.chem2_frozen_weight = 0
        self.chem2_only_frozen = 0
        self.is_chem1_frozen = False
        self.is_chem2_frozen = False
    
    def get_freeze_status(self):
        return {
            'rock1': {'frozen': self.is_rock1_frozen, 'weight_total': self.rock1_frozen_weight, 'weight_only': self.rock1_frozen_weight},
            'sand': {'frozen': self.is_sand_frozen, 'weight_total': self.sand_frozen_weight, 'weight_only': getattr(self, 'sand_only_frozen', 0)},
            'rock2': {'frozen': self.is_rock2_frozen, 'weight_total': self.rock2_frozen_weight, 'weight_only': getattr(self, 'rock2_only_frozen', 0)},
            'current_state': self.state_load_rock_and_sand
        }


