from __future__ import division, print_function
from data import Data
import matplotlib.pyplot as plt
from micronopt import *
#from Interrogator import *
import time
import datetime

interr = Interrogator()
interr.connect()
print(interr.idn)
response = interr.get_peaks

file = open('Peak.txt', 'a')
file.write(str(datetime.date.today())+"\n")

wavelengths, levels, peaks = interr.decode_peaks(response, True)
interr.disconnect()
i = 0
exit()
while i < 4:
    print("Canal: "+str(i+1))
    file.write("Canal: "+str(i+1)+"\n")
    file.write("Peaks: "+ str(peaks[i])+"\n")
    print(str(wavelengths[i][0])+" "+ str(levels[i][0])+"\n")
    resultado = str(interr.get_ch_state(i+1))
    file.write(resultado+"\n")
    resultado = str(interr.get_peak_threshold(i+1))
    file.write(resultado+"\n")
    resultado = str(interr.get_peak_width(i+1))
    file.write(resultado+"\n")
    resultado = str(interr.get_peak_width_level(i+1))
    file.write(resultado+"\n")
    resultado = str(interr.get_rel_peak_threshold(i+1))
    file.write(resultado+"\n")
    i += 1
file.close()
interr.disconnect()
