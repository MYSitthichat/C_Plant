from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QThread
import os
import sys
from pymodbus.client import ModbusSerialClient
import time

class AUTODA_Controller(QThread,QObject):
    comport_error = Signal(list)
    weight_rock_and_sand = Signal(int)
    weight_cement_and_fyash = Signal(int)
    
    def __init__(self,main_window,db):
    # def __init__(self,):
        super(AUTODA_Controller, self).__init__()
        self.running = True
        self.main_window = main_window
        self.db = db
        self.read_config_file()
    
    def int32_to_registers(self, value):
        if value < 0:
            value = (1 << 32) + value
        high_word = (value >> 16) & 0xFFFF
        low_word = value & 0xFFFF
        return [high_word, low_word]
    
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
                        self.rock_and_sand_id = self.config.get('ROCK_AND_SAND_ID', int())
                        self.rock_and_sand_id = int(self.rock_and_sand_id)
                        self.cement_and_flyash_id = self.config.get('CEMENT_AND_FLYASH_ID', int())
                        self.cement_and_flyash_id = int(self.cement_and_flyash_id)
                        self.water_id = self.config.get('WATER_ID', int())
                        self.water_id = int(self.water_id)
                        self.chemical_id = self.config.get('CHEMICAL_ID', int())
                        self.chemical_id = int(self.chemical_id)
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

    def read_cement_and_fyash(self):
        register_weight = 81  # Register weight cement and flyash
        read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.cement_and_flyash_id)
        raw_value = (read_weight.registers[0])
        if raw_value > 32767:
            weight_value = raw_value - 65536
        else:
            weight_value = raw_value
        self.weight_cement_and_fyash.emit(weight_value)

    def read_weight_rock_and_sand(self):
        register_weight = 81  # Register weight rock and sand
        read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.rock_and_sand_id)
        raw_value = (read_weight.registers[0])
        if raw_value > 32767:
            weight_value = raw_value - 65536
        else:
            weight_value = raw_value
        self.weight_rock_and_sand.emit(weight_value)

    def write_set_point(self,value):
        address_register = 314 #register set point rock and sand
        unlock_address = 5      # Address 5 (คือ Register 40006)
        unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.rock_and_sand_id)
        self.msleep(100)
        register_values = self.int32_to_registers(value)
        self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.rock_and_sand_id)



    def run(self):
        while self.running:
            try:
                self.read_weight_rock_and_sand()
                self.read_cement_and_fyash()
            except Exception as e:
                print(f"Error in AutoDA Controller: {e}")
                pass
            self.msleep(100)

    def stop(self):
        self.running = False
        self.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    autoda_controller = AUTODA_Controller()
    autoda_controller.initialize_connections()
    time.sleep(2)
    autoda_controller.start()
    sys.exit(0)