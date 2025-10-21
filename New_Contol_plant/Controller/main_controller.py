from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject 
import csv
from PySide6.QtWidgets import QFileDialog,QMessageBox
from threading import Thread
import time
from datetime import datetime


class MainController(QObject):   
    def __init__(self):
        super(MainController, self).__init__()
        self.main_window = MainWindow()
        self.main_window.reg_save_pushButton.clicked.connect(self.reg_save)
        self.main_window.reg_clear_pushButton.clicked.connect(self.reg_clear)
        self.main_window.reg_save_new_custommer_pushButton.clicked.connect(self.reg_save_new_custommer)
        self.main_window.mix_start_load_pushButton.clicked.connect(self.mix_start_load)
        self.main_window.mix_cancel_load_pushButton.clicked.connect(self.mix_cancel_load)
        self.main_window.for_add_formula_pushButton.clicked.connect(self.for_add_formula)
        self.main_window.for_config_formula_pushButton.clicked.connect(self.for_config_formula)
        self.main_window.for_delete_formula_pushButton.clicked.connect(self.for_delete_formula)
        self.main_window.for_save_formula_pushButton.clicked.connect(self.for_save_formula)
        self.main_window.for_cancel_pushButton.clicked.connect(self.for_cancel)
        self.main_window.debug_open_rock_1_pushButton.clicked.connect(self.debug_open_rock_1)
        self.main_window.debug_close_rock_1_pushButton.clicked.connect(self.debug_close_rock_1)
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



    def reg_save(self):
        pass

    def reg_clear(self):
        pass
    
    def reg_save_new_custommer(self):
        pass
        
# End methods
    def Show_main(self):
        self.main_window.Show()
        