########################################################################
# import default python-library
########################################################################
import datetime
import time
import subprocess
import os
import wave
########################################################################

########################################################################
# import addition python-library
########################################################################
import pyaudio
import packaging

#from config import flagCOMPortRead
#######################################################################

def mic_id():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'][-13:-1] == ' AUDIO  CODEC':
            print('Used MIC is ', audio.get_device_info_by_index(i)['name'])
            return i
    else:
        return 1
        #CHANGE THIS
        print("No Microphone")


def audio_write(settings, sec, filename=None):
    
    global flagCOMPortRead
    
    audio = pyaudio.PyAudio()

    if filename is None:
        filename = 'audio_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.wav'

    stream = audio.open(format=pyaudio.paInt16,
                    channels=settings['chans'],
                    rate=settings['samp_rate'],
                    input=True,
                    output=True,
                    frames_per_buffer=settings['chunk'],
                    input_device_index=1)

    frames = []
    if flagCOMPortRead is False:
        for i in range(0, int(settings['samp_rate'] / settings['chunk'] * sec)):
            data = stream.read(settings['chunk'])
            frames.append(data)

    else:
        while flagCOMPortRead:
            data = stream.read(settings['chunk'])
            frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile = wave.open(settings['audio_output_dir'] + filename,'wb')
    wavefile.setnchannels(settings['chans'])
    wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(settings['samp_rate'])
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    print('Audio')
    print(filename, '===>', settings['audio_output_dir'])

if __name__ == "__main__":

    audio = pyaudio.PyAudio()


    # p = pyaudio.PyAudio()
    # for i in range(p.get_device_count()):
    #     print(p.get_device_info_by_index(i)['name'][-13:-1])
    print(mic_id())