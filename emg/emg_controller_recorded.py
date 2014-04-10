from pyqtgraph.Qt import QtGui, QtCore
from plotter import PlotterWindow
import numpy as np
import time, sys, Queue, threading
from filters import IIRFilter

sampling_frequency = 400
buffer_size = 750

record_file_name = "signal-2014-02-17-22-49-58.txt"
recorded_readings = None
playback_counter = 0

readings_queue = Queue.Queue()

def processing_loop():
    while running:
        readings = readings_queue.get()

def reading_loop():
    period = 1.0/sampling_frequency
    last_time = time.clock()
    while running:
        now = time.clock()
        if now - last_time >= period:
            readings = read_emg()
            plotter.update(readings)
            readings_queue.put(readings)
            last_time = now
    
def read_emg():
    global emg_buffer, recorded_readings, playback_counter
    
    emg_readings = recorded_readings[playback_counter, :] 
    playback_counter += 1
    if playback_counter == recorded_readings.shape[0]:
        playback_counter = 0
        print "Gone through all recorded readings, resetting"
    
    return emg_readings

signal_file = open(record_file_name, 'r')

signal_string = signal_file.read()
lines = signal_string.split("\n")

recorded_readings = np.zeros((len(lines), 4))

for i in range(len(lines)):
    numbers = lines[i].split(" ")  
    for j in range(0,4):
        try:
            recorded_readings[i, j] = float(numbers[j])
        except:
            pass
                
running = True

app = QtGui.QApplication(sys.argv)

plotter = PlotterWindow(sampling_frequency, buffer_size)
reading_thread = threading.Thread(target=reading_loop, args=())
reading_thread.start()
processing_thread = threading.Thread(target=processing_loop, args=())
processing_thread.start()
app.exec_()
running = False
print "Terminating.."
