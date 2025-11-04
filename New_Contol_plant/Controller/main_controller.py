from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject, Qt
from PySide6.QtWidgets import QFileDialog,QMessageBox,QTreeWidgetItem
from threading import Thread
import time
from datetime import datetime
from Controller.database_control import C_palne_Database
from Controller.PLC_controller import PLC_Controller
from Controller.temp_queue import TempQueue
from Controller.reg_tab import reg_tab
from Controller.load_work_queue import load_work_queue
from Controller.formula_tab import formula_tab
from Controller.offset_tab import offset_tab

class MainController(QObject):
    action = Slot(str)
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()

        self.db = C_palne_Database()
        # self.plc_controller = PLC_Controller()
        self.data_formula = []

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

    @Slot(str)
    @Slot(bool)
    def update_status_port(self,status):
        print("update status port:",status)


    def mix_start_load(self):
        print("mix start load")

    def mix_cancel_load(self):
        print("mix cancel load")


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


    def Show_main(self):
        self.main_window.Show()

