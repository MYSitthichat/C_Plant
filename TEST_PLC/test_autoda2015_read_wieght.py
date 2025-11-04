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

    def run(self):
        while self.running:
            if self.read_state == True:
                try:
                    read_weight_rock_and_sand = self.plc_device_device.read_holding_registers(address=81, count=1, device_id=8)
                    read_weight_cement_and_flyash = self.plc_device_device.read_holding_registers(address=81, count=1, device_id=6)

                    raw_value_rock_and_sand = int(read_weight_rock_and_sand.registers[0])
                    raw_value_cement_and_flyash = int(read_weight_cement_and_flyash.registers[0])

                    if raw_value_rock_and_sand > 32767:
                        weight_value_rock_and_sand = raw_value_rock_and_sand - 65536
                    else:
                        weight_value_rock_and_sand = raw_value_rock_and_sand

                    if raw_value_cement_and_flyash > 32767:
                        weight_value_cement_and_flyash = raw_value_cement_and_flyash - 65536
                    else:
                        weight_value_cement_and_flyash = raw_value_cement_and_flyash

                    print(f"Weight Rock&Sand: {weight_value_rock_and_sand} | Weight Cement&Flyash: {weight_value_cement_and_flyash}")
                    # self.msleep(100)
                except Exception as e:
                    print(f"Error reading PLC: {e}")
                    pass
                self.msleep(100)  

    def stop(self):
        self.running = False
        self.wait()
    
if __name__ == '__main__':
    main_app = Read_PLC_Thread()
    main_app.connect_comport_open('COM7')
    main_app.start()
    for i in range(100):
        time.sleep(0.5)
    main_app.stop()
    main_app.disconnect_comport()