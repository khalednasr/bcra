import numpy as np
import math


def MAV(window):
    N = window.shape[0]
    return (np.sum(abs(window))/N)

def RMS(window):
    N = window.shape[0]
    return math.sqrt((np.sum(window**2)/N))

def WL(window):
    N = window.shape[0]
    WL = 0.0
    for i in range(0,(N-1)):
        WL += abs(window[i+1] - window[i])
    return WL

def ZC(window):
    N = window.shape[0]
    ZC = 0
    for i in range(0,(N-1)):
        if window[i]*window[i+1] < 0.0:
            ZC += 1
    return ZC

def SSC(window):
    N = window.shape[0]
    SSC = 0
    for i in range(1,(N-1)):
        if (window[i]-window[i-1]) * (window[i+1]-window[i]) < 0.0:
            SSC += 1
    return SSC

def IEMG(window):
    return np.sum(abs(window))

def SKW(window):
    N = window.shape[0]
    mean = np.mean(window)
    num = np.sum(((window - mean)**3))/N
    den = (np.sum(((window - mean)**2))/N)**1.5
    return num/den

def VAR(window):
    return np.var(window)


def get_features(window):
    features = []
    features = [SKW(window)/1000.0,WL(window)/50000.0,RMS(window)/1000.0,
				ZC(window)/1000.0,MAV(window)/1000000.0,SSC(window)/1000.0]
    return features
	
def get_features_dataset(dataset,window_size):
	dataset = dataset.T
	dataset = dataset.reshape(-1,4,window_size)
	features_list = []
	for i in range(0,dataset.shape[0]):
		for j in range(0,dataset.shape[1]):
			features_list.append(get_features(dataset[i][j]))

	return np.array(features_list).reshape(dataset.shape[0],-1).T
	