from View.view_main_frame import MainWindow
from PySide6.QtCore import Slot , QObject 
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



    def reg_save(self):
        print("reg save")

    def reg_clear(self):
        print("reg clear")

    def reg_save_new_custommer(self):
        print("reg save new customer")

    def mix_start_load(self):
        print("mix start load")

    def mix_cancel_load(self):
        print("mix cancel load")

    def for_add_formula(self):
        print("for add formula")

    def for_config_formula(self):
        print("for config formula")

    def for_delete_formula(self):
        print("for delete formula")

    def for_save_formula(self):
        print("for save formula")

    def for_cancel(self):
        print("for cancel formula")

    def debug_open_rock_1(self):
        print("debug open rock 1")

    def debug_close_rock_1(self):
        print("debug close rock 1")

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

    def offset_save(self):
        print("offset save")

    def offset_edite(self):
        print("offset edite")

    def offset_cancel(self):
        print("offset cancel")

        

# End methods
    def Show_main(self):
        self.main_window.Show()
