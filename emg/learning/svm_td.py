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

gk = GaussianKernel()
gk.set_width(80)

svm = GMNPSVM(0.003, gk, Ytrain)
svm.train(Xtrain)

print MulticlassAccuracy().evaluate(svm.apply(Xtrain), Ytrain) * 100
print MulticlassAccuracy().evaluate(svm.apply(Xvalid), Yvalid) * 100