from PySide6.QtWidgets import QApplication,QMessageBox
from PySide6.QtCore import Slot , QObject, Signal
import os
import sys
from pymodbus.client import ModbusSerialClient
import time

class AUTODA_Controller(QObject):
    comport_error = Signal(list)
    
    def __init__(self,main_window,db):
        super(AUTODA_Controller, self).__init__()
        self.main_window = main_window
        self.db = db
        self.read_config_file()
        
    def initialize_connections(self):
        self.connect_to_autodac()
    
    def read_config_file(self):
        self.config = {}
        self.autoda_port = ''
        self.baudrate = ''
        self.stop_bits = ''
        self.parity = ''
        self.data_bits = ''
        self.timeout_error = ''
        self.rock_and_sand_id = ''
        self.cement_and_flyash_id = ''
        self.water_id = ''
        self.chemical_id = ''
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'port.conf')
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
                        self.autoda_port = self.config.get('AUTODA_PORT', '')
                        self.baudrate = self.config.get('BAUDRATE', '')
                        self.stop_bits = self.config.get('STOP_BITS', '')
                        self.parity = self.config.get('PARITY', '')
                        self.data_bits = self.config.get('DATA_BITS', '')
                        self.timeout_error = self.config.get('TIMEOUT_ERROR', '')
                        self.rock_and_sand_id = self.config.get('ROCK_AND_SAND_ID', '')
                        self.cement_and_flyash_id = self.config.get('CEMENT_AND_FLYASH_ID', '')
                        self.water_id = self.config.get('WATER_ID', '')
                        self.chemical_id = self.config.get('CHEMICAL_ID', '')
        except FileNotFoundError:
            print(f"port.conf file not found at {config_path}")
            
    def debug_rock_1_action(self, action):
        if action == "start":
            print("Debug: Starting Rock 1")
        elif action == "stop":
            print("Debug: Stopping Rock 1")
    
    def connect_to_autodac(self):
        autoda_port = self.autoda_port
        baudrate = int(self.baudrate)
        stop_bits = int(self.stop_bits)
        parity = str(self.parity)
        data_bits = int(self.data_bits)
        timeout = int(self.timeout_error)

        self.autoda_client = ModbusSerialClient(
            port=autoda_port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stop_bits,
            bytesize=data_bits,
            timeout=timeout
        )
        try:
            if self.autoda_client.connect():
                self.comport_error.emit([False, 'AutoDA'])
            else:
                self.comport_error.emit([True, 'AutoDA'])
        except Exception as e:
            self.comport_error.emit([True, 'AutoDA'])

    def disconnect_to_autodac(self):
        self.autoda_client.close()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plc_controller = AUTODA_Controller()
    sys.exit(0)