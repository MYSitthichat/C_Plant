from pymodbus.client import ModbusSerialClient
import time


# --- ฟังก์ชันตัวช่วย (จากไฟล์ test_autoda2015_read_wieght_float.py) ---
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


class test_autoda2015:
    def __init__(self):
        # --- ข้อมูล Register สำหรับ Autoda ---
        self.SLAVE_ID = 4
        self.ADDRESS_DIV = 88  # Register 40089 (Gain value / div)
        self.divisor = 1  # ตัวหารสำหรับแปลงค่าทศนิยม
        self.client = None
    
    def int32_to_registers(self, value):
        """
        แปลงค่า 32-bit (signed int) ให้เป็น list 16-bit 2 ค่า [High Word, Low Word]
        """
        if value < 0:
            value = (1 << 32) + value
        high_word = (value >> 16) & 0xFFFF
        low_word = value & 0xFFFF
        return [high_word, low_word]
    
    def float_to_int_with_divisor(self, float_value):
        """
        แปลงค่าทศนิยมให้เป็น integer โดยใช้ตัวหาร (divisor)
        """
        return int(float_value * self.divisor)
    
    
    def connect_client(self, comport):
        self.client = ModbusSerialClient(
            port=comport,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=3
        )
        if self.client.connect():
            print(f"Successfully connected to {comport}")
            # อ่านค่าการตั้งค่าทศนิยมทันทีหลังจากเชื่อมต่อ
            self.read_decimal_setting()
        else:
            raise Exception(f"Failed to connect to {comport}")
    
    def read_decimal_setting(self):
        """
        อ่านค่าการตั้งค่าทศนิยมจาก Autoda (Register 40089)
        """
        try:
            print("กำลังอ่านค่าการตั้งค่าทศนิยม (Address 88)...")
            rr_div = self.client.read_holding_registers(
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
                print(f"เครื่องถูกตั้งค่าไว้ที่: {self.divisor} (หมายถึง ทศนิยม {len(str(self.divisor))-1} ตำแหน่ง)")
                return True
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอ่านค่าทศนิยม: {e}")
            self.divisor = 1  # ใช้ค่าเริ่มต้น
            return False

    def disconnect_client(self):    
        if self.client:
            self.client.close()

    def unlock_register(self):
        UNLOCK_ADDRESS = 5      # Address 5 (คือ Register 40006)
        UNLOCK_CODE = 0x5AA5    # ค่า Hex 0x5AA5 (23205)
        print("กำลัง Unlock Register...")
        result = self.client.write_register(address=UNLOCK_ADDRESS, value=UNLOCK_CODE, device_id=self.SLAVE_ID)
        if result.isError():
            print(f"!! ข้อผิดพลาดในการ Unlock: {result}")
            return False
        else:
            print("Unlock Register สำเร็จ")
            time.sleep(0.1)
            return True

    def write_value(self, value):
        """
        เขียนค่า integer แบบเดิม (32-bit)
        """
        address_register = 314
        # address_register = 90
        try:
            if not self.client:
                raise Exception("No client connection available")
            else:
                print("เชื่อมต่อสำเร็จ")
                value_to_write = value
                register_values = self.int32_to_registers(value_to_write)
                print(f"Writing 32-bit value: {value_to_write} as registers: {register_values}")
                rr_write = self.client.write_registers(address=address_register, values=register_values, device_id=self.SLAVE_ID)
                if rr_write.isError():
                    print(f"!! error to write value: {rr_write}")
                    return False
                else:
                    print("Write 32-bit value successful!")
                    return True

        except Exception as e:
            print(f"!! error occurred: {e}")
            return False
    
    def write_float_value(self, float_value, address_register=314):
        """
        เขียนค่าทศนิยมไปที่ Autoda โดยแปลงตาม divisor ที่อ่านได้
        """
        try:
            if not self.client:
                raise Exception("No client connection available")
            
            # แปลงค่าทศนิยมเป็น integer ตาม divisor
            int_value = self.float_to_int_with_divisor(float_value)
            
            print(f"\n--- การเขียนค่าทศนิยม ---")
            print(f"ค่าทศนิยมที่ต้องการเขียน: {float_value}")
            print(f"Divisor ปัจจุบัน: {self.divisor}")
            print(f"ค่า Integer ที่จะเขียน: {int_value}")
            
            # แปลงเป็น 32-bit registers
            register_values = self.int32_to_registers(int_value)
            print(f"Register values: {register_values}")
            
            # เขียนค่าลง register
            rr_write = self.client.write_registers(
                address=address_register, 
                values=register_values, 
                device_id=self.SLAVE_ID
            )
            
            if rr_write.isError():
                print(f"!! ข้อผิดพลาดในการเขียนค่า: {rr_write}")
                return False
            else:
                print("เขียนค่าทศนิยมสำเร็จ!")
                return True

        except Exception as e:
            print(f"!! เกิดข้อผิดพลาด: {e}")
            return False

if __name__ == "__main__":
    print("=== เริ่มต้นการทดสอบการเขียนค่า Setpoint แบบทศนิยมไปที่ Autoda ===\n")
    
    tester = test_autoda2015()
    
    try:
        # เชื่อมต่อ
        tester.connect_client(comport="COM7")
        time.sleep(1)
        
        # Unlock register
        if tester.unlock_register():
            time.sleep(0.5)
            
            # ทดสอบเขียนค่าทศนิยม
            print("\n=== ทดสอบการเขียนค่าทศนิยม ===")
            
            # ทดสอบค่าต่างๆ
            test_values = [1.0, 1.5, 1.9, 2.3, 2.7]
            
            for float_val in test_values:
                print(f"\n--- ทดสอบค่า {float_val} ---")
                success = tester.write_float_value(float_val)
                if success:
                    print(f"✓ เขียนค่า {float_val} สำเร็จ")
                else:
                    print(f"✗ เขียนค่า {float_val} ล้มเหลว")
                time.sleep(15)
            
            # ทดสอบเขียนค่าแบบเดิม (integer) เพื่อเปรียบเทียบ
            print("\n=== ทดสอบการเขียนค่าแบบเดิม (Integer) ===")
            integer_value = 150
            print(f"\n--- ทดสอบค่า {integer_value} (แบบเดิม) ---")
            success = tester.write_value(integer_value)
            if success:
                print(f"✓ เขียนค่า {integer_value} (แบบเดิม) สำเร็จ")
            else:
                print(f"✗ เขียนค่า {integer_value} (แบบเดิม) ล้มเหลว")
                
        else:
            print("ไม่สามารถ Unlock Register ได้")
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    
    finally:
        tester.disconnect_client()
        print("\nปิดการเชื่อมต่อเรียบร้อย")
        print("=== การทดสอบเสร็จสิ้น ===")