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

        # Loading control variables
        # ROCK AND SAND STATE
        self.rock_and_sand_values = []
        self.is_loading_rock_and_sand_in_progress = False
        self.thread_rock_and_sand = None
        self.state_load_rock_and_sand = 0
        self.rock_and_sand_loadding_success = False
        self.rock_success = False
        # ROCK AND SAND STATE
        # CEMENT AND FYASH STATE
        self.cement_and_fyash_values = []
        self.is_loading_cement_and_fyash_in_progress = False
        self.thread_cement_and_fyash = None
        self.state_load_cement_and_fyash = 0
        self.cement_and_fyash_loading_success = False
        # CEMENT AND FYASH STATE
        # WATER STATE
        self.water_value = []
        self.is_loading_water_in_progress = False
        self.thread_water = None
        self.state_load_water = 0
        self.water_loading_success = False
        # WATER STATE

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

        # debug tab
        self.debug_tab = debug_tab(self.main_window)
        
        # mix control tab
        self.plc_controller = PLC_Controller(self.main_window, self.db)
        self.plc_controller.comport_error.connect(self.update_status_port)
        self.plc_controller.status_loading_rock_and_sand.connect(self.check_loading_rock_and_sand)
        self.plc_controller.status_loading_cement_and_fyash.connect(self.check_loading_cement_and_fyash)
        self.plc_controller.initialize_connections()
        self.plc_controller.start()

        self.autoda_controller = AUTODA_Controller(self.main_window, self.db)
        self.autoda_controller.comport_error.connect(self.update_status_port)
        self.autoda_controller.weight_rock_and_sand.connect(self.update_weight_rock_and_sand)
        self.autoda_controller.weight_cement_and_fyash.connect(self.update_weight_cement_and_fyash)
        self.autoda_controller.weight_water.connect(self.update_weight_water)
        self.autoda_controller.weight_chemical.connect(self.update_weight_chemical)

        self.autoda_controller.initialize_connections()
        self.autoda_controller.start()

        self.main_window.mix_start_load_pushButton.clicked.connect(self.mix_start_load)
        self.main_window.mix_cancel_load_pushButton.clicked.connect(self.mix_cancel_load)

        self.main_window.set_readonly_mix_weights()
        

        


    @Slot(list)
    @Slot(int)
    


    def update_weight_rock_and_sand(self, weight):
        self.main_window.mix_monitor_rock_1_lineEdit.setText(str(weight))
        self.main_window.mix_monitor_rock_2_lineEdit.setText(str(weight))
        self.main_window.mix_monitor_sand_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_rock_1_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_rock_2_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_sand_lineEdit.setText(str(weight))

    def update_weight_cement_and_fyash(self, weight):
        self.main_window.mix_monitor_cement_lineEdit.setText(str(weight))
        self.main_window.mix_monitor_fyash_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_cement_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_fyash_lineEdit.setText(str(weight))

    def update_weight_water(self, weight):
        self.main_window.mix_monitor_water_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_water_lineEdit.setText(str(weight))

    def update_weight_chemical(self, weight):
        self.main_window.mix_monitor_chem_1_lineEdit.setText(str(weight))
        self.main_window.mix_monitor_chem_2_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_chem_1_lineEdit.setText(str(weight))
        self.main_window.mix_wieght_Loaded_chem_2_lineEdit.setText(str(weight))

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
            
        if self.rock_and_sand_loadding_success == True:
            self.loaded_rock_and_sand_successfully()
            self.rock_and_sand_loadding_success = False
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
        else:
            pass
        
    def mix_start_load(self):
        self.rock1, self.sand, self.rock2, self.cement, self.fyash, self.water, self.chem1, self.chem2 = self.main_window.get_data_formular_in_mix_form()
        self.rock_and_sand_values = [int(self.rock1), int(self.sand), int(self.rock2)]
        self.cement_and_fyash_values = [int(self.cement), int(self.fyash)]

        self.is_loading_rock_and_sand_in_progress = True
        self.thread_rock_and_sand = Thread(target=self.load_rock_and_sand_sequence,args=(self.rock_and_sand_values,))
        self.thread_rock_and_sand.start()
        self.state_load_rock_and_sand = 1

        self.is_loading_cement_and_fyash_in_progress = True
        self.thread_cement_and_fyash = Thread(target=self.load_cement_and_fyash_sequence,args=(self.cement_and_fyash_values,))
        self.thread_cement_and_fyash.start()
        self.state_load_cement_and_fyash = 1
        
        
    def load_rock_and_sand_sequence(self,data_loaded):
        rock_1, sand, rock_2 = data_loaded
        while self.is_loading_rock_and_sand_in_progress:
            if self.state_load_rock_and_sand == 0:
                pass
            elif self.state_load_rock_and_sand == 1:
                self.autoda_controller.write_set_point_rock_and_sand(rock_1)
                self.plc_controller.loading_rock1("start")
                self.state_load_rock_and_sand = 2
                
            elif self.state_load_rock_and_sand == 2:
                if self.rock_success == True:
                    self.plc_controller.loading_rock1("stop")
                    self.autoda_controller.write_set_point_rock_and_sand(sand)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 3
                    
            elif self.state_load_rock_and_sand == 3:
                self.plc_controller.loading_sand("start")
                self.state_load_rock_and_sand = 4
            
            elif self.state_load_rock_and_sand == 4:
                if self.rock_success == True:
                    self.plc_controller.loading_sand("stop")
                    self.autoda_controller.write_set_point_rock_and_sand(rock_2)
                    time.sleep(1)
                    self.state_load_rock_and_sand = 5
            
            elif self.state_load_rock_and_sand == 5:
                self.plc_controller.loading_rock2("start")
                self.state_load_rock_and_sand = 6
            
            elif self.state_load_rock_and_sand == 6:
                if self.rock_success == True:
                    self.plc_controller.loading_rock2("stop")
                    self.state_load_rock_and_sand = 0
                    self.rock_and_sand_loadding_success = True
                    self.is_loading_rock_and_sand_in_progress = False
            time.sleep(0.1)
    

    def load_cement_and_fyash_sequence(self,data_loaded):
        cement, fyash = data_loaded
        while self.is_loading_cement_and_fyash_in_progress:
            if self.state_load_cement_and_fyash == 0:
                pass
            elif self.state_load_cement_and_fyash == 1:
                self.autoda_controller.write_set_point_cement_and_fyash(cement)
                self.plc_controller.loading_cement("start")
                self.state_load_cement_and_fyash = 2
                
            elif self.state_load_cement_and_fyash == 2:
                if self.cement_success == True:
                    self.plc_controller.loading_cement("stop")
                    self.autoda_controller.write_set_point_cement_and_fyash(fyash)
                    time.sleep(1)
                    self.state_load_cement_and_fyash = 3
                    
            elif self.state_load_cement_and_fyash == 3:
                self.plc_controller.loading_flyash("start")
                self.state_load_cement_and_fyash = 4
            
            elif self.state_load_cement_and_fyash == 4:
                if self.cement_success == True:
                    self.plc_controller.loading_flyash("stop")
                    self.state_load_cement_and_fyash = 0
                    self.cement_and_fyash_loading_success = True
                    self.is_loading_cement_and_fyash_in_progress = False
            time.sleep(0.1)


    def loaded_rock_and_sand_successfully(self):
        if self.thread_rock_and_sand and self.thread_rock_and_sand.is_alive():
            self.thread_rock_and_sand.join()


    def loaded_cement_and_fyash_successfully(self):
        if self.thread_cement_and_fyash and self.thread_cement_and_fyash.is_alive():
            self.thread_cement_and_fyash.join()
            

    def mix_cancel_load(self):
        if self.is_loading_rock_and_sand_in_progress:
            self.is_loading_rock_and_sand_in_progress = False
            if hasattr(self, 'thread_rock_and_sand') and self.thread_rock_and_sand.is_alive():
                self.thread_rock_and_sand.join()
        if self.is_loading_cement_and_fyash_in_progress:
            self.is_loading_cement_and_fyash_in_progress = False
            if hasattr(self, 'thread_cement_and_fyash') and self.thread_cement_and_fyash.is_alive():
                self.thread_cement_and_fyash.join()


    def Show_main(self):
        self.main_window.Show()


