from PySide6.QtWidgets import QApplication,QMessageBox
from PySide6.QtCore import Slot , QObject, Signal, QThread
import os
import sys
from pymodbus.client import ModbusSerialClient
import time

class PLC_Controller(QThread, QObject):
    comport_error = Signal(list)
    status_loading_rock_and_sand = Signal(bool)
    status_loading_cement_and_fyash = Signal(bool)
    status_loading_water = Signal(bool)
    status_loading_chemical = Signal(bool)
    
    def __init__(self, main_window, db):
        super(PLC_Controller, self).__init__()
        self.running = True
        self.main_window = main_window
        self.db = db
        self.read_config_file()
        
    def initialize_connections(self):
        self.connect_to_plc()
    
    def read_config_file(self):
        self.config = {}
        self.plc_port = ''
        self.baudrate = ''
        self.stop_bits = ''
        self.parity = ''
        self.data_bits = ''
        self.timeout_error = ''
        self.PLC_id_weight = ''
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'port.conf')
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
                        self.plc_port = self.config.get('PLC_PORT', '')
                        self.baudrate = self.config.get('BAUDRATE', '')
                        self.stop_bits = self.config.get('STOP_BITS', '')
                        self.parity = self.config.get('PARITY', '')
                        self.data_bits = self.config.get('DATA_BITS', '')
                        self.timeout_error = self.config.get('TIMEOUT_ERROR', '')
                        self.PLC_id_weight = self.config.get('PLC_ID_WEIGHT', '')
                        self.PLC_id_conditioner = self.config.get('PLC_ID_CONDITION', '')
                        
        except FileNotFoundError:
            print(f"port.conf file not found at {config_path}")
            
    def debug_rock_1_action(self, action):
        if action == "start":
            print("Debug: Starting Rock 1")
        elif action == "stop":
            print("Debug: Stopping Rock 1")
            
    def connect_to_plc(self):
        plc_port = self.plc_port
        baudrate = int(self.baudrate)
        stop_bits = int(self.stop_bits)
        parity = str(self.parity)
        data_bits = int(self.data_bits)
        timeout = int(self.timeout_error)
        self.plc_client = ModbusSerialClient(
            port=plc_port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stop_bits,
            bytesize=data_bits,
            timeout=timeout
        )
        try:
            if self.plc_client.connect():
                self.comport_error.emit([False, 'PLC'])
            else:
                self.comport_error.emit([True, 'PLC'])
        except Exception as e:
            self.comport_error.emit([True, 'PLC'])

    def disconnect_to_plc(self):
        self.plc_client.close()
    
    def loading_rock1(self,status):
        if status == "start":
            self.plc_client.write_coil(address=0, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=0, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_sand(self,status):
        if status == "start":
            self.plc_client.write_coil(address=1, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=1, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_rock2(self,status):
        if status == "start":
            self.plc_client.write_coil(address=2, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=2, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_cement(self,status):
        if status == "start":
            self.plc_client.write_coil(address=3, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=3, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_flyash(self,status):
        if status == "start":
            self.plc_client.write_coil(address=4, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=4, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_water(self,status):
        if status == "start":
            self.plc_client.write_coil(address=5, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=5, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def loading_chemical(self,status):
        if status == "start":
            self.plc_client.write_coil(address=6, value=1, device_id=int(self.PLC_id_weight))
        elif status == "stop":
            self.plc_client.write_coil(address=6, value=0, device_id=int(self.PLC_id_weight))
        pass
    
    def reading_finish_load_rock_and_sand(self):
        read_finish = self.plc_client.read_coils(address=100, count=1, device_id=int(self.PLC_id_weight))
        self.status_loading_rock_and_sand.emit(read_finish.bits[0])
        
    def reading_finish_load_cement_and_fyash(self):
        read_finish = self.plc_client.read_coils(address=110, count=1, device_id=int(self.PLC_id_weight))
        self.status_loading_cement_and_fyash.emit(read_finish.bits[0])

    def reading_finish_load_water(self):
        read_finish = self.plc_client.read_coils(address=120, count=1, device_id=int(self.PLC_id_weight))
        self.status_loading_water.emit(read_finish.bits[0])

    def reading_finish_load_chemical(self):
        read_finish = self.plc_client.read_coils(address=130, count=1, device_id=int(self.PLC_id_weight))
        self.status_loading_chemical.emit(read_finish.bits[0])

    def run(self):
        while self.running:
            try:
                self.reading_finish_load_rock_and_sand()
                self.reading_finish_load_cement_and_fyash()
                self.reading_finish_load_water()
                self.reading_finish_load_chemical()
            except Exception as e:
                print(f"Error in PLC Controller: {e}")
            self.msleep(100)

    def stop(self):
        self.running = False
        self.wait()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plc_controller = PLC_Controller()
    sys.exit(0)