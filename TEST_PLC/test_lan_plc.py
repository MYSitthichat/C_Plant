from pymodbus.client import ModbusTcpClient

GATEWAY_IP = "192.168.1.170" 
GATEWAY_PORT = 8899
PLC_SLAVE_ID = 1

class lan_plc():
    def connect_lan_open(self, ip, port):
        print(f"Attempting to connect to Gateway at {ip}:{port}...")
        client = ModbusTcpClient(
            host=ip,
            port=port,
            timeout=3 )
        if client.connect():
            print(f"Connected to Gateway {ip}:{port}")
            self.speed_device = client
        else:
            print(f"FAILED to connect to Gateway {ip}:{port}")
            self.speed_device = None

    def test_condition(self):
        PLC_SLAVE_ID = 1
        self.connect_lan_open(GATEWAY_IP, GATEWAY_PORT)
        if not self.speed_device:
            print("Test aborted. No connection to Gateway.")
            return
        try:
            print(f"Sending WRITE COIL 0 (ON) to PLC (Unit ID: {PLC_SLAVE_ID})...")
            self.speed_device.write_coil(
                address=1, 
                value=1, 
                device_id=PLC_SLAVE_ID
            )
            print(f"Sending WRITE COIL 0 (OFF) to PLC (Unit ID: {PLC_SLAVE_ID})...")
            self.speed_device.write_coil(
                address=1, 
                value=0, 
                device_id=PLC_SLAVE_ID
            )
            print("Test complete.")
        except Exception as e:
            print(f"An error occurred during Modbus communication: {e}")
        finally:
            if self.speed_device:
                self.speed_device.close()
                print("Connection closed.")
                
    def read_register(self):
        rr = self.speed_device.read_holding_registers(address=0, count=1, device_id=1)
        if rr.isError():
            print("Error reading register")
        else:
            print("Register values:", rr.registers[0])
    
if __name__ == '__main__':
    main_app = lan_plc()
    print("Test finished")
    GATEWAY_IP = "192.168.1.170" 
    GATEWAY_PORT = 8899
    main_app.connect_lan_open(GATEWAY_IP,GATEWAY_PORT)
    main_app.test_condition()
    main_app.read_register()