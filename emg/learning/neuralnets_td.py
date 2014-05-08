import numpy as np
from modshogun import *
import time
import imp
TDF = imp.load_source('TDF', '../TDF.py')

window_size = 64

Xtrain = np.load('../data/ss/Xtrain.npy')
Ytrain = np.load('../data/ss/Ytrain.npy')
Xvalid = np.load('../data/ss/Xvalid.npy')
Yvalid = np.load('../data/ss/Yvalid.npy')

x_one = Xtrain[:,0].reshape(window_size*4,1)
y_one = Ytrain[0]

Xtrain = TDF.get_features_dataset(Xtrain, window_size)
Xvalid = TDF.get_features_dataset(Xvalid, window_size)

Xtrain = RealFeatures(Xtrain)
Ytrain = MulticlassLabels(Ytrain)
Xvalid = RealFeatures(Xvalid)
Yvalid = MulticlassLabels(Yvalid)

layers = DynamicObjectArray()
layers.append_element(NeuralRectifiedLinearLayer(10))
layers.append_element(NeuralSoftmaxLayer(5))

net = NeuralNetwork()
net.initialize(24, layers, 0.01)

#net.l2_coefficient = 5e-5

net.set_labels(Ytrain)

net.io.set_loglevel(MSG_INFO)
net.max_num_epochs = 10000
net.epsilon = 1e-9
net.train(Xtrain)

net.save_serializable(SerializableAsciiFile('net2.txt', 'w'))

#net = NeuralNetwork()
#net.load_serializable(SerializableAsciiFile('net.txt', 'r'))

print MulticlassAccuracy().evaluate(net.apply_multiclass(Xtrain), Ytrain) * 100
print MulticlassAccuracy().evaluate(net.apply_multiclass(Xvalid), Yvalid) * 100

processing_time = 0
for i in range(100):
    t = time.time()
    y = net.apply_multiclass(RealFeatures(TDF.get_features_dataset(x_one, window_size)))
    processing_time += (time.time()-t)*1000/100
print processing_time
