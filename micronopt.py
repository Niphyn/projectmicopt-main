from __future__ import print_function, division
import datetime
import socket
import struct
import time
import json
import sys
import numpy as np
from data import Data
import re

class Interrogator(object):
    def __init__(self, ip_address="10.0.0.122", port=50000, fbg_props=None):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.latest_response = ""
        self.sensors = []
        if fbg_props:
            self.create_sensors(fbg_props)
        self.sample_rate = 1000
        self.append_data = False
        self.stream_data = False
        self.data = {}
        self.acq_counter = 0

    
    def connect(self):
        print('Conectando...')
        self.socket.connect((self.ip_address, self.port))
        print('Conectou')

    def send_command(self, command, receive=True):
        if command[0] != "#":
            command = "#" + command
        if command[-1] != "\n":
            command += "\n"
        self.socket.send(command.encode("ascii"))
        if receive:
            #respsize = int(self.socket.recv(10)) # <<
            respsize = int(self.socket.recv(10)) # <<
            
            full_response = self.socket.recv(respsize, socket.MSG_WAITALL)
            
            self.latest_response = full_response
            
    def decode_peaks(self,response, verbose=False):
        # Decodificando a parte inicial da leitura
        (
            seconds,               # 32 unsigned int
            microseconds,          # 32 unsigned int
            serial_number,         # 32 unsigned int
            peaks_channel1,     # 16 signed int (signed short)
            peaks_channel2,     # 16 signed int (signed short)
            peaks_channel3,     # 16 signed int (signed short)
            peaks_channel4,     # 16 signed int (signed short)
            ) = struct.unpack('<'+'I'*3 +'h'*4, response[:3*4+2*4])

        # Pegando os trechos de cada canal
        # OBS: o tamanho dos bytes tava errado no pdf - corrigido
        bytes_ch1_wavelength_data = response[32:32+4*peaks_channel1]
        bytes_ch2_wavelength_data = response[32+4*peaks_channel1:32+4*peaks_channel1+4*peaks_channel2]
        bytes_ch3_wavelength_data = response[32+4*(peaks_channel1+peaks_channel2):32+4*(peaks_channel1+peaks_channel2)+4*peaks_channel3]
        bytes_ch4_wavelength_data = response[32+4*(peaks_channel1+peaks_channel2+peaks_channel3):32+4*(peaks_channel1+peaks_channel2+peaks_channel3)+4*peaks_channel4]
        
        
        # Idem 
        bytes_ch1_levels = response[32+4*(peaks_channel1+peaks_channel2+peaks_channel3+peaks_channel4):32+4*(peaks_channel1+peaks_channel2+peaks_channel3)+2*peaks_channel1]
        bytes_ch2_levels = response[32+4*(peaks_channel1+peaks_channel2+peaks_channel3+peaks_channel4)+2*peaks_channel1:32+4*(peaks_channel1+peaks_channel2+peaks_channel3)+2*peaks_channel1+2*peaks_channel2]
        bytes_ch3_levels = response[32+4*(peaks_channel1+peaks_channel2+peaks_channel3+peaks_channel4)+2*(peaks_channel1+peaks_channel2):32+4*(peaks_channel1+peaks_channel2+peaks_channel3)+2*(peaks_channel1+peaks_channel2)+2*peaks_channel3]
        bytes_ch4_levels = response[32+4*(peaks_channel1+peaks_channel2+peaks_channel3+peaks_channel4)+2*(peaks_channel1+peaks_channel2+peaks_channel3):32+4*(peaks_channel1+peaks_channel2+peaks_channel3)+2*(peaks_channel1+peaks_channel2+peaks_channel3)+2*peaks_channel4]
        
        
        ch1_wavelengths = struct.unpack('<'+'i'*peaks_channel1, bytes_ch1_wavelength_data)
        ch2_wavelengths = struct.unpack('<'+'i'*peaks_channel2, bytes_ch2_wavelength_data)
        ch3_wavelengths = struct.unpack('<'+'i'*peaks_channel3, bytes_ch3_wavelength_data)
        ch4_wavelengths = struct.unpack('<'+'i'*peaks_channel4, bytes_ch4_wavelength_data)
        
        ch1_levels = struct.unpack('<'+'h'*peaks_channel1, bytes_ch1_levels)
        ch2_levels = struct.unpack('<'+'h'*peaks_channel2, bytes_ch2_levels)
        ch3_levels = struct.unpack('<'+'h'*peaks_channel3, bytes_ch3_levels)
        ch4_levels = struct.unpack('<'+'h'*peaks_channel4, bytes_ch4_levels)

        if peaks_channel1 == 0:
            ch1_wavelengths = (0,0)
            ch1_levels = (0,0)
        
        if peaks_channel2 == 0:
            ch2_wavelengths = (0,0)
            ch2_levels = (0,0)

        if peaks_channel3 == 0:
            ch3_wavelengths = (0,0)
            ch3_levels = (0,0)

        if peaks_channel4 == 0:
            ch4_wavelengths = (0,0)
            ch4_levels = (0,0)

        
        if verbose:
            print('Peaks in Channel 1:', peaks_channel1)
            print(ch1_wavelengths, ch1_levels)
            print('Peaks in Channel 2:', peaks_channel2)
            print(ch2_wavelengths, ch2_levels)
            print('Peaks in Channel 3:', peaks_channel3)
            print(ch3_wavelengths, ch4_levels)
            print('Peaks in Channel 4:', peaks_channel4)
            print(ch4_wavelengths, ch4_levels)
        
        return (ch1_wavelengths, ch2_wavelengths, ch3_wavelengths, ch4_wavelengths), (ch1_levels, ch2_levels, ch3_levels, ch4_levels), (peaks_channel1, peaks_channel2, peaks_channel3, peaks_channel4)

    @property
    def idn(self):
        self.send_command("IDN?")
        return self.latest_response.decode()

    @property
    def get_peaks(self):
        self.send_command("GET_PEAKS_AND_LEVELS")
        return self.latest_response

    @property
    def get_spectrum(self):
        self.send_command("GET_DATA")
        #print('Response length:', len(self.latest_response))
        response = self.latest_response
        data = Data(response)
        return data
        
    def flush_buffer(self, receive=True, verbose=False):
        """
        This command flushes out the contents of the data buffer for the 
        present socket connection, clearing all data and resetting the buffer 
        count to zero.
        """
        print('Flushing buffer...')
        self.send_command("FLUSH_BUFFER", receive=receive)
        if verbose and receive:
            print(self.latest_response)
            print('Flushed buffer')
    
 
    #Todos os Gets estão com prints para eu ver a estrutura da resposta
    #define um limite mínimo de um canaç em específico para evitar a detecção de ruídos como picos   
    
    def set_peak_threshold(self, ch, val):
        self.send_command("SET_PEAK_THRESHOLD_CH"+str(ch)+" "+str(val))
        return self.latest_response
    
    #obtêm o limite mínimo para um espectro ser considerado pico de um canal em específico
    def get_peak_threshold(self, ch):
        self.send_command("GET_PEAK_THRESHOLD_CH"+str(ch))
        resultado = self.decode_gets()
        print("Peak Threshold eh " + resultado)
        return "Peak Threshold eh " + resultado
    
    #obtêm o estado de um canal em específico como (ativo = 1 e inativo = 0)
    def get_ch_state(self, ch):
        self.send_command("GET_DUT"+str(ch)+"_STATE")
        resultado = self.decode_gets()
        print("Estado do Canal eh " + resultado)
        return "Estado do Canal eh "+ resultado
    
    #define o estado de um canal em específico como (ativo = 1 e inativo = 0)
    def set_ch_state(self, ch, val):
        self.send_command("SET_DUT"+str(ch)+"_STATE "+str(val))
        return self.latest_response
    
    #define o limite máximo para um espectro ser considerado pico e não ruído com base no ponto mais alto detectado de um canal em específico
    def set_rel_peak_threshold(self, ch, val):
        self.send_command("SET_REL_PEAK_THRESHOLD_CH"+str(ch)+" "+str(val))
        return self.latest_response
    
    #obtem o limite máximo para um expectro ser considerado pico
    def get_rel_peak_threshold(self, ch):
        self.send_command("GET_REL_PEAK_THRESHOLD_CH"+str(ch))
        resultado = self.decode_gets()
        print("Relative Peak Threshold eh " + resultado)
        return "Relative Peak Threshold eh "+ resultado
    
    #define a largura mínima para um canal para que caractehristicas espectrais só sejam consideradas picos se tiverem no mínimo essa largura a um level abaixo 
    def set_peak_width(self, ch, val):
        self.send_command("SET_PEAK_WIDTH_CH"+str(ch)+" "+str(val))
        return self.latest_response
    
    #obtêm a largura mínima de um canal em um level abaixo
    def get_peak_width(self, ch):
        self.send_command("GET_PEAK_WIDTH_CH"+str(ch))
        resultado = self.decode_gets()
        print("Peak Width eh " + resultado)
        return "Peak Width eh "+ resultado
    
    #define o level no qual a largura será medida
    def set_peak_width_level(self, ch, val):
        self.send_command("SET_PEAK_WIDTH_LEVEL_CH"+str(ch)+" "+str(val))
        return self.latest_response
    
    #obtêm o level no qual a largura será medida 
    def get_peak_width_level(self, ch):
        self.send_command("GET_PEAK_WIDTH_LEVEL_CH"+str(ch))
        resultado = self.decode_gets()
        print("Peak Width Level eh " + resultado)
        return "Peak Width Level eh "+ resultado
        
    def decode_gets(self):
        str_aux = str(self.latest_response)
        resultado = str_aux.split(' ',1)
        resultado = resultado[1].split("\\",1)
        return resultado[0]

    def disconnect(self):
        print('Desconectando...')
        self.socket.close()
        print('Desconectou')
    
        
    

    
