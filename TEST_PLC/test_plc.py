from PySide6.QtCore import QThread, Signal, QObject, Slot
from pymodbus.client import ModbusSerialClient

class Speed_motor_Thread(QThread, QObject):
    data_received = Signal(list)
    status_port = Signal(str)
    @Slot(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        print("init speed motor thread")


    def connect_comport_open(self, speed_device):
        self.speed_device = speed_device
        client = ModbusSerialClient(
            port=speed_device,
            baudrate=9600,# parameter PLC H4081 = 9600 ,H4071 = 4800
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1
        )
        if client.connect():
            print("Connected to", speed_device)
            self.speed_device = client


    def disconnect_comport(self):
        if self.speed_device:
            self.speed_device.close()
            # self.status_port.emit("false")
        self.running = False



    def test_condition(self):
        self.connect_comport_open('COM9')
        self.msleep(2000)
        sleep = 200
        for i in range(5):
            self.speed_device.write_coil(address=0, value=1, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=0, value=0, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=1, value=1, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=1, value=0, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=2, value=1, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=2, value=0, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=3, value=1, device_id=1)
            self.msleep(sleep)
            self.speed_device.write_coil(address=3, value=0, device_id=1)
            self.msleep(sleep)
        self.disconnect_comport()
        print("set speed success")

    def read_register(self):
        rr = self.speed_device.read_holding_registers(address=0, count=1, device_id=1)
        if rr.isError():
            print("Error reading register")
        else:
            print("Register values:", rr.registers[0])


if __name__ == '__main__':
    main_app = Speed_motor_Thread()
    main_app.test_condition()
    print("Test finished")