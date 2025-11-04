from pymodbus.client import ModbusSerialClient
from PySide6.QtCore import QObject, Slot, QTimer
from PySide6.QtWidgets import QApplication
import time
import sys
from PLC_controller import Read_PLC_Thread

class autoda2015_rock_and_sand_monitor(QObject):
    def __init__(self):
        super(autoda2015_rock_and_sand_monitor, self).__init__()
        self.plc_controller = Read_PLC_Thread()
        self.plc_controller.data_check.connect(self.on_data_check)
        self.client = None
        self.m100_status = False
        self.test_counter = 0
        self.max_test_iterations = 100
        self.test_values = []
        self.current_test_index = 0
        self.waiting_for_m100 = False
        self.test_completed = False

    @Slot(bool)
    def on_data_check(self, status):
        self.m100_status = status
        print(f"M100 Status: {status}")
        
        # ถ้ารอ M100 = True และได้รับสัญญาณ True
        if self.waiting_for_m100 and status == True:
            current_test = self.test_values[self.current_test_index]
            print(f"✓ M100 detected TRUE for {current_test['name']} (value: {current_test['value']})")
            
            self.plc_controller.control_rock_and_sand_write(current_test['type'], False)
            print(f"✓ Deactivated PLC coil: {current_test['type']}")
            
            self.waiting_for_m100 = False
            self.current_test_index += 1
            
            if self.current_test_index >= len(self.test_values):
                print("\n🎉 All test values completed successfully!")
                self.test_completed = True
                self.plc_controller.off_all_coil()
                self.stop_test()
            else:
                # ส่งค่าถัดไป
                print(f"Moving to next test...")
                QTimer.singleShot(2000, self.send_next_value)  # รอ 2 วินาที แล้วส่งค่าถัดไป

    def int32_to_registers(self, value):
        if value < 0:
            value = (1 << 32) + value
        high_word = (value >> 16) & 0xFFFF
        low_word = value & 0xFFFF
        return [high_word, low_word]
    
    def connect_client(self, comport):
        self.client = ModbusSerialClient(
            port=comport,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=3
        )
        if not self.client:
            raise Exception("Client Creation Failed")
        else:
            pass

    def disconnect_client(self):    
        if self.client:
            self.client.close()

    def unlock_register(self):
        UNLOCK_ADDRESS = 5      # Address 5 (คือ Register 40006)
        UNLOCK_CODE = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        self.client.write_register(address=UNLOCK_ADDRESS,value=UNLOCK_CODE,device_id=5)
        time.sleep(0.1)

    def write_value(self,value):
        SLAVE_ID = 5
        address_register = 314
        try:
            if not self.client:
                raise Exception("No client connection available")
            else:
                value_to_write = value
                register_values = self.int32_to_registers(value_to_write)
                rr_write = self.client.write_registers(address=address_register,values=register_values,device_id=SLAVE_ID)
                if rr_write.isError():
                    pass
        except Exception as e:
            print(f"!! error occurred: {e}")

    def send_next_value(self):
        """ส่งค่าถัดไปในลิสต์"""
        if self.current_test_index < len(self.test_values):
            current_test = self.test_values[self.current_test_index]
            current_value = current_test["value"]
            current_type = current_test["type"]
            current_name = current_test["name"]
            self.unlock_register()
            self.write_value(current_value)
            time.sleep(2)
            self.plc_controller.control_rock_and_sand_write(current_type, True)
            time.sleep(1)
            self.waiting_for_m100 = True
            print(f"Waiting for M100 to become TRUE for {current_name} , {current_value}")

    def run_test(self):
        ROCK1 = 100
        SAND1 = 200
        ROCK2 = 300
        SAND2 = 400
        self.test_values = [
            {"value": ROCK1, "type": "rock1", "name": "ROCK1"},
            {"value": SAND1, "type": "sand1", "name": "SAND1"}, 
            {"value": ROCK2, "type": "rock2", "name": "ROCK2"},
            {"value": SAND2, "type": "sand2", "name": "SAND2"}
        ]
        self.current_test_index = 0
        self.waiting_for_m100 = False
        self.test_completed = False
        self.connect_client(comport="COM7")
        self.plc_controller.connect_comport_open('COM9')
        self.plc_controller.start()
        print("Waiting for PLC connection...")
        time.sleep(2) 
        self.send_next_value()

    def stop_test(self):
        print("Stopping test...")
        self.test_completed = True
        self.disconnect_client()
        self.plc_controller.stop()
        
        # ใช้ QTimer เพื่อให้ app quit หลังจาก event loop ทำงานเสร็จ
        QTimer.singleShot(500, QApplication.quit)

if __name__ == "__main__":
    # สร้าง QApplication สำหรับ event loop
    app = QApplication(sys.argv)
    
    # สร้าง monitor object
    autoda_monitor = autoda2015_rock_and_sand_monitor()
    
    # เริ่มการทดสอบ
    autoda_monitor.run_test()
    # เริ่ม event loop
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        autoda_monitor.stop_test()