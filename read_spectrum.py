# from data import Data
import matplotlib.pyplot as plt
from micronopt import *
import numpy as np
# import pandas as pd
# import shutil
# import datetime
# from os import mkdir, path

interrogator = Interrogator()
interrogator.connect()


print(interrogator.idn)

print('\nMain header:')
header = interrogator.get_spectrum.header
for item in header:
    print(item, ":", header[item])

ch1_data = interrogator.get_spectrum.channel1
ch2_data = interrogator.get_spectrum.channel2
ch3_data = interrogator.get_spectrum.channel3
ch4_data = interrogator.get_spectrum.channel4

print('\nChannel 1 subheader:')
for item in ch1_data.sub_header:
    print(item, ':', ch1_data.sub_header[item])

print('\nChannel 2 subheader:')
for item in ch2_data.sub_header:
    print(item, ':', ch2_data.sub_header[item])

print('\nChannel 3 subheader:')
for item in ch3_data.sub_header:
    print(item, ':', ch3_data.sub_header[item])

print('\nChannel 4 subheader:')
for item in ch4_data.sub_header:
    print(item, ':', ch4_data.sub_header[item])


print('\n')
interrogator.disconnect()