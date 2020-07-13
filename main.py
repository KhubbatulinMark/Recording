########################################################################
# import default python-library
########################################################################
import os 
import sys
import pathlib
import datetime
########################################################################

########################################################################
# import addition python-library
########################################################################
import yaml
import serial
# my library
from common import yaml_load
from audio.audio import audio_write
from vibro.vibro import vibro_write
from modbus.adapter import modbus_write
########################################################################

########################################################################
# import interface library
########################################################################
from tkinter import Tk, Button
from threading import Thread
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename
########################################################################

#param loading
param = yaml_load("config.yaml")
audio_param = param['audio']
vibro_param = param['vibro']
modbus_param = param['modbus']
flagCOMPortRead = False
serialCOMPort = serial.Serial()

#main funcrions 

def stop():
    global flagCOMPortRead
    flagCOMPortRead = False
    print('Stop')
    serialCOMPort.close()
    writeThread.join()
    audioTread.join()
    innerwtiteTread.join()
    labelCOM1 = Label(text='COM is not open', bg='red')
    labelCOM1.place(x=0, y=72, width=704, height=40)

def exit():
    global flagCOMPortRead
    flagCOMPortRead = False
    serialCOMPort.close()
    sys.exit()

def start_audio(audio_param):
    
    global flagCOMPortRead
    flagCOMPortRead = False
    audio_write(audio_param, sec=10)

def start_vibro(vibro_param):
    
    global flagCOMPortRead
    flagCOMPortRead = True
    vibro_write(vibro_param)

def start_modbus(modbus_param):
    
    global flagCOMPortRead
    flagCOMPortRead = True
    modbus_write(modbus_param, flagCOMPortRead)


def rec_inner_data():
    
    global flagCOMPortRead

    newreader = ModBusAdapter(INNER_COM, fmt.build_fmt())
    cols = fmt.get_cols()
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
    pandasdata.to_csv(INNER_DIR + filename + '.csv')
    print('Inner complete', pandasdata.shape[0])
    
########################################################################
#---------------------------INTERFACE----------------------------------#
########################################################################
# arrayCOM = vibro.vibro.COMPortDetection()

root = Tk()
root.geometry('600x120')
root.title('Recording Audio, Vibro, Modbus')

# Start writing from all devices
button_all = Button(root, text="Start All", command=lambda: clicked())
button_all.place(x=0, y=0, width=200, height=60)

# Stop writing with all methods
button_stop = Button(root, text="Stop record", command=lambda: stop())
button_stop.place(x=200, y=0, width=200, height=60)

# COM port stop button
button_exit = Button(root, text="Exit", command=lambda: exit())
button_exit.place(x=400, y=0, width=200, height=60)

# Start writing audio
button_audio = Button(root, text="Start Audio", command=lambda: start_audio(audio_param))
button_audio.place(x=0, y=60, width=200, height=60)

# Start writing vibro
button_vibro = Button(root, text="Start Vibro", command=lambda: start_vibro(vibro_param))
button_vibro.place(x=200, y=60, width=200, height=60)

# Start writing modbus
button_modbus = Button(root, text="Start Modbus", command=lambda: start_modbus())
button_modbus.place(x=400, y=60, width=200, height=60)



if __name__ == "__main__":

    root.mainloop()
