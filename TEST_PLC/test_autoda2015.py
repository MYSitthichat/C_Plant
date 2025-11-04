from pymodbus.client import ModbusSerialClient
import time


class test_autoda2015:
    def int32_to_registers(self, value):
        """
        แปลงค่า 32-bit (signed int) ให้เป็น list 16-bit 2 ค่า [High Word, Low Word]
        """
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