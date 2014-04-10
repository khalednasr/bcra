from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
from time import clock
import time
import datetime

class PlotterWindow(QtGui.QMainWindow):    
    record_file = None
    record_start_time = 0
    is_recording = False
    record_one = False
    
    record_timer_period = 3000 #ms
    
    def __init__(self, sampling_frequency,buffer_size):
        QtGui.QMainWindow.__init__(self, None)
        
        self.readings_buffer = np.zeros((4, buffer_size))
        self.sampling_frequency = sampling_frequency
        self.buffer_size = buffer_size
        
        self.freq_axis = np.fft.fftfreq(buffer_size, d = 1.0/sampling_frequency)
        self.freq_axis = self.freq_axis[0:len(self.freq_axis)/2]
        
        self.initUI();
        
        self.resize(1000,600)
        self.setWindowTitle("Serial Plotter")
        self.show()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updatePlots)
        self.timer.start(1/0.03)

        
    def initUI(self):
        ymin = -1000
        ymax = 1000
        
        self.pw1 = pg.PlotWidget(name='pw1')
        self.pw1.setXRange(0, self.buffer_size)
        self.pw1.setYRange(ymin,ymax)
        self.pw1.setTitle('Channel 1')
        #self.pw1.showAxis('bottom', False)
        self.pw1.showGrid(True, True)
        self.pc1 = self.pw1.plot(pen='y')
        
        self.pwf1 = pg.PlotWidget(name='pwf1')
        self.pwf1.setXRange(0, self.freq_axis[len(self.freq_axis)-1])
        self.pwf1.setYRange(0,160)
        self.pwf1.setTitle('Channel 1 FFT')
        self.pw1.showGrid(True, True)
        self.pcf1 = self.pwf1.plot(pen='y')

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.pw1)
        hbox1.addWidget(self.pwf1)

        self.pw2 = pg.PlotWidget(name='pw2')
        self.pw2.setXRange(0, self.buffer_size)
        self.pw2.setYRange(ymin,ymax)
        self.pw2.setTitle('Channel 2')
        #self.pw2.showAxis('bottom', False)
        self.pw2.showGrid(True, True)
        self.pc2 = self.pw2.plot(pen='y')
        
        self.pwf2 = pg.PlotWidget(name='pwf2')
        self.pwf2.setXRange(0, self.freq_axis[len(self.freq_axis)-1])
        self.pwf2.setYRange(0,160)
        self.pwf2.setTitle('Channel 2 FFT')
        self.pw2.showGrid(True, True)
        self.pcf2 = self.pwf2.plot(pen='y')

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.pw2)
        hbox2.addWidget(self.pwf2)

        self.pw3 = pg.PlotWidget(name='pw3')
        self.pw3.setXRange(0, self.buffer_size)
        self.pw3.setYRange(ymin,ymax)
        self.pw3.setTitle('Channel 3')
        #self.pw3.showAxis('bottom', False)
        self.pw3.showGrid(True, True)
        self.pc3 = self.pw3.plot(pen='y')
        
        self.pwf3 = pg.PlotWidget(name='pwf3')
        self.pwf3.setXRange(0, self.freq_axis[len(self.freq_axis)-1])
        self.pwf3.setYRange(0,160)
        self.pwf3.setTitle('Channel 3 FFT')
        self.pw3.showGrid(True, True)
        self.pcf3 = self.pwf3.plot(pen='y')

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.pw3)
        hbox3.addWidget(self.pwf3)
        
        self.pw4 = pg.PlotWidget(name='pw4')
        self.pw4.setXRange(0, self.buffer_size)
        self.pw4.setYRange(ymin,ymax)
        self.pw4.setTitle('Channel 4')
        #self.pw4.showAxis('bottom', False)
        self.pw4.showGrid(True, True)
        self.pc4 = self.pw4.plot(pen='y')
        
        self.pwf4 = pg.PlotWidget(name='pwf4')
        self.pwf4.setXRange(0, self.freq_axis[len(self.freq_axis)-1])
        self.pwf4.setYRange(0,160)
        self.pwf4.setTitle('Channel 4 FFT')
        self.pw4.showGrid(True, True)
        self.pcf4 = self.pwf4.plot(pen='y')

        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(self.pw4)
        hbox4.addWidget(self.pwf4)

        self.record_button = QtGui.QPushButton("Start Recording")
        self.record_button.clicked.connect(self.record)
        
        self.record_name_textedit = QtGui.QLineEdit(self)
        self.record_name_textedit.setText("signal")
        
        self.pause_button = QtGui.QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)
        
        hbox5 = QtGui.QHBoxLayout()       
        hbox5.addWidget(self.record_button, stretch = 1)
        hbox5.addWidget(QtGui.QLabel("Record File Name:", self))
        hbox5.addWidget(self.record_name_textedit, stretch = 1)
        hbox5.addWidget(self.pause_button, stretch = 1)
        
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addLayout(hbox5, stretch = 1)
        vbox1.addLayout(hbox1, stretch = 10)
        vbox1.addLayout(hbox2, stretch = 10)
        vbox1.addLayout(hbox3, stretch = 10)
        vbox1.addLayout(hbox4, stretch = 10)
        
        central_widget = QtGui.QWidget()
        central_widget.setLayout(vbox1)
        self.setCentralWidget(central_widget)
    
    def update(self, values_to_plot, values_to_record = None):
        self.readings_buffer = np.roll(self.readings_buffer, -1, 1)
        self.readings_buffer[:, self.buffer_size-1] = values_to_plot
        
        if self.is_recording:
            if (values_to_record != None): self.record_line(values_to_record)
            else: self.record_line(values_to_plot)
            
    def record(self, dummy):
        file_name = self.record_name_textedit.text() + "-" + str(datetime.datetime.now()).replace(" ", "-").replace(":", "-").split(".")[0] + ".txt"
        if not self.is_recording:
            self.record_file = open(file_name, 'w')
            self.record_button.setText("Stop Recording")
            self.is_recording = True
            
            self.record_timer = QtCore.QTimer()
            self.record_timer.timeout.connect(self.record_timer_tick)
            self.record_timer.start(self.record_timer_period)
            
        else:
            self.is_recording = False
            self.record_file.close()
            self.record_button.setText("Start Recording")
            
            self.record_timer.stop()
    
    counter = 0
    
    def record_timer_tick(self):
        QtGui.QApplication.beep()
        if (self.record_one):
            self.counter += 1
            print self.counter
        self.record_one = not self.record_one
    
    def record_line(self, values_to_record):          
        self.record_file.write(str(values_to_record[0]) + " ")
        self.record_file.write(str(values_to_record[1]) + " ")
        self.record_file.write(str(values_to_record[2]) + " ")
        self.record_file.write(str(values_to_record[3]) + "\n")

    def updatePlots(self):
        channel1_data = self.readings_buffer[0,:]
        self.pc1.setData(channel1_data)

        channel2_data = self.readings_buffer[1,:]
        self.pc2.setData(channel2_data)
        
        channel3_data = self.readings_buffer[2,:]
        self.pc3.setData(channel3_data)
        
        channel4_data = self.readings_buffer[3,:]
        self.pc4.setData(channel4_data)
        
        channel1_fft = abs(np.fft.fft(channel1_data)[0:len(self.freq_axis)])/self.buffer_size
        self.pcf1.setData(self.freq_axis, channel1_fft)

        channel2_fft = abs(np.fft.fft(channel2_data)[0:len(self.freq_axis)])/self.buffer_size
        self.pcf2.setData(self.freq_axis, channel2_fft)

        channel3_fft = abs(np.fft.fft(channel3_data)[0:len(self.freq_axis)])/self.buffer_size
        self.pcf3.setData(self.freq_axis, channel3_fft)

        channel4_fft = abs(np.fft.fft(channel4_data)[0:len(self.freq_axis)])/self.buffer_size
        self.pcf4.setData(self.freq_axis, channel4_fft)
    
    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Resume")
        else:
            self.timer.start()
            self.pause_button.setText("Pause")
        

if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    main_window = PlotterWindow()
    app.exec_()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
