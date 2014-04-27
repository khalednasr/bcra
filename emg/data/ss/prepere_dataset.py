import numpy as np

num_patterns = 5
window_size = 64
window_increment = 32

def process_file(filename):
	raw = np.loadtxt(filename)
	N = raw.shape[0]
	out = None
	for i in range(0, N, window_increment):
		if i+window_size > N: i = N-window_size

		if out == None:
			out = raw[i:i+window_size,:].T.reshape(window_size*4)
		else:
			out = np.vstack((out, raw[i:i+window_size,:].T.reshape(window_size*4)))
	
	return out.T

def process_set(directory):
	X = None
	Y = None
	for i in range(num_patterns):
		filename = directory + '/p' + str(i) + '.txt'
		X_i = process_file(filename)
		Y_i = np.ones(X_i.shape[1])*i
		
		if X == None:
			X = X_i
			Y = Y_i
		else:
			X = np.hstack((X,X_i))
			Y = np.hstack((Y,Y_i))
	
	return (X,Y)

training_data = process_set('raw/training')
validation_data = process_set('raw/validation')

np.save('Xtrain.npy', training_data[0])
np.save('Ytrain.npy', training_data[1])
np.save('Xvalid.npy', validation_data[0])
np.save('Yvalid.npy', validation_data[1])
