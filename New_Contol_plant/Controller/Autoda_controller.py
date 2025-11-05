from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QThread
import os
import sys
from pymodbus.client import ModbusSerialClient
import time


def get_divisor_from_code(div_code):
    div_map = {
        12: 1,     # 0 ตำแหน่ง (ค่า 1) 
        9: 10,     # 1 ตำแหน่ง (ค่า 0.1) 
        6: 100,    # 2 ตำแหน่ง (ค่า 0.01) 
        3: 1000,   # 3 ตำแหน่ง (ค่า 0.001) 
        0: 10000   # 4 ตำแหน่ง (ค่า 0.0001) 
    }
    return div_map.get(div_code, 1)

class AUTODA_Controller(QThread,QObject):
    comport_error = Signal(list)
    weight_rock_and_sand = Signal(int)
    weight_cement_and_fyash = Signal(int)
    weight_water = Signal(int)
    weight_chemical = Signal(float)  # เปลี่ยนเป็น float สำหรับทศนิยม
    
    def __init__(self,main_window,db):
    # def __init__(self,):
        super(AUTODA_Controller, self).__init__()
        self.running = True
        self.main_window = main_window
        self.db = db
        # ตัวแปรสำหรับการจัดการทศนิยมของ Chemical
        self.chemical_divisor = 1
        self.chemical_decimal_initialized = False
        self.read_config_file()
    
    def int32_to_registers(self, value):
        if value < 0:
            value = (1 << 32) + value
        high_word = (value >> 16) & 0xFFFF
        low_word = value & 0xFFFF
        return [high_word, low_word]
    
    def read_chemical_decimal_setting(self):
        try:
            ADDRESS_DIV = 88  # Register 40089 (Gain value / div)
            rr_div = self.autoda_client.read_holding_registers(
                address=ADDRESS_DIV,
                count=1,
                device_id=self.chemical_id
            )
            
            if rr_div.isError():
                self.chemical_divisor = 1
                return False
            else:
                div_code = rr_div.registers[0]
                self.chemical_divisor = get_divisor_from_code(div_code)
                self.chemical_decimal_initialized = True
                return True
                
        except Exception as e:
            self.chemical_divisor = 1
            return False
    
    def float_to_int_with_chemical_divisor(self, float_value):
        return int(float_value * self.chemical_divisor)
    
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

    def read_weight_rock_and_sand(self):
        register_weight = 81  # Register weight rock and sand
        read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.rock_and_sand_id)
        raw_value = (read_weight.registers[0])
        if raw_value > 32767:
            weight_value = raw_value - 65536
        else:
            weight_value = raw_value
        self.weight_rock_and_sand.emit(weight_value)

    def read_cement_and_fyash(self):
        register_weight = 81  # Register weight cement and flyash
        read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.cement_and_flyash_id)
        raw_value = (read_weight.registers[0])
        if raw_value > 32767:
            weight_value = raw_value - 65536
        else:
            weight_value = raw_value
        self.weight_cement_and_fyash.emit(weight_value)

    def read_water(self):
        register_weight = 81  # Register weight water
        read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.water_id)
        raw_value = (read_weight.registers[0])
        if raw_value > 32767:
            weight_value = raw_value - 65536
        else:
            weight_value = raw_value
        self.weight_water.emit(weight_value)

    def read_chemical(self):
        if not self.chemical_decimal_initialized:
            self.read_chemical_decimal_setting()
        
        register_weight = 81  # Register weight chemical
        try:
            read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.chemical_id)
            
            if read_weight.isError():
                self.weight_chemical.emit(0.0)
                return
                
            raw_value = (read_weight.registers[0])
            if raw_value > 32767:
                signed_value = raw_value - 65536
            else:
                signed_value = raw_value
            float_value = signed_value / self.chemical_divisor
            
            self.weight_chemical.emit(float_value)
            
        except Exception as e:
            self.weight_chemical.emit(0.0)

    def write_set_point_rock_and_sand(self,value):
        address_register = 314 #register set point rock and sand
        unlock_address = 5      # Address 5 (คือ Register 40006)
        unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.rock_and_sand_id)
        self.msleep(100)
        register_values = self.int32_to_registers(value)
        self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.rock_and_sand_id)

    def write_set_point_cement_and_fyash(self,value):
        address_register = 314 #register set point rock and sand
        unlock_address = 5      # Address 5 (คือ Register 40006)
        unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.cement_and_flyash_id)
        self.msleep(100)
        register_values = self.int32_to_registers(value)
        self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.cement_and_flyash_id)

    def write_set_point_water(self,value):
        address_register = 314 #register set point rock and sand
        unlock_address = 5      # Address 5 (คือ Register 40006)
        unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.water_id)
        self.msleep(100)
        register_values = self.int32_to_registers(value)
        self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.water_id)
    
    def write_set_point_chemical(self, value):
        if not self.chemical_decimal_initialized:
            self.read_chemical_decimal_setting()
        address_register = 314  # register set point chemical
        unlock_address = 5      # Address 5 (คือ Register 40006)
        unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        try:
            # Unlock register
            unlock_result = self.autoda_client.write_register(
                address=unlock_address, 
                value=unlock_code, 
                device_id=self.chemical_id
            )
            if unlock_result.isError():
                return False
            self.msleep(100)
            int_value = self.float_to_int_with_chemical_divisor(value)
            register_values = self.int32_to_registers(int_value)
            write_result = self.autoda_client.write_registers(
                address=address_register, 
                values=register_values, 
                device_id=self.chemical_id
            )
            if write_result.isError():
                return False
            else:
                return True
        except Exception as e:
            return False

    def run(self):
        while self.running:
            try:
                self.read_weight_rock_and_sand()
                self.read_cement_and_fyash()
                self.read_water()
                self.read_chemical()
            except Exception as e:
                print(f"Error in AutoDA Controller: {e}")
                pass
            self.msleep(10)

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