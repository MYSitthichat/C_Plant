from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QThread, QMutex
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

    setpoint_rock_sand_read = Signal(object)
    setpoint_cement_and_fyash_read = Signal(object)
    setpoint_water_read = Signal(object)
    setpoint_chemical_read = Signal(object)

    
    def __init__(self,main_window,db):
    # def __init__(self,): #Debug
        super(AUTODA_Controller, self).__init__()
        self.mutex = QMutex()
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
        # debug
        # autoda_port = 'COM4'
        # baudrate = 9600
        # stop_bits = 1
        # parity = 'N'
        # data_bits = 8
        # timeout = 3
        # debug
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
                print(f"autoda status port {self.autoda_client.is_socket_open()}")
                self.comport_error.emit([False, 'AutoDA'])
            else:
                self.comport_error.emit([True, 'AutoDA'])
        except Exception as e:
            self.comport_error.emit([True, 'AutoDA'])

    def disconnect_to_autodac(self):
        self.autoda_client.close()

    def monitor_connection(self):
        """ตรวจสอบ connection status และ reconnect ถ้าจำเป็น"""
        if not hasattr(self, 'autoda_client') or not self.autoda_client:
            print("AutoDA client not initialized")
            return False
        
        try:
            if not self.autoda_client.is_socket_open():
                print("AutoDA serial port is closed - attempting reconnect...")
                self.connect_to_autodac()
                self.msleep(2000)  # รอ 2 วินาที
                
                if self.autoda_client and self.autoda_client.is_socket_open():
                    print("✓ AutoDA reconnected successfully")
                    # อ่านค่า chemical decimal setting ใหม่หลัง reconnect
                    self.chemical_decimal_initialized = False
                    self.read_chemical_decimal_setting()
                    return True
                else:
                    print("✗ AutoDA reconnect failed")
                    self.comport_error.emit([True, 'AutoDA'])
                    return False
            return True
        except Exception as e:
            print(f"Error checking AutoDA connection: {e}")
            return False

    def ensure_connection(self, operation_name="operation"):
        """ตรวจสอบและรับประกัน connection ก่อนทำงาน"""
        max_retry = 3
        for attempt in range(max_retry):
            if self.monitor_connection():
                return True
            print(f"Connection failed for {operation_name}, retry {attempt + 1}/{max_retry}")
            self.msleep(1000)
        
        print(f"Failed to ensure connection for {operation_name} after {max_retry} retries")
        return False

    def read_weight_rock_and_sand(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading rock_sand weight, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            self.weight_rock_and_sand.emit(0)
                            return
                    
                    register_weight = 81  # Register weight rock and sand
                    read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.rock_and_sand_id)
                    
                    if read_weight.isError():
                        print(f"Error reading rock_sand weight, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(300)
                            continue
                        else:
                            self.weight_rock_and_sand.emit(0)
                            return
                    
                    raw_value = (read_weight.registers[0])
                    if raw_value > 32767:
                        weight_value = raw_value - 65536
                    else:
                        weight_value = raw_value
                    self.weight_rock_and_sand.emit(weight_value)
                    return
                    
                except Exception as e:
                    print(f"Exception reading rock_sand weight, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(300)
                    else:
                        self.weight_rock_and_sand.emit(0)
                        
        except Exception as e:
            print(f"Fatal exception in read_weight_rock_and_sand: {e}")
            self.weight_rock_and_sand.emit(0)
        finally:
            self.mutex.unlock()

    def read_cement_and_fyash(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading cement weight, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            self.weight_cement_and_fyash.emit(0)
                            return
                    
                    register_weight = 81  # Register weight cement and flyash
                    read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.cement_and_flyash_id)
                    
                    if read_weight.isError():
                        print(f"Error reading cement weight, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(300)
                            continue
                        else:
                            self.weight_cement_and_fyash.emit(0)
                            return
                    
                    raw_value = (read_weight.registers[0])
                    if raw_value > 32767:
                        weight_value = raw_value - 65536
                    else:
                        weight_value = raw_value
                    self.weight_cement_and_fyash.emit(weight_value)
                    return
                    
                except Exception as e:
                    print(f"Exception reading cement weight, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(300)
                    else:
                        self.weight_cement_and_fyash.emit(0)
                        
        except Exception as e:
            print(f"Fatal exception in read_cement_and_fyash: {e}")
            self.weight_cement_and_fyash.emit(0)
        finally:
            self.mutex.unlock()

    def read_water(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading water weight, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            self.weight_water.emit(0)
                            return
                    
                    register_weight = 81  # Register weight water
                    read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.water_id)
                    
                    if read_weight.isError():
                        print(f"Error reading water weight, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(300)
                            continue
                        else:
                            self.weight_water.emit(0)
                            return
                    
                    raw_value = (read_weight.registers[0])
                    if raw_value > 32767:
                        weight_value = raw_value - 65536
                    else:
                        weight_value = raw_value
                    self.weight_water.emit(weight_value)
                    return
                    
                except Exception as e:
                    print(f"Exception reading water weight, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(300)
                    else:
                        self.weight_water.emit(0)
                        
        except Exception as e:
            print(f"Fatal exception in read_water: {e}")
            self.weight_water.emit(0)
        finally:
            self.mutex.unlock()

    def read_chemical(self):
        self.mutex.lock()
        max_retries = 3
        try:
            if not self.chemical_decimal_initialized:
                self.read_chemical_decimal_setting()
            
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading chemical weight, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            self.weight_chemical.emit(0.0)
                            return
                    
                    register_weight = 81  # Register weight chemical
                    read_weight = self.autoda_client.read_holding_registers(address=register_weight, count=1, device_id=self.chemical_id)
                    
                    if read_weight.isError():
                        print(f"Error reading chemical weight, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(300)
                            continue
                        else:
                            self.weight_chemical.emit(0.0)
                            return
                    
                    raw_value = (read_weight.registers[0])
                    if raw_value > 32767:
                        signed_value = raw_value - 65536
                    else:
                        signed_value = raw_value
                    float_value = signed_value / self.chemical_divisor
                    self.weight_chemical.emit(float_value)
                    return
                    
                except Exception as e:
                    print(f"Exception reading chemical weight, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(300)
                    else:
                        self.weight_chemical.emit(0.0)
                        
        except Exception as e:
            print(f"Fatal exception in read_chemical: {e}")
            self.weight_chemical.emit(0.0)
        finally:
            self.mutex.unlock()

    def read_setpoint_rock_sand(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading setpoint rock_sand, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"No response received after {max_retries} retries for setpoint rock_sand")
                            self.setpoint_rock_sand_read.emit(None)
                            return
                    
                    address_register = 314 #register set point rock and sand
                    rock_sand_address = 1
                    result = self.autoda_client.read_holding_registers(address=address_register, count=2, device_id=rock_sand_address)
                    
                    if result.isError():
                        print(f"Error reading setpoint rock_sand, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            print(f"No response received after {max_retries} retries, continue with next request")
                            self.setpoint_rock_sand_read.emit(None)
                            return
                    
                    self.setpoint_rock_sand_read.emit(result.registers[1])
                    return
                    
                except Exception as e:
                    print(f"Exception reading setpoint rock_sand, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        print(f"No response received after {max_retries} retries, continue with next request")
                        self.setpoint_rock_sand_read.emit(None)
                        
        except Exception as e:
            print(f"Fatal exception in read_setpoint_rock_sand: {e}")
            self.setpoint_rock_sand_read.emit(None)
        finally:
            self.mutex.unlock()

    def read_setpoint_cement_fyash(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading setpoint cement, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"No response received after {max_retries} retries for setpoint cement")
                            self.setpoint_cement_and_fyash_read.emit(None)
                            return
                    
                    address_register = 314 #register set point rock and sand
                    cement_and_fyash_address = 2
                    result = self.autoda_client.read_holding_registers(address=address_register, count=2, device_id=cement_and_fyash_address)
                    
                    if result.isError():
                        print(f"Error reading setpoint cement, attempt {attempt + 1}: Repeating....")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            print(f"No response received after {max_retries} retries, continue with next request")
                            self.setpoint_cement_and_fyash_read.emit(None)
                            return
                    
                    self.setpoint_cement_and_fyash_read.emit(result.registers[1])
                    return
                    
                except Exception as e:
                    print(f"Exception reading setpoint cement, attempt {attempt + 1}: {e}")
                    print("Repeating....")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        print(f"No response received after {max_retries} retries, continue with next request")
                        self.setpoint_cement_and_fyash_read.emit(None)
                        
        except Exception as e:
            print(f"Fatal exception in read_setpoint_cement_fyash: {e}")
            self.setpoint_cement_and_fyash_read.emit(None)
        finally:
            self.mutex.unlock()

    def read_setpoint_water_work(self):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading setpoint water, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"No response received after {max_retries} retries for setpoint water")
                            self.setpoint_water_read.emit(None)
                            return
                    
                    address_register = 314 #register set point rock and sand
                    water_address = 3
                    result = self.autoda_client.read_holding_registers(address=address_register, count=2, device_id=water_address)
                    
                    if result.isError():
                        print(f"Error reading setpoint water, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            print(f"No response received after {max_retries} retries, continue with next request")
                            self.setpoint_water_read.emit(None)
                            return
                    
                    self.setpoint_water_read.emit(result.registers[1])
                    return
                    
                except Exception as e:
                    print(f"Exception reading setpoint water, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        print(f"No response received after {max_retries} retries, continue with next request")
                        self.setpoint_water_read.emit(None)
                        
        except Exception as e:
            print(f"Fatal exception in read_setpoint_water: {e}")
            self.setpoint_water_read.emit(None)
        finally:
            self.mutex.unlock()

    def read_setpoint_chemical_work(self):
        self.mutex.lock()
        max_retries = 3
        try:
            if not self.chemical_decimal_initialized:
                self.read_chemical_decimal_setting()
            
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนอ่าน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before reading setpoint chemical, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"No response received after {max_retries} retries for setpoint chemical")
                            self.setpoint_chemical_read.emit(None)
                            return
                    
                    address_register = 314
                    chemical_drress = 4 
                    result = self.autoda_client.read_holding_registers(
                        address=address_register, 
                        count=2, 
                        device_id=chemical_drress
                    )
                    
                    if result.isError():
                        print(f"Error reading setpoint chemical, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            print(f"No response received after {max_retries} retries, continue with next request")
                            self.setpoint_chemical_read.emit(None)
                            return
                    
                    high_word = result.registers[0]
                    low_word = result.registers[1]
                    raw_int = (high_word << 16) | low_word
                    if raw_int >= 0x80000000:
                        raw_int -= 0x100000000
                    float_setpoint = raw_int / self.chemical_divisor
                    self.setpoint_chemical_read.emit(float_setpoint)
                    return
                    
                except Exception as e:
                    print(f"Exception reading setpoint chemical, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        print(f"No response received after {max_retries} retries, continue with next request")
                        self.setpoint_chemical_read.emit(None)
                        
        except Exception as e:
            print(f"Fatal exception in read_setpoint_chemical: {e}")
            self.setpoint_chemical_read.emit(None)
        finally:
            self.mutex.unlock()

    def write_set_point_rock_and_sand(self,value):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนเขียน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before writing setpoint rock_sand, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"Failed to write setpoint rock_sand after {max_retries} retries")
                            return False
                    
                    address_register = 314 #register set point rock and sand
                    unlock_address = 5      # Address 5 (คือ Register 40006)
                    unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
                    
                    unlock_result = self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.rock_and_sand_id)
                    if unlock_result.isError():
                        print(f"Error unlocking rock_sand register, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    self.msleep(100)
                    register_values = self.int32_to_registers(value)
                    write_result = self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.rock_and_sand_id)
                    
                    if write_result.isError():
                        print(f"Error writing setpoint rock_sand, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    return True
                    
                except Exception as e:
                    print(f"Exception writing setpoint rock_sand, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        return False
                        
        except Exception as e:
            print(f"Fatal exception in write_set_point_rock_and_sand: {e}")
            return False
        finally:
            self.mutex.unlock()

    def write_set_point_cement_and_fyash(self,value):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนเขียน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before writing setpoint cement, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"Failed to write setpoint cement after {max_retries} retries")
                            return False
                    
                    address_register = 314 #register set point rock and sand
                    unlock_address = 5      # Address 5 (คือ Register 40006)
                    unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
                    
                    unlock_result = self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.cement_and_flyash_id)
                    if unlock_result.isError():
                        print(f"Error unlocking cement register, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    self.msleep(100)
                    register_values = self.int32_to_registers(value)
                    write_result = self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.cement_and_flyash_id)
                    
                    if write_result.isError():
                        print(f"Error writing setpoint cement, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    return True
                    
                except Exception as e:
                    print(f"Exception writing setpoint cement, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        return False
                        
        except Exception as e:
            print(f"Fatal exception in write_set_point_cement_and_fyash: {e}")
            return False
        finally:
            self.mutex.unlock()

    def write_set_point_water(self,value):
        self.mutex.lock()
        max_retries = 3
        try:
            for attempt in range(max_retries):
                try:
                    # ตรวจสอบ connection ก่อนเขียน
                    if not self.autoda_client or not self.autoda_client.is_socket_open():
                        if attempt < max_retries - 1:
                            print(f"Connection lost before writing setpoint water, retry {attempt + 1}")
                            self.mutex.unlock()
                            self.monitor_connection()
                            self.mutex.lock()
                            continue
                        else:
                            print(f"Failed to write setpoint water after {max_retries} retries")
                            return False
                    
                    address_register = 314 #register set point rock and sand
                    unlock_address = 5      # Address 5 (คือ Register 40006)
                    unlock_code = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
                    
                    unlock_result = self.autoda_client.write_register(address=unlock_address,value=unlock_code,device_id=self.water_id)
                    if unlock_result.isError():
                        print(f"Error unlocking water register, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    self.msleep(100)
                    register_values = self.int32_to_registers(value)
                    write_result = self.autoda_client.write_registers(address=address_register, values=register_values, device_id=self.water_id)
                    
                    if write_result.isError():
                        print(f"Error writing setpoint water, attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            self.msleep(500)
                            continue
                        else:
                            return False
                    
                    return True
                    
                except Exception as e:
                    print(f"Exception writing setpoint water, attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        self.msleep(500)
                    else:
                        return False
                        
        except Exception as e:
            print(f"Fatal exception in write_set_point_water: {e}")
            return False
        finally:
            self.mutex.unlock()
    
    def write_set_point_chemical(self, value):
        self.mutex.lock()
        try:
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
        except Exception as e:
            print(f"Exception in read_setpoint_chemical: {e}")
        finally:
            self.mutex.unlock()

    def run(self):
        last_monitor_time = time.time()
        connection_error_count = 0
        max_connection_errors = 10
        
        try:
            while self.running:
                try:
                    # ตรวจสอบ connection ทุก 10 วินาที
                    current_time = time.time()
                    if current_time - last_monitor_time > 10:
                        if not self.monitor_connection():
                            connection_error_count += 1
                            print(f"Connection monitor failed ({connection_error_count}/{max_connection_errors})")
                            
                            if connection_error_count >= max_connection_errors:
                                print(f"CRITICAL: AutoDA connection lost for {max_connection_errors} checks")
                                self.comport_error.emit([True, 'AutoDA'])
                                connection_error_count = 0
                        else:
                            connection_error_count = 0
                        
                        last_monitor_time = current_time
                    
                    # อ่านค่าน้ำหนักปกติ
                    self.read_weight_rock_and_sand()
                    self.read_cement_and_fyash()
                    self.read_water()
                    self.read_chemical()
                    
                except Exception as e:
                    print(f"Error in AutoDA Controller run loop: {e}")
                    self.msleep(1000)
                
        except Exception as e:
            print(f"Fatal Error in AutoDA Controller: {e}")
            
        finally:
            if self.autoda_client and self.autoda_client.is_socket_open():
                self.autoda_client.close()
                print("AutoDA Comport closed inside thread.")
                    
            self.msleep(100)

    def stop(self):
        self.running = False
        self.wait()

    def stop_controller(self):
        """เมธอดสำหรับสั่งหยุด Thread และปิด Port จากภายนอก"""
        print("Stop signal received by AUTODA_Controller.")
        self.running = False # บอกให้ loop ใน run() หยุดทำงาน


if __name__ == "__main__":
    app = QApplication(sys.argv)
    autoda_controller = AUTODA_Controller()
    autoda_controller.initialize_connections()
    time.sleep(2)
    autoda_controller.start()
    time.sleep(5)
    # test_rock_sand = 1975
    # test_cement_fyash = 280
    # test_water = 155
    # test_chemical = 2.9
    # autoda_controller.write_set_point_rock_and_sand(test_rock_sand)
    # time.sleep(0.5)
    # autoda_controller.write_set_point_cement_and_fyash(test_cement_fyash)
    # time.sleep(0.5)
    # autoda_controller.write_set_point_water(test_water)
    # time.sleep(0.5)
    # autoda_controller.write_set_point_chemical(test_chemical)
    # # print
    # time.sleep(2)
    # rock = autoda_controller.read_setpoint_rock_sand()
    # time.sleep(0.5)
    # cement = autoda_controller.read_setpoint_cement_fyash()
    # time.sleep(0.5)
    # water = autoda_controller.read_setpoint_water_work()
    # time.sleep(0.5)
    # chemical = autoda_controller.read_setpoint_chemical_work()
    # time.sleep(0.5)
    # print(f"Rock and Sand: {rock}")
    # print(f"Cement and Flyash: {cement}")
    # print(f"Water: {water}")
    # print(f"Chemical: {chemical}")
    # if rock == test_rock_sand and cement == test_cement_fyash and water == test_water and chemical == test_chemical:
    #     print("Setpoint match")
    #     autoda_controller.stop_controller()
    # else:
    #     print("Setpoint not match")
    autoda_controller.disconnect_to_autodac()
    autoda_controller.stop()
    time.sleep(3)
    sys.exit(0)
