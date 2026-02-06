from pymodbus.client import ModbusSerialClient
import time

class test_autoda2015:
    def __init__(self):
        self.client = None
        self.SLAVE_ID = 3 

    def connect_client(self, comport):
        self.client = ModbusSerialClient(
            port=comport,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=3
        )
        if not self.client.connect():
            raise Exception("Client Creation Failed")
        else:
            print(f"Connecting to {comport}...")

    def disconnect_client(self):    
        if self.client:
            self.client.close()

    def unlock_register(self):
        UNLOCK_ADDRESS = 5      
        UNLOCK_CODE = 0x5AA5    
        try:
            self.client.write_register(address=UNLOCK_ADDRESS, value=UNLOCK_CODE, slave=self.SLAVE_ID)
            print("Unlock Register: Success")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error unlocking: {e}")

    def set_zero(self):
        ZERO_ADDRESS = 94 # 40095
        CMD_VALUE = 1
        
        try:
            if not self.client:
                raise Exception("No client connection available")
            rr_write = self.client.write_register(address=ZERO_ADDRESS, value=CMD_VALUE, slave=self.SLAVE_ID)
            
            if rr_write.isError():
                print(f"!! Error setting zero: {rr_write}")
            else:
                print("Set Zero (Clear) Successful!")

        except Exception as e:
            print(f"!! Error occurred during set zero: {e}")

if __name__ == "__main__":
    tester = test_autoda2015()
    
    # เปลี่ยน Comport ตามเครื่องของคุณ (เช่น COM3 หรือ /dev/ttyUSB0)
    comport_name = "COM7" 
    
    try:
        tester.connect_client(comport=comport_name)
        time.sleep(1)

        tester.unlock_register()
        time.sleep(0.5)
        
        # 2. สั่ง Set Zero
        tester.set_zero()
        
    except Exception as e:
        print(f"Main Error: {e}")
    finally:
        tester.disconnect_client()
        print("Test finished")