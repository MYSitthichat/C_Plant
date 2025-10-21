from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
import time

# comport = '/dev/ttyS0'
comport = '/dev/ttyUSB1'
# สังเกตว่าแก้ stopbitd เป็น stopbits
client = ModbusClient(method='rtu', port=comport, stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=1)
connection = client.connect()

if not connection:
    print("Failed to connect!")
else:
    print("Connected to Modbus device.")
    main_state = 0
    while True:
        if main_state == 0:
            print("state 0: Reading holding registers...")
            
            # อ่านค่าจาก Modbus device
            modbus_result = client.read_holding_registers(address=0, count=1, unit=8)
            
            # --- จุดสำคัญ: ตรวจสอบ Error ก่อนใช้งาน ---
            # isError() จะคืนค่า True หากการสื่อสารล้มเหลว
            if modbus_result.isError():
                print(f"Modbus Error: {modbus_result}")
                # อาจจะลองใหม่ในรอบถัดไป
            else:
                # ถ้าไม่ Error ถึงจะเข้ามาทำงานส่วนนี้
                print("Read successful!")
                print(f"Raw Register Value: {modbus_result.registers[0]}")
                print(f"Calculated Value: {modbus_result.registers[0] / 52}")
                print(f"All Registers: {modbus_result.registers}")
                main_state = 1

        elif main_state == 1:
            print("state 1")
            main_state = 2 # ย้ายไป state 2 เลยเพื่อจบ loop

        elif main_state == 2:
            print("state 2")
            break
            
        time.sleep(2)

    print("exit loop")
    client.close() # อย่าลืมปิดการเชื่อมต่อเมื่อใช้งานเสร็จ
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
# import time

# # comport = '/dev/ttyS0'
# comport = '/dev/ttyUSB0'
# client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
# connection = client.connect()
# time.sleep(3)
# main_state = 0
# while True:
#     if main_state == 0:
#         print("state 0")
#         modbus_result = client.read_holding_registers(address=0,count=1,unit=8)
#         # if modbus_result.function_code < 0x80:
#         print(modbus_result)
#         print(modbus_result.registers[0]/52)
#         print(modbus_result.registers)
#         main_state = 1

#     elif main_state == 1:
#         print("state 1")
#         modbus_result = client.read_holding_registers(address=0,count=1,unit=8)
#         if modbus_result.function_code < 0x80:
#             print(type(modbus_result.registers[0]))
#             main_state = 2

#     elif main_state == 2:
#         print("state 2")
#         break
#     time.sleep(2)

# print("exit loop")