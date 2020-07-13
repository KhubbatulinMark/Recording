import sys
import serial
import datetime

# Определение COM портов
# return    result      подключенные ком-порты
def COMPortDetection():
    """ Определение открытых COM портов """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Инициализация COM порта
# argument  COMPortName     номер порат
# return    serialCOMPort
def InitComPort(COMPortName):
    """ Инициализация COM порта """
    global serialCOMPort
    serialCOMPort = serial.Serial(
        port=COMPortName,
        baudrate=230400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        dsrdtr=False,
        rtscts=True,
        timeout=None
    )
    print(serialCOMPort.name + " is open")
    return serialCOMPort

def vibro_write(vibro_param, filename):

    global flagCOMPortRead

    serial_comport = InitComPort(vibro_param['ComPort'])

    if filename is None:
        filename = 'audio_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.txt'

    f = open(vibro_param['vibro_output_dir'] + filename, 'w')
    while flagCOMPortRead:
        packet: bytes = []
        dataSize = serial_comport.in_waiting
        if dataSize > 0:
            packet = serial_comport.read(dataSize)
        if packet:
            count = 0
            while count < dataSize:
                f.write(str(packet[count]) + str("\n"))
                count += 1
    f.close()

if __name__ == "__main__":
    pass