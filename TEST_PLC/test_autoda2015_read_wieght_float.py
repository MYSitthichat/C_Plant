from PySide6.QtCore import QThread, Signal, QObject
from pymodbus.client import ModbusSerialClient
import time


# --- ฟังก์ชันตัวช่วย (จากคำตอบที่แล้ว) ---
def get_divisor_from_code(div_code):
    """
    แปลงรหัส 'div' ที่อ่านได้ (จาก 40089) ให้เป็นตัวหาร
    """
    div_map = {
        12: 1,     # 0 ตำแหน่ง (ค่า 1) 
        9: 10,     # 1 ตำแหน่ง (ค่า 0.1) 
        6: 100,    # 2 ตำแหน่ง (ค่า 0.01) 
        3: 1000,   # 3 ตำแหน่ง (ค่า 0.001) 
        0: 10000   # 4 ตำแหน่ง (ค่า 0.0001) 
    }
    # คืนค่าตัวหาร (เช่น 100) ถ้าไม่เจอก็คืนค่า 1 (ไม่หาร)
    return div_map.get(div_code, 1) 


class Read_PLC_Thread(QThread, QObject):
    data_check = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.write_state = False
        self.write_success = False
        self.read_state = True
        self.delay_time_for_write = 50
        
        # --- ข้อมูล Register สำหรับ Autoda ---
        self.SLAVE_ID = 4  # Device ID ของ Autoda
        self.ADDRESS_DIV = 88  # Register 40089 (Gain value / div)
        self.ADDRESS_WEIGHT = 81  # Register สำหรับอ่านน้ำหนัก
        self.divisor = 1  # ตัวหารสำหรับแปลงค่าทศนิยม
        
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
    
    def read_decimal_setting(self):
        """
        อ่านค่าการตั้งค่าทศนิยมจาก Autoda (Register 40089)
        """
        try:
            print("กำลังอ่านค่าการตั้งค่าทศนิยม (Address 88)...")
            rr_div = self.plc_device_device.read_holding_registers(
                address=self.ADDRESS_DIV,
                count=1,
                device_id=self.SLAVE_ID
            )
            
            if rr_div.isError():
                print(f"!! ข้อผิดพลาดในการอ่าน Address 88: {rr_div}")
                return False
            else:
                div_code = rr_div.registers[0]  # เช่น อ่านได้ค่า 6
                self.divisor = get_divisor_from_code(div_code)  # แปลงเป็น 100

                print("\n--- ผลการอ่านค่าทศนิยม ---")
                print(f"รหัส 'div' ที่อ่านได้จากเครื่อง: {div_code}")
                print(f"เครื่องถูกตั้งค่าไว้ที่: {self.divisor} (หมายถึง {1/self.divisor} หรือ ทศนิยม {len(str(self.divisor))-1} ตำแหน่ง)")
                return True
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอ่านค่าทศนิยม: {e}")
            return False
    
    def read_weight_float(self, device_id=None, address=None):
        """
        อ่านค่าน้ำหนักแบบทศนิยมจาก Autoda
        """
        try:
            device_id = device_id or self.SLAVE_ID
            address = address or self.ADDRESS_WEIGHT
            
            read_weight = self.plc_device_device.read_holding_registers(
                address=address, 
                count=1, 
                device_id=device_id
            )
            
            if read_weight.isError():
                print(f"!! ข้อผิดพลาดในการอ่านน้ำหนัก: {read_weight}")
                return None
                
            raw_value = int(read_weight.registers[0])
            
            # แปลงค่า signed integer (16-bit)
            if raw_value > 32767:
                signed_value = raw_value - 65536
            else:
                signed_value = raw_value
            
            # แปลงเป็นค่าทศนิยม
            float_value = signed_value / self.divisor
            
            return float_value
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอ่านน้ำหนักแบบทศนิยม: {e}")
            return None
        
    def stop(self):
        self.running = False
        self.wait()  # Wait for thread to finish

    def run(self):
        # อ่านค่าการตั้งค่าทศนิยมเมื่อเริ่มต้น
        if self.plc_device_device:
            self.read_decimal_setting()
        
        while self.running:
            if self.read_state == True:
                try:
                    # ใช้ฟังก์ชันใหม่สำหรับอ่านค่าแบบทศนิยม
                    weight_float_rock_and_sand = self.read_weight_float(device_id=4, address=81)
                    
                    if weight_float_rock_and_sand is not None:
                        print(f"Weight Rock&Sand (Float): {weight_float_rock_and_sand:.3f}")
                    
                    # ตัวอย่างการอ่านค่าเพิ่มเติม (ถ้าต้องการ)
                    # weight_float_cement_and_flyash = self.read_weight_float(device_id=4, address=82)
                    # if weight_float_cement_and_flyash is not None:
                    #     print(f"Weight Cement&Flyash (Float): {weight_float_cement_and_flyash:.3f}")

                except Exception as e:
                    print(f"Error reading PLC: {e}")
                    pass
                self.msleep(100)  

    def stop(self):
        self.running = False
        self.wait()
    
if __name__ == '__main__':
    print("=== เริ่มต้นการทดสอบการอ่านค่า Autoda แบบทศนิยม ===")
    
    main_app = Read_PLC_Thread()
    main_app.connect_comport_open('COM7')
    
    if main_app.plc_device_device:
        print("เชื่อมต่อ PLC สำเร็จ")
        main_app.start()
        
        # รันการทดสอบ 50 รอบ (25 วินาที)
        for i in range(50):
            time.sleep(0.5)
            if i == 10:  # ทดสอบอ่านค่าทศนิยมอีกครั้งหลังจาก 5 วินาที
                print("\n=== ทดสอบอ่านค่าการตั้งค่าทศนิยมอีกครั้ง ===")
                main_app.read_decimal_setting()
        
        main_app.stop()
        main_app.disconnect_comport()
        print("ปิดการเชื่อมต่อเรียบร้อย")
    else:
        print("ไม่สามารถเชื่อมต่อ PLC ได้")