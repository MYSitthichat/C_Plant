from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem

class debug_tab(QObject):
    def __init__(self, main_window, plc_controller):
        super(debug_tab, self).__init__()
        self.main_window = main_window
        self.plc_controller = plc_controller
        self.connect_signals()

    def connect_signals(self):

        # self.main_window.debug_open_rock_1_pushButton.clicked.connect(self.plc_controller.emit.action("start"))
        # self.main_window.debug_close_rock_1_pushButton.clicked.connect(self.plc_controller.debug_rock_1_action(action = "stop"))
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

    def debug_open_rock_1(self):
        self.plc_controller.loading_rock1("start")

    def debug_close_rock_1(self):
        self.plc_controller.loading_rock1("stop")

    def debug_open_rock_2(self):
        self.plc_controller.loading_rock2("start")

    def debug_close_rock_2(self):
        self.plc_controller.loading_rock2("stop")

    def debug_open_sand(self):
        self.plc_controller.loading_sand("start")

    def debug_close_sand(self):
        self.plc_controller.loading_sand("stop")

    def debug_open_converyer_under(self):
        self.plc_controller.converyer_midle("start")

    def debug_close_converyer_under(self):
        self.plc_controller.converyer_midle("stop")

    def debug_open_converyer_top(self):
        self.plc_controller.converyer_top("start")

    def debug_close_converyer_top(self):
        self.plc_controller.converyer_top("stop")

    def debug_open_cement(self):
        self.plc_controller.loading_cement("start")

    def debug_close_cement(self):
        self.plc_controller.loading_cement("stop")

    def debug_open_fyash(self):
        self.plc_controller.loading_flyash("start")

    def debug_close_fyash(self):
        self.plc_controller.loading_flyash("stop")

    def debug_open_vale_cement(self):
        self.plc_controller.vale_cement_and_fyash("start")

    def debug_close_vale_cement(self):
        self.plc_controller.vale_cement_and_fyash("stop")

    def debug_open_mixer(self):
        self.plc_controller.mixer("start")

    def debug_close_mixer(self):
        self.plc_controller.mixer("stop")

    def debug_open_vale_mixer(self):
        self.plc_controller.vale_mixer("start")

    def debug_close_vale_mixer(self):
        self.plc_controller.vale_mixer("stop")

    def debug_open_water(self):
        self.plc_controller.loading_water("start")

    def debug_close_water(self):
        self.plc_controller.loading_water("stop")

    def debug_open_vale_water(self):
        self.plc_controller.vale_water("start")

    def debug_close_vale_water(self):
        self.plc_controller.vale_water("stop")

    def debug_open_chem_1(self):
        self.plc_controller.loading_chemical_1("start")

    def debug_close_chem_1(self):
        self.plc_controller.loading_chemical_1("stop")

    def debug_open_chem_2(self):
        self.plc_controller.loading_chemical_2("start")

    def debug_close_chem_2(self):
        self.plc_controller.loading_chemical_2("stop")

    def debug_open_vale_chem(self):
        self.plc_controller.pump_chemical_up("start")

    def debug_close_vale_chem(self):
        self.plc_controller.pump_chemical_up("stop")

