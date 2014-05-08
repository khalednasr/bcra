from pyqtgraph.Qt import QtGui, QtCore
from plotter import PlotterWindow
import numpy as np
import time, sys, Queue, threading
import bluetooth as bt
from filters import IIRFilter

sampling_frequency = 400
buffer_size = 400

readings_queue = Queue.Queue()
window_size = 16
sliding_size = window_size/2
processing_buffer = np.zeros(4,window_size)

order = 2
notch_filter = IIRFilter(order, [48, 52], 'stop', sampling_frequency)
band_filter = IIRFilter(order, [15, 200], 'pass', sampling_frequency)

def processing_loop():
    while running:
        readings = readings_queue.get()
		processing_buffer = np.roll(processing_buffer,-1,1)
		processing_buffer[:, window_size-1] =  readings_queue.get()
        
        print readings_queue.qsize()

def reading_loop():
    while running:
        raw = read_emg()# -2000
        filtered = notch_filter.update(raw)
        filtered = band_filter.update(filtered)
        plotter.update(filtered)
        #readings_queue.put(readings)

def read_emg():
    while True:
        b1 = ord(port.recv(1))
        if b1 == 255:
            b2 = ord(port.recv(1))
            if b2 == 255: break

    emg_readings = np.zeros(4)
    emg_readings[0] = read_int16()
    emg_readings[1] = read_int16()
    emg_readings[2] = read_int16()
    emg_readings[3] = read_int16()
    read_int16() #timestamp
    
    return emg_readings

def read_int16():
    try:
        b1 = ord(port.recv(1))
        b2 = ord(port.recv(1))
        return b2 + 256*b1 - 32766
    except:
        pass
    
port = bt.BluetoothSocket(bt.RFCOMM)
port.connect(('20:13:10:29:03:20', 1))
running = True

print "Connected"

app = QtGui.QApplication(sys.argv)
plotter = PlotterWindow(sampling_frequency, buffer_size)
reading_thread = threading.Thread(target=reading_loop, args=())
reading_thread.start()
processing_thread = threading.Thread(target=processing_loop, args=())
#processing_thread.start()
app.exec_()
running = False
port.close()
print "Terminating.."
