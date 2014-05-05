import numpy as np
from modshogun import *

Xtrain = np.load('../data/ss/Xtrain.npy')
Ytrain = np.load('../data/ss/Ytrain.npy')
Xvalid = np.load('../data/ss/Xvalid.npy')
Yvalid = np.load('../data/ss/Yvalid.npy')

Xtrain = RealFeatures(Xtrain)
Ytrain = MulticlassLabels(Ytrain)
Xvalid = RealFeatures(Xvalid)
Yvalid = MulticlassLabels(Yvalid)

layers = DynamicObjectArray()
layers.append_element(NeuralRectifiedLinearLayer(150))
layers.append_element(NeuralSoftmaxLayer(5))

net = NeuralNetwork()
net.initialize(64, layers)

#net.l2_coefficient = 0.01

net.optimization_method = NNOM_GRADIENT_DESCENT
net.gd_learning_rate = 0.003
#net.gd_mini_batch_size = 100
net.epsilon = 0.0

net.dropout_hidden = 0.5
net.dropout_input = 0.2
net.max_norm = 15

net.set_labels(Ytrain)

#net.io.set_loglevel(MSG_INFO)
net.max_num_epochs = 10
for i in range(0,1000):
    net.train(Xtrain)
    training_acc = MulticlassAccuracy().evaluate(net.apply_multiclass(Xtrain), Ytrain) * 100
    validation_acc = MulticlassAccuracy().evaluate(net.apply_multiclass(Xvalid), Yvalid) * 100
    print training_acc, validation_acc, i


net.save_serializable(SerializableAsciiFile('net2.txt', 'w'))

#net = NeuralNetwork()
#net.load_serializable(SerializableAsciiFile('net.txt', 'r'))

print MulticlassAccuracy().evaluate(net.apply_multiclass(Xtrain), Ytrain) * 100
print MulticlassAccuracy().evaluate(net.apply_multiclass(Xvalid), Yvalid) * 100

#import matplotlib.pyplot as plt
#X1 = np.mean(Xtrain, 0)
#X2 = np.var(Xtrain, 0)
#
#colors = ['r', 'g', 'b', 'c', 'y']
#for i in range(5):
#    plt.scatter(X1[Ytrain==i], X2[Ytrain==i], color=colors[i])
#    
#plt.show()
