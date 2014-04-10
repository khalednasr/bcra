import numpy as np
import scipy.signal as signal

class FIRFilter():
    def __init__(self, numtaps, bands, gains, fs, num_channels = 4):
        self.numtaps = numtaps
        self.fs = fs
        self.num_channels = num_channels
        
        self.b = signal.remez(numtaps, bands, gains, Hz = fs)[::-1]
        
        self.x = np.zeros((num_channels,numtaps))
        
    def update(self, new_values):
        self.x = np.roll(self.x, -1, 1)
        self.x[:, self.numtaps-1] = new_values
        
        y = np.zeros(self.num_channels)       
        for i in range(self.num_channels):
            y[i] = np.dot(self.x[i, :], self.b)
            
        return y
    
class IIRFilter():
    def __init__(self, order, bands, btype, fs, num_channels = 4):
        self.num_channels = num_channels
        
        def f2w(f): return f / (0.5*fs)
        
        if len(bands) == 2:
            self.b, self.a = signal.butter(order, [f2w(bands[0]), f2w(bands[1])], btype=btype)
        else:
            self.b, self.a = signal.butter(order, f2w(bands), btype=btype)
        
        self.a = self.a[::-1]
        self.b = self.b[::-1]
        
        self.x = np.zeros((num_channels,len(self.b)))
        self.y = np.zeros((num_channels,len(self.a)))
        
    def update(self, new_values):
        self.x = np.roll(self.x, -1, 1)
        self.x[:, len(self.b)-1] = new_values[:]
        
        self.y = np.roll(self.y, -1, 1)
        
        yn = np.zeros(self.num_channels)
        l = len(self.a)
        for i in range(self.num_channels):
            yn[i] = np.dot(self.x[i, :], self.b) - np.dot(self.a[0:l - 1], self.y[i,0:l -1])
            yn[i] = yn[i] / self.a[len(self.a) - 1]
        
        self.y[:, len(self.a)-1] = yn
        
        return yn

class AvgFilter():
    def __init__(self, numtaps, num_channels = 4):
        self.numtaps = numtaps
        self.num_channels = num_channels
        
        self.x = np.zeros((num_channels,numtaps))
        
    def update(self, new_values):
        self.x = np.roll(self.x, -1, 1)
        self.x[:, self.numtaps-1] = new_values
        
        y = np.sum(self.x, 1) / self.numtaps
            
        return y
        
        
        
        
        
        
        
        
        
        
        