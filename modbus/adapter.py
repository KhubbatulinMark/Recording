import struct
from modbus.message import Message_INNER
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.common import ReadHoldingRegistersResponse
from modbus.model_facade import ModelFacade
import logging
import datetime
import time
import os
import sys

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
cf = logging.FileHandler('modbus-adapter.log')
logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    handlers=[ch, cf])
logger = logging.getLogger(__name__)


class ModBusPacketError(Exception):
    pass


class ModBusAdapter:
    """
    Return parsed data from the ModBus port
    """
    PORT = ''
    BAUD_RATE = 115200
    BYTESIZE = 8
    STOPBITS = 2
    TIMEOUT = 0.2
    SLAVE_UNIT = 1
    REGISTERS_NUM = 28
    TURN_REGISTER = 27

    def __init__(self, com, fmt):
        client = ModbusSerialClient(method="rtu",
                                    port=com,  # self.PORT,
                                    stopbits=self.STOPBITS,
                                    baudrate=self.BAUD_RATE,
                                    bytesize=self.BYTESIZE,
                                    timeout=self.TIMEOUT, )
        client.connect()
        self.client = client
        self.fmt = fmt

    def _answer_parser(self, message: bytes) -> tuple:
        _ = message[0]  # data bytes num
        raw_data = message[1:]

        logger.debug(f"Raw Data {raw_data}")
        return struct.unpack(self.fmt, raw_data)
        # strdata=''
        #
        # return raw_data

    def read_state(self) -> tuple:
        """
        Read registers state
        :return:
        """
        response = self.client.read_holding_registers(0, self.REGISTERS_NUM, unit=self.SLAVE_UNIT)
        if isinstance(response, ReadHoldingRegistersResponse):
            return self._answer_parser(response.encode())
        else:
            raise ModBusPacketError("Broken packet")

    def turn(self, is_on: bool = True):
        """
        Turn on/off remote device
        :param is_on:
        :return:
        """
        self.client.write_register(address=self.TURN_REGISTER, value=int(is_on), unit=self.SLAVE_UNIT)


def modbus_write(modbus_param, filename=None):

    global flagCOMPortRead
    
    if filename is None:
        filename = 'modbus_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.wav'
    
    newreader = ModBusAdapter(modbus_param['ComPort'], Message_INNER.build_fmt())
    cols = Message_INNER.get_cols()
    data = [None] * len(cols)
    all_val_dict = dict(zip(cols, data))
    # TODO Записывать построчно
    while flagCOMPortRead:
        try:
            data = list(newreader.read_state())
        except ModBusPacketError:
            data = list(newreader.read_state())
        dictdata = dict(zip(cols, data))
        for name in all_val_dict:
            if all_val_dict[name] == None:
                if name == 'ts':
                    all_val_dict[name] = [datetime.datetime.timestamp(datetime.datetime.now())]
                else:
                    all_val_dict[name] = [dictdata[name]]
            else:
                if name == 'ts':
                    all_val_dict[name].append(datetime.datetime.timestamp(datetime.datetime.now()))
                else:
                    all_val_dict[name].append(dictdata[name])
    newreader.client.close()
    new = ModelFacade(all_val_dict)
    pandasdata = new.return_data()
    pandasdata.to_csv(modbus_param['modbus_output_dir'] + filename + '.csv')
    print('Inner complete', pandasdata.shape[0])





if __name__ == "__main__":
    pass