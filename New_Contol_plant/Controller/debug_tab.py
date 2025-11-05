from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class debug_tab(QObject):
    def __init__(self, main_window,):
        super(debug_tab, self).__init__()
        self.main_window = main_window

        self.connect_signals()

    def connect_signals(self):

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

