#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import math
import time

def int32_to_registers(value):
    """
    แปลงค่า 32-bit (signed int) ให้เป็น list 16-bit 2 ค่า [High Word, Low Word]
    """
    if value < 0:
        value = (1 << 32) + value
    
    high_word = (value >> 16) & 0xFFFF
    low_word = value & 0xFFFF
    
    return [high_word, low_word]

SERIAL_PORT = 'COM7' 
BAUD_RATE = 9600
SLAVE_ID = 2 
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
        
        rr_write = client.write_registers(
            address=TARGET_ADDRESS,
            values=register_values,
            device_id=SLAVE_ID 
        )
        
        if rr_write.isError():
            print(f"!! ข้อผิดพลาดในการเขียนค่า: {rr_write}")
        else:
            print("เขียนค่า 32-bit สำเร็จ!")

except Exception as e:
    print(f"!! เกิดข้อผิดพลาด: {e}")

finally:
    if client.is_socket_open():
        client.close()
        print("\nปิดการเชื่อมต่อ Modbus แล้ว")
    else:
        print("\nการเชื่อมต่อไม่ได้ถูกเปิด (หรือปิดไปแล้ว)")