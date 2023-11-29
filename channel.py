import struct
import numpy as np


class Channel:
    def __init__(self, data):
        self.sub_header = self.__unpack_sub_header(data[0:20])
        
        self.__data = data[20:20+2*self.sub_header['nPoints']] # data is a list of bytes
        #print('length of data:', len(self.__data))
        self.data = self.__unpack_data() # data is a list of integers
        # dava pra ser só self.data = np.array([self.__unpack_point(n)[0] for n in range(int(len(self.__data)/2))])
        self.wavelenghts = np.array([self.sub_header['Minimum wavelength']+self.sub_header['Wavelength increment']*npoint for npoint in range(self.sub_header['nPoints'])])

    def __unpack_sub_header(self, sub_header):
        sub_header_format = '<IIIII'
        (
            sub_header_size,
            minimum_wavelength,
            wavelength_increment,
            nPoints,
            dut_number,
        ) = struct.unpack(sub_header_format, sub_header)
        
        unpacked_sub_header = {
            'Subheader_size':sub_header_size,
            'Minimum wavelength':minimum_wavelength, 
            'Wavelength increment':wavelength_increment, 
            'nPoints': nPoints,
            'DUT number':dut_number,
        }
        return unpacked_sub_header
    
    def __unpack_point(self, n):
        
        values = struct.unpack("<h", self.__data[n*2:(n+1)*2])
        return values
    
    def __unpack_data(self):
        #values = struct.unpack("<"+"h"*self.sub_header['nPoints'], self.__data)

        return np.array([self.__unpack_point(n)[0] for n in range(self.sub_header['nPoints'])])