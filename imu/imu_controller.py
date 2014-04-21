import pyglet
import numpy as np
import serial
import threading
import time, math
from math import sin, cos, atan2
from simulation import SimulationWindow


port_name = "/dev/ttyACM0"
baud_rate = 115200
running = False

start_time = time.time()
drift_time = 15
drift_over = False

#zero_rmatrix = np.array([
#   [0.0, 0.0, 1.0],
#   [0.0, 1.0, 0.0],
#   [-1.0, 0.0, 0.0]])

zero_rmatrix = np.eye(3)

drift_correction_rmatrix1 = np.eye(3)
drift_correction_rmatrix2 = np.eye(3)

def processing_loop():
	while running:
		rmatrix1, rmatrix2, mag = read_imu()
		
		#yaw_mag = math.atan2(mag[1], mag[0]) * (180.0/math.pi)
		
		#yaw_mag = atan2(mag[2]*sin(phi) - mag[1]*cos(phi), mag[0]*cos(theta)+mag[1]*sin(theta)*sin(phi) + mag[2]*sin(theta)*cos(phi)) * (180.0/math.pi)
		#yaw_mag = atan2(mag[1]*cos(theta) + mag[2]*sin(theta), mag[0]*cos(phi)+mag[1]*sin(theta)*sin(phi) + mag[2]*cos(theta)*sin(phi)) * (180.0/math.pi)
		
		mag = np.dot(rmatrix1, mag)
		yaw_error = math.atan2(mag[1], mag[0])
		
		rz1 = np.array([
		 [ cos(yaw_error),  sin(yaw_error), 0.0],
		 [-sin(yaw_error),  cos(yaw_error), 0.0],
		 [      0.0      ,       0.0      , 1.0]])
		
		rmatrix1 = np.dot(rz1, rmatrix1)
		
		rmatrix1, rmatrix2 = correct_drift(rmatrix1, rmatrix2)
		
		print yaw_error * 180 / math.pi
		
		x1 = rmatrix1[:,0]
		y1 = rmatrix1[:,1]
		z1 = rmatrix1[:,2] 
		
		p1 = x1 * 100
		p2 = y1 * 75
		p3 = z1 * 50
		p4 = None
		
		simulator.update_points(p1, p2, p3, p4, drift_over)

def correct_drift(rmatrix1, rmatrix2):
	global drift_over, drift_correction_rmatrix1, drift_correction_rmatrix2
	if not drift_over:
		elapsed_time = time.time() - start_time
		if elapsed_time > drift_time:
			drift_over = True
			drift_correction_rmatrix1 = np.dot(zero_rmatrix, np.linalg.inv(rmatrix1))
			drift_correction_rmatrix2 = np.dot(zero_rmatrix, np.linalg.inv(rmatrix2))
		
	rmatrix1 = np.dot(drift_correction_rmatrix1, rmatrix1)
	rmatrix2 = np.dot(drift_correction_rmatrix2, rmatrix2)
		
	return rmatrix1, rmatrix2
        
   
def read_imu():
	while True:
		b1 = ord(port.read())
		if b1 == 255:
			b2 = ord(port.read())
			if b2 == 255: break
	
	quat1 = np.zeros(4)
	quat2 = np.zeros(4)
	mag = np.zeros(3)
	for i in range(4):
		quat1[i] = float(read_int16())/32767
	
	for i in range(3):
		mag[i] = float(read_int16())/16
	
	temp = mag[0]
	mag[0] = mag[1]
	mag[1] = -1*temp

	return (quaternion_to_rmatrix(quat1), np.eye(3), mag)

def read_int16():
	high_byte = ord(port.read())
	low_byte = ord(port.read())
	return low_byte + 256*high_byte - 32766

def quaternion_to_rmatrix(quaternion):
	q = np.array(quaternion, dtype=np.float64, copy=True)
	n = np.dot(q, q)
	_EPS = np.finfo(float).eps * 4.0
	if n < _EPS:
		return np.identity(4)
	q *= math.sqrt(2.0 / n)
	q = np.outer(q, q)
	rmatrix = np.array([
		[1.0-q[2, 2]-q[3, 3],     q[1, 2]-q[3, 0],     q[1, 3]+q[2, 0]],
		[    q[1, 2]+q[3, 0], 1.0-q[1, 1]-q[3, 3],     q[2, 3]-q[1, 0]],
		[    q[1, 3]-q[2, 0],     q[2, 3]+q[1, 0], 1.0-q[1, 1]-q[2, 2]]])
	
	#rmatrix = np.zeros((3,3))
	#rmatrix[0,:] = -1*rmatrix_[0,:]
	#rmatrix[1,:] =  1*rmatrix_[1,:]
	#rmatrix[2,:] = -1*rmatrix_[2,:]
		
	return rmatrix

def rmatrix_to_euler(rmatrix):
	if rmatrix[2,0] != 1 and rmatrix[2,0] != -1:
		theta1 = -math.asin(rmatrix[2,0]) * 180.0/math.pi
		psi1 =math.atan2(rmatrix[2,2], rmatrix[2,1]) * 180.0/math.pi
		return (theta1, psi1)


if __name__ == '__main__':
	port = serial.Serial(port_name, baudrate = baud_rate)
	print 'Connected'
	running = True
	simulator = SimulationWindow()
	
	processing_thread = threading.Thread(target=processing_loop, args=())
	processing_thread.start()
	
	pyglet.app.run()
	running = False
	port.close()
	
