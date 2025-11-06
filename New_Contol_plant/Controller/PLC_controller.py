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
        self.reading_state = True
        self.write_state = False
        self.write_success = False
        
        self.device_timeout = {}  
        self.last_communication_time = {} 
        self.communication_delay = 50
        self.error_count = {}
        self.max_error_count = 3

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
                        self.baudrate = self.config.get('BAUDRATE_PLC', '')
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
        
        reduced_timeout = min(timeout, 1)  # ไม่เกิน 1 วินาที
        
        self.plc_client = ModbusSerialClient(
            port=plc_port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stop_bits,
            bytesize=data_bits,
            timeout=reduced_timeout
        )
        try:
            if self.plc_client.connect():
                self.comport_error.emit([False, 'PLC'])
                self.initialize_device_management()
            else:
                self.comport_error.emit([True, 'PLC'])
        except Exception as e:
            self.comport_error.emit([True, 'PLC'])
    
    def initialize_device_management(self):
        devices = [self.PLC_id_weight, self.PLC_id_conditioner]
        current_time = time.time()
        
        for device_id in devices:
            if device_id: 
                self.device_timeout[device_id] = current_time
                self.last_communication_time[device_id] = current_time
                self.error_count[device_id] = 0

    def disconnect_to_plc(self):
        self.plc_client.close()
    
    def safe_modbus_operation(self, operation_func, device_id, operation_name="unknown"):
        try:
            current_time = time.time()
            if device_id in self.error_count and self.error_count[device_id] >= self.max_error_count:
                if current_time - self.last_communication_time.get(device_id, 0) < 5:  # รอ 5 วินาที
                    return None
                else:
                    self.error_count[device_id] = 0
            
            last_comm_time = self.last_communication_time.get(device_id, 0)
            if current_time - last_comm_time < (self.communication_delay / 1000):
                return None
            result = operation_func()
            self.last_communication_time[device_id] = current_time
            if device_id in self.error_count:
                self.error_count[device_id] = 0
                
            return result
            
        except Exception as e:
            if device_id not in self.error_count:
                self.error_count[device_id] = 0
            self.error_count[device_id] += 1
            
            # print(f"Error in {operation_name} for device {device_id}: {e} (Error count: {self.error_count[device_id]})")
            return None
    
    def safe_write_coil(self, address, value, device_id, operation_name="write_coil"):
        def write_operation():
            return self.plc_client.write_coil(address=address, value=value, device_id=device_id)
        
        result = self.safe_modbus_operation(write_operation, str(device_id), operation_name)
        if result and result.isError():
            print(f"Failed to write coil {address} to device {device_id}: {result}")
            return False
        return result is not None
    
    def loading_rock1(self, status):
        if status == "start":
            self.safe_write_coil(address=0, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_rock1_start")
        elif status == "stop":
            self.safe_write_coil(address=0, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_rock1_stop")
    
    def loading_sand(self, status):
        if status == "start":
            self.safe_write_coil(address=1, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_sand_start")
        elif status == "stop":
            self.safe_write_coil(address=1, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_sand_stop")
    
    def loading_rock2(self, status):
        if status == "start":
            self.safe_write_coil(address=2, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_rock2_start")
        elif status == "stop":
            self.safe_write_coil(address=2, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_rock2_stop")
    
    def loading_cement(self, status):
        if status == "start":
            self.safe_write_coil(address=3, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_cement_start")
        elif status == "stop":
            self.safe_write_coil(address=3, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_cement_stop")
    
    def loading_flyash(self, status):
        if status == "start":
            self.safe_write_coil(address=4, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_flyash_start")
        elif status == "stop":
            self.safe_write_coil(address=4, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_flyash_stop")
    
    def loading_water(self, status):
        if status == "start":
            self.safe_write_coil(address=5, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_water_start")
        elif status == "stop":
            self.safe_write_coil(address=5, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_water_stop")
    
    def loading_chemical_1(self, status):
        if status == "start":
            self.safe_write_coil(address=6, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_chemical_1_start")
        elif status == "stop":
            self.safe_write_coil(address=6, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_chemical_1_stop")

    def loading_chemical_2(self, status):
        if status == "start":
            self.safe_write_coil(address=7, value=1, device_id=int(self.PLC_id_weight), operation_name="loading_chemical_2_start")
        elif status == "stop":
            self.safe_write_coil(address=7, value=0, device_id=int(self.PLC_id_weight), operation_name="loading_chemical_2_stop")

    def start_vibrater_rock_and_sand(self, status):
        if status == "start":
            self.safe_write_coil(address=0, value=1, device_id=int(self.PLC_id_conditioner), operation_name="vibrater_rock_sand_start")
        elif status == "stop":
            self.safe_write_coil(address=0, value=0, device_id=int(self.PLC_id_conditioner), operation_name="vibrater_rock_sand_stop")

    def converyer_midle(self, status):
        if status == "start":
            success = self.safe_write_coil(address=1, value=1, device_id=int(self.PLC_id_conditioner), operation_name="converyer_midle_start")
            self.write_success = success
        elif status == "stop":
            success = self.safe_write_coil(address=1, value=0, device_id=int(self.PLC_id_conditioner), operation_name="converyer_midle_stop")
            self.write_success = success

    def converyer_top(self, status):
        if status == "start":
            self.safe_write_coil(address=2, value=1, device_id=int(self.PLC_id_conditioner), operation_name="converyer_top_start")
        elif status == "stop":
            self.safe_write_coil(address=2, value=0, device_id=int(self.PLC_id_conditioner), operation_name="converyer_top_stop")

    def mixer(self, status):
        if status == "start":
            self.safe_write_coil(address=3, value=1, device_id=int(self.PLC_id_conditioner), operation_name="mixer_start")
        elif status == "stop":
            self.safe_write_coil(address=3, value=0, device_id=int(self.PLC_id_conditioner), operation_name="mixer_stop")
    
    def vibrater_cement_and_fyash(self, status):
        if status == "start":
            self.safe_write_coil(address=4, value=1, device_id=int(self.PLC_id_conditioner), operation_name="vibrater_cement_flyash_start")
        elif status == "stop":
            self.safe_write_coil(address=4, value=0, device_id=int(self.PLC_id_conditioner), operation_name="vibrater_cement_flyash_stop")
    
    def vale_water(self, status):
        if status == "start":
            self.safe_write_coil(address=5, value=1, device_id=int(self.PLC_id_conditioner), operation_name="vale_water_start")
        elif status == "stop":
            self.safe_write_coil(address=5, value=0, device_id=int(self.PLC_id_conditioner), operation_name="vale_water_stop")
    
    def vale_cement_and_fyash(self, status):
        if status == "start":
            self.safe_write_coil(address=6, value=1, device_id=int(self.PLC_id_conditioner), operation_name="vale_cement_flyash_start")
        elif status == "stop":
            self.safe_write_coil(address=6, value=0, device_id=int(self.PLC_id_conditioner), operation_name="vale_cement_flyash_stop")
    
    def vale_mixer(self, status):
        if status == "start":
            self.safe_write_coil(address=7, value=1, device_id=int(self.PLC_id_conditioner), operation_name="vale_mixer_start")
        elif status == "stop":
            self.safe_write_coil(address=7, value=0, device_id=int(self.PLC_id_conditioner), operation_name="vale_mixer_stop")
    
    def pump_chemical_up(self, status):
        if status == "start":
            self.safe_write_coil(address=8, value=1, device_id=int(self.PLC_id_conditioner), operation_name="pump_chemical_start")
        elif status == "stop":
            self.safe_write_coil(address=8, value=0, device_id=int(self.PLC_id_conditioner), operation_name="pump_chemical_stop")

    def reading_finish_load_rock_and_sand(self):
        def read_operation():
            return self.plc_client.read_coils(address=100, count=1, device_id=int(self.PLC_id_weight))
        
        result = self.safe_modbus_operation(read_operation, self.PLC_id_weight, "read_rock_sand_status")
        if result and not result.isError():
            self.status_loading_rock_and_sand.emit(result.bits[0])
        
    def reading_finish_load_cement_and_fyash(self):
        def read_operation():
            return self.plc_client.read_coils(address=110, count=1, device_id=int(self.PLC_id_weight))
        
        result = self.safe_modbus_operation(read_operation, self.PLC_id_weight, "read_cement_flyash_status")
        if result and not result.isError():
            self.status_loading_cement_and_fyash.emit(result.bits[0])

    def reading_finish_load_water(self):
        def read_operation():
            return self.plc_client.read_coils(address=120, count=1, device_id=int(self.PLC_id_weight))
        
        result = self.safe_modbus_operation(read_operation, self.PLC_id_weight, "read_water_status")
        if result and not result.isError():
            self.status_loading_water.emit(result.bits[0])

    def reading_finish_load_chemical(self):
        def read_operation():
            return self.plc_client.read_coils(address=130, count=1, device_id=int(self.PLC_id_weight))
        
        result = self.safe_modbus_operation(read_operation, self.PLC_id_weight, "read_chemical_status")
        if result and not result.isError():
            self.status_loading_chemical.emit(result.bits[0])

    def off_all_device(self):
        self.loading_rock1("stop")
        time.sleep(0.1)
        self.loading_sand("stop")
        time.sleep(0.1)
        self.loading_rock2("stop")
        time.sleep(0.1)
        self.loading_cement("stop")
        time.sleep(0.1)
        self.loading_flyash("stop")
        time.sleep(0.1)
        self.loading_water("stop")
        time.sleep(0.1)
        self.loading_chemical_1("stop")
        time.sleep(0.1)
        self.loading_chemical_2("stop")
        time.sleep(0.1)
        self.start_vibrater_rock_and_sand("stop")
        time.sleep(0.1)
        self.converyer_midle("stop")
        time.sleep(0.1)
        self.converyer_top("stop")
        time.sleep(0.1)
        self.mixer("stop")
        time.sleep(0.1)
        self.vibrater_cement_and_fyash("stop")
        time.sleep(0.1)
        self.vale_water("stop")
        time.sleep(0.1)
        self.vale_cement_and_fyash("stop")
        time.sleep(0.1)
        self.vale_mixer("stop")
        time.sleep(0.1)
        self.pump_chemical_up("stop")
        time.sleep(0.1)

    def run(self):
        read_functions = [
            self.reading_finish_load_rock_and_sand,
            self.reading_finish_load_cement_and_fyash,
            self.reading_finish_load_water,
            self.reading_finish_load_chemical
        ]
        read_index = 0 
        
        while self.running:
            try:
                if self.reading_state == True:
                    if read_functions:
                        read_functions[read_index]()
                        read_index = (read_index + 1) % len(read_functions)
                        self.msleep(10)
                else:
                    pass
                # if self.write_state == True:
                #     if self.write_success == True:
                #         self.write_state = False
                #         self.write_success = False
                #         self.reading_state = True
                    
            except Exception as e:
                print(f"Error in PLC Controller: {e}")
                self.msleep(50)
            self.msleep(55)

    def set_communication_parameters(self, communication_delay=50, max_error_count=3, timeout_seconds=1):
        self.communication_delay = communication_delay
        self.max_error_count = max_error_count
        if hasattr(self, 'plc_client') and self.plc_client:
            self.plc_client.timeout = timeout_seconds
            print(f"Updated communication parameters - Delay: {communication_delay}ms, Max errors: {max_error_count}, Timeout: {timeout_seconds}s")
    
    def get_communication_status(self):
        status = {}
        current_time = time.time()
        for device_id, error_count in self.error_count.items():
            last_comm = self.last_communication_time.get(device_id, 0)
            time_since_last = current_time - last_comm
            
            status[device_id] = {
                'error_count': error_count,
                'last_communication': last_comm,
                'seconds_since_last_comm': round(time_since_last, 2),
                'is_active': error_count < self.max_error_count
            }
        return status
    
    def reset_device_errors(self, device_id=None):
        if device_id:
            if device_id in self.error_count:
                self.error_count[device_id] = 0
                print(f"Reset error count for device {device_id}")
        else:
            for device in self.error_count:
                self.error_count[device] = 0

    def stop(self):
        self.running = False
        self.wait()
        status = self.get_communication_status()
        for device_id, stats in status.items():
            # print(f"Device {device_id}: Errors={stats['error_count']}, Last comm={stats['seconds_since_last_comm']}s ago")
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plc_controller = PLC_Controller()
    sys.exit(0)