from PySide6.QtCore import QThread, Signal, QObject
from pymodbus.client import ModbusSerialClient
import time 


class Read_PLC_Thread(QThread, QObject):
    data_check = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.write_state = False
        self.write_success = False
        self.read_state = True
        self.delay_time_for_write = 50
        
    def connect_comport_open(self, plc_device):
        client = ModbusSerialClient(
            port=plc_device,
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1
        )
        if client.connect():
            self.plc_device_device = client
            self.running = True
            # print("PLC connected")
        else:
            self.plc_device_device = None
            # print(f"Failed to connect to PLC on port {plc_device}")

    def disconnect_comport(self):
        self.running = False
        if self.plc_device_device and hasattr(self.plc_device_device, 'close'):
            self.plc_device_device.close()
        self.plc_device_device = None
        
    def stop(self):
        self.running = False
        self.wait()  # Wait for thread to finish

    def control_rock_and_sand_write(self,type,status):
        self.write_state = False
        if type == "rock1":
            self.address_register = 0
            self.status_coil = status
            self.write_state = True
        elif type == "sand1":
            self.address_register = 1
            self.status_coil = status
            self.write_state = True
        elif type == "rock2":
            self.address_register = 2
            self.status_coil = status
            self.write_state = True
        elif type == "sand2":
            self.address_register = 3
            self.status_coil = status
            self.write_state = True

    def off_all_coil(self):
        for address in range(4):
            self.plc_device_device.write_coil(address=address, value=False, device_id=1)
            time.sleep(0.1)

    def run(self):
        while self.running:
            if self.write_state == True:
                # print("write plc")
                # print(f"Address: {self.address_register}, Status: {self.status_coil}")
                self.plc_device_device.write_coil(address=self.address_register,value=self.status_coil,device_id=1)
                self.msleep(100)
                self.write_state = False
                self.read_state = True
                # print("write plc finish")
                self.msleep(100)
            if self.read_state == True:
                try:
                    read_status_m100 = self.plc_device_device.read_coils(address=100, count=1, device_id=1)
                    if read_status_m100.bits[0] == True:
                        self.data_check.emit(True)
                        # print("Silo Full Detected")
                    else:
                        self.data_check.emit(False)
                        # print("Silo Not Full")
                    # print(f"Read M100: {read_status_m100.bits[0]}")
                    self.msleep(100)
                except Exception as e:
                    print(f"Error reading PLC: {e}")
                    pass
                self.msleep(100)  

    def stop(self):
        self.running = False
        self.wait()
    
if __name__ == '__main__':
    main_app = Read_PLC_Thread()
    main_app.connect_comport_open('COM9')
    main_app.start()
    for i in range(10):
        time.sleep(1)
    main_app.stop()
    main_app.disconnect_comport()