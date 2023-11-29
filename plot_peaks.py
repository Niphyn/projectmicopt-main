
from data import Data
from micronopt import *
import numpy as np
import time
import keyboard
import matplotlib.pyplot as plt

exitProgram = False

def quit():
    global exitProgram
    exitProgram=True

keyboard.add_hotkey('q', lambda: quit())

interrogator = Interrogator()
interrogator.connect()


number_of_samples = 50
acquisitions_per_average = 4
average_time = 10

time_step = average_time / acquisitions_per_average

plt.ion() 
nacq = [0]

ch1_acqs = []
ch2_acqs = []
ch3_acqs = []
ch4_acqs = []

maxval = 0
minval = 1e10

while not exitProgram:
    i = 0
    wavelengths_list = [()] * acquisitions_per_average
    power_at_peak_list = [()] * acquisitions_per_average
    number_of_peaks_list = [()] * acquisitions_per_average
    while i<acquisitions_per_average:
        init_time = time.time()
        response = interrogator.get_peaks
        wavelengths_list[i], power_at_peak_list[i], number_of_peaks_list[i] = interrogator.decode_peaks(response, False)
        final_time = time.time()
        time_difference = final_time - init_time
        if time_difference > time_step:
            print('Erro - demorou demais para coletar os dados')
            interrogator.disconnect()
            exit()
        time.sleep(time_difference)
        i+=1
    channels_wavelengths = [0, 0, 0, 0]
    valid_measures = [0, 0, 0, 0]
    for i, acq in enumerate(wavelengths_list):
        for j, var in enumerate(acq):
            if len(var)==1: # ta considerando a adição que a jullie fez, tem que checar por causa do caso de ter mais de um pico
                valid_measures[j] += 1
                channels_wavelengths[j] += var[0]

    wavelengths_average = [0, 0, 0, 0]
    if sum(valid_measures)==0:
        print('0 medidas ocorridas')
        # nesse caso pegar o espectro aqui
        interrogator.disconnect()
        exit()
    for i in range(4):
        if valid_measures[i]:
            wavelengths_average[i] = channels_wavelengths[i] / valid_measures[i] / 10000
    
    ch1_acqs.append(wavelengths_average[0])
    if wavelengths_average[0] > maxval:
        maxval = wavelengths_average[0]
    if wavelengths_average[0] < minval:
        minval = wavelengths_average[0]
    plt.plot(nacq, ch1_acqs, color='k')
    nacq.append(nacq[-1]+1)
    xlim_min = nacq[-1]-number_of_samples
    xlim_max = nacq[-1]
    if xlim_min < 0:
        xlim_min = 0
        xlim_max = number_of_samples
        
    plt.xlim((xlim_min, xlim_max))
    plt.ylim((minval - (maxval - minval), maxval + (maxval - minval)))
    plt.draw()
    plt.pause(0.1)
    if len(nacq) > 2*number_of_samples:
        nacq = nacq[-2*number_of_samples:]
        ch1_acqs = ch1_acqs[-2*number_of_samples+1:]



interrogator.disconnect()
