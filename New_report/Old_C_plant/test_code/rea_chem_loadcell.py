from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

comport = '/dev/ttyUSB0'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
time.sleep(1)
main_state = 0
loop_counter = 0
while loop_counter <= 10:
    print("loop ",loop_counter, " : ")
    modbus_result = client.read_holding_registers(address=12,count=1,unit=2)
    if modbus_result.function_code < 0x80:
        chem_offset_float = int(modbus_result.registers[0])
    else:
        chem_offset_float = 140
    print(modbus_result," : ", chem_offset_float)
    time.sleep(1)
    loop_counter = loop_counter + 1

print("exit loop")