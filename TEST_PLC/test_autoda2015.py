from pymodbus.client import ModbusSerialClient
import time


<<<<<<< HEAD
class test_autoda2015:
    def int32_to_registers(self, value):
        """
        แปลงค่า 32-bit (signed int) ให้เป็น list 16-bit 2 ค่า [High Word, Low Word]
        """
        if value < 0:
            value = (1 << 32) + value
=======
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600
<<<<<<< HEAD
SLAVE_ID = 2 
=======
SLAVE_ID = 3
>>>>>>> f106f4c655a8825747e17bd736a51912e61fd0db
UNLOCK_ADDRESS = 5      # Address 5 (คือ Register 40006)
UNLOCK_CODE = 0x5AA5    # ค่า Hex 0x5AA5 (23205) 

print(f"กำลังพยายามเชื่อมต่อกับ {SERIAL_PORT}...")
client = ModbusSerialClient(
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=3 
)

try:
    if not client.connect():
        print(f"!! ข้อผิดพลาด: ไม่สามารถเปิดพอร์ต {SERIAL_PORT} ได้")
        raise Exception("Connection Failed")

    print("เชื่อมต่อสำเร็จ!")
    print(f"กำลังส่งรหัสปลดล็อค (0x5AA5) ไปยัง Address {UNLOCK_ADDRESS} (Slave ID: {SLAVE_ID})...")
    rr_unlock = client.write_register(
        address=UNLOCK_ADDRESS,
        value=UNLOCK_CODE,
        device_id=SLAVE_ID
    )

    if rr_unlock.isError():
        print(f"!! ข้อผิดพลาดในการปลดล็อค: {rr_unlock}")
        print(f"!! (ตรวจสอบว่า SLAVE_ID = {SLAVE_ID} ถูกต้องหรือไม่)")
    else:
        print("ปลดล็อคสำเร็จ!")
        time.sleep(0.1) 

        # (ตัวอย่างนี้เขียนที่ 40315 Upper limit 0)
        TARGET_ADDRESS = 314 
        value_to_write = 200
        register_values = int32_to_registers(value_to_write)  # [0, 200]

        print(f"กำลังเขียนค่า 32-bit {register_values} ไปยัง Address {TARGET_ADDRESS}")
>>>>>>> c60322bd4b5d54765d69df30b7db47094d61901f
        
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
            print(f"Connecting to {comport}...")

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
                print("เชื่อมต่อสำเร็จ")
                value_to_write = value
                register_values = self.int32_to_registers(value_to_write)
                rr_write = self.client.write_registers(address=address_register,values=register_values,device_id=SLAVE_ID)
                if rr_write.isError():
                    print(f"!! error to write value: {rr_write}")
                else:
                    print("Write 32-bit value successful!")

        except Exception as e:
            print(f"!! error occurred: {e}")

if __name__ == "__main__":
    tester = test_autoda2015()
    tester.connect_client(comport="COM7")
    time.sleep(2)
    tester.unlock_register()
    time.sleep(0.5)
    i = 0
    value_target = 0
    for i in range(5):
        print(f"Writing value: {value_target}")
        tester.write_value(value=value_target)
        value_target += 50
        time.sleep(5)
    tester.disconnect_client()
    print("Test finished")