import serial
from serial import tools
from serial.tools import list_ports


class Serial_Reader_Engine:
    def __init__(self, baud):
        ports = list(serial.tools.list_ports.comports())
        self.serialdata = 'No'

        for port in ports:
            #print(port[0])
            if 'COM6' in port[1]:
                self.serialdata = serial.Serial(port[0], baud, bytesize=8,stopbits=2)
    def _read(self):
        return self.serialdata.readline()

serialread=Serial_Reader_Engine(115200)
print(serialread._read())
