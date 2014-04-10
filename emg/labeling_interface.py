from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#input_file_name = 'Patterns/p5.txt'
input_file_name = 'EMG-S1/M-M1.csv'
output_file_name = 'Patterns/p5_labels.txt'
start_position_label = 'p4'
position_label = 'p5'
number_movements = 20
period = 5000 * 2

labels_offset =  14000
ymin = -2000
ymax = labels_offset + 2000

class LabelingInterface(QtGui.QMainWindow):    
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        
        self.initUI();
        
        self.resize(1000,600)
        self.setWindowTitle("Labeling Interface")
        self.show()

        
    def initUI(self):
        self.pw = pg.PlotWidget(name ="Labeling Interface")
        self.pw.setYRange(ymin,ymax)
        #pg.setConfigOptions(antialias=True)
        
        self.readings = self.read_input_file()

        self.pw.plot(self.readings[:,3], pen=(255,0,0))
        self.pw.plot(self.readings[:,2] + 4000, pen=(0,0,255))
        self.pw.plot(self.readings[:,1] + 8000, pen=(0,255,255))
        self.pw.plot(self.readings[:,0] + 12000, pen=(255,0,255))
        
        self.labels = np.zeros(self.readings.shape[0])
        self.labels_curve = self.pw.plot(self.labels + labels_offset, pen=(0,255,0))
        
        update_button = QtGui.QPushButton("Update Labels")
        update_button.clicked.connect(self.update_labels)
        
        extend_button = QtGui.QPushButton("Extend")
        extend_button.clicked.connect(self.extend)
        
        save_button = QtGui.QPushButton("Save")
        save_button.clicked.connect(self.save)
        
        hbox1 = QtGui.QHBoxLayout()
        #hbox1.addWidget(extend_button, stretch = 1)
        hbox1.addWidget(update_button, stretch = 1)
        hbox1.addWidget(save_button, stretch = 1)
        
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(self.pw, stretch = 10)
        vbox1.addLayout(hbox1, stretch = 10)
        

        central_widget = QtGui.QWidget()
        central_widget.setLayout(vbox1)
        self.setCentralWidget(central_widget)
    
    vlines = []
    def mousePressEvent(self, event):
        if self.pw.getPlotItem().sceneBoundingRect().contains(event.pos()):
            x = int(self.pw.getPlotItem().vb.mapSceneToView(event.pos()).x())
            if event.button() == 4:
                vline = pg.InfiniteLine(angle=90, movable = True)
                vline.setPos(x)
                self.pw.addItem(vline, ignoreBounds=True)
                self.vlines.append(vline)
                print len(self.vlines)
    
    def extend(self):
        if len(self.vlines) == 4:
            for i in range(4):
                for j in range(0,number_movements-1):
                    vline = pg.InfiniteLine(angle=90, movable = True)
                    vline.setPos(self.vlines[i].getPos()[0] + period * (j+1))
                    self.pw.addItem(vline, ignoreBounds=True)
                    self.vlines.append(vline)
        else:
            print "Error"
            
    
    def update_labels(self):
        for i in range(0,len(self.vlines), 4):
            self.labels[self.vlines[i+0].getPos()[0]:self.vlines[i+1].getPos()[0]] = 1000
            self.labels[self.vlines[i+1].getPos()[0]:self.vlines[i+2].getPos()[0]] = 2000
            self.labels[self.vlines[i+2].getPos()[0]:self.vlines[i+3].getPos()[0]] = -500
        
        self.labels_curve.setData(self.labels + labels_offset)
        
    def save(self):
        self.update_labels()
        record_file = open(output_file_name, 'w')
        for i in range(self.readings.shape[0]):
            if self.labels[i] == 1000:
                label = position_label + '_i'
            elif self.labels[i] == 2000:
                label = position_label + '_s'
            elif self.labels[i] == -500:
                label = position_label + '_o'
            else: label = start_position_label + '_s'
            
            record_file.write(label + "\n")            
            
        print 'Done Saving'
    
    def read_input_file(self):
        signal_file = open(input_file_name, 'r')

        signal_string = signal_file.read()
        lines = signal_string.split("\n")

        recorded_readings = np.zeros((len(lines), 4))

        for i in range(len(lines)):
            numbers = lines[i].split(",")  
            for j in range(2):
                try:
                    recorded_readings[i, j] = float(numbers[j]) * 1000000
                except:
                    pass
        return recorded_readings
    
if __name__ == '__main__':
    app = QtGui.QApplication([])
    main_window = LabelingInterface()
    app.exec_()
        
