import numpy as np
import scipy.signal as signal
import pywt

class WPT(object):
    """ This class performs Wavelet Packet Transform
        - Compulsory inputs: data
        - Optional inputs: basis wavelet, signal extension mode, maximum level of decomposition
        - Output: list of coefficients wraped in natural order
    """
    
    def __init__(self, data, wavelet = 'db4', mode = 'per', maxlevel = None):
        self.wp = pywt.WaveletPacket(data, wavelet, mode, maxlevel)


    def __generate_nodes_list(self,order='natural'):
        l = self.wp.maxlevel
        nodes_list = []
        for i in range(0,l):
            for node in self.wp.get_level(i+1, order):
                nodes_list.append(node.path)
        return nodes_list

    def __wrap_coeffs(self):
        nodes_list = self.__generate_nodes_list()
        coeffs_list = [] 
        for node in nodes_list:
            for coeff in self.wp[node].data:
                coeffs_list.append(coeff)
        return coeffs_list

    def get_coeffs(self):
        return self.__wrap_coeffs()


class Transform_Dataset(object):
    """ This class transforms a given dataset
        - Compulsory inputs: dataset's filename
        - Optional inputs: window size, basis wavelet, signal extension mode, maximum level of decomposition
        - Outputs: * txt file (by calling create_output_txt)
                   * 2D array containing the transformed dataset (by calling create_output_online)
    """
    
    def __init__(self, input_file_name, window_size = 128, wavelet = 'db7', mode = 'per', maxlevel = 4):
        self.window_size = window_size
        self.wavelet = wavelet
        self.mode = mode
        self.maxlevel = maxlevel
        self.input_file = open(input_file_name,'r')
        self.input_lines = self.input_file.readlines()
        self.input_file.close
        

    def __get_line_nums(self,index):
        nums_list = []
        for word in self.input_lines[index].split():
            nums_list.append(float(word))
        nums_array = np.array(nums_list).reshape(-1,self.window_size)
        return nums_array

    def __create_packet(self, data):
        wp = WPT(data, self.wavelet, self.mode, self.maxlevel)
        return wp.get_coeffs()

    def __write_packet(self, packet):
        for i in range(0, len(packet)):
            self.output_file.write(str(packet[i]))
            if i < len(packet)-1:
                self.output_file.write(' ')

    def create_output_txt(self, filename):
        self.output_file = open(filename, 'w')
        n_lines = len(self.input_lines)
        for i in range(0, n_lines):
            nums_array = self.__get_line_nums(i)

            for j in range(0, nums_array.shape[0]):
                packet = self.__create_packet(nums_array[j])
                self.__write_packet(packet)

                if i >= n_lines-1 and j >= nums_array.shape[0]-1:
                    pass
                else:
                    if j >= nums_array.shape[0]-1:
                        self.output_file.write('\n')
                    else:
                        self.output_file.write(' ')

        self.output_file.close()

    def create_output_online(self):
        n_lines = len(self.input_lines)
        final_list = []
        for i in range(0, n_lines):
            nums_array = self.__get_line_nums(i)

            for j in range(0, nums_array.shape[0]):
                packet = self.__create_packet(nums_array[j])
                final_list += packet
    
        final_array = np.array(final_list).reshape(n_lines,-1)
        return final_array
        
        
