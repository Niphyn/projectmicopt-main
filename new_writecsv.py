from data import Data
import matplotlib.pyplot as plt
from micronopt import *
import numpy as np
import pandas as pd
import shutil
import datetime
import os

def list_to_string(lst, sep=','):
    full_string = ''
    for item in lst:
        full_string += str(item)+sep
    return full_string[:-1]

directory = './data'
filename = directory+'/database.csv'

if not os.path.exists(directory):
  os.mkdir(directory)
  print("Folder %s created!" % directory)

interrogator = Interrogator()
interrogator.connect()

while True:
    plt.pause(0.1)
    spectrum = interrogator.get_spectrum
    counter = spectrum.header['Counter']

    wavelengths = spectrum.channel1.wavelenghts
    ch1_spectrum = spectrum.channel1.data
    ch2_spectrum = spectrum.channel2.data
    ch3_spectrum = spectrum.channel3.data
    ch4_spectrum = spectrum.channel4.data
    
    interrogator.disconnect()
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_row = date+','+str(counter)+','+'{ch1:'+list_to_string(ch1_spectrum,':')+'},'+'{ch2:'+list_to_string(ch2_spectrum,':')+'},'+'{ch3:'+list_to_string(ch3_spectrum,':')+'},'+'{ch4:'+list_to_string(ch4_spectrum,':')+'}'

    if (os.path.isfile(filename) == 0) or (os.stat(filename).st_size == 0):
        #print('Sem header')
        with open(filename, 'a') as f:
            print('asd')
            #f.write('{wavelengths:'+list_to_string(wavelengths,':')+'}')

    with open(filename, 'a') as f:
        f.write('\n'+full_row)
    
    break

with open(filename, 'a') as f:
    f.close()
           

# interrogator.disconnect()       

    