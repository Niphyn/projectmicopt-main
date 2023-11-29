
from data import Data
import matplotlib.pyplot as plt
from micronopt import *
import numpy as np
import pandas as pd
import shutil
import datetime
from os import mkdir, path



directory = './data'

# check whether directory already exists
if not path.exists(directory):
  mkdir(directory)
  print("Folder %s created!" % directory)
# else:
#   print("Folder %s already exists" % path)


interrogator = Interrogator()
interrogator.connect()

fig, axs = plt.subplots(2, 2)

plt.ion() 

while True:
    spectrum = interrogator.get_spectrum

    wavelengths = spectrum.channel1.wavelenghts/10000
    spectrum_ch1 = spectrum.channel1.data
    spectrum_ch2 = spectrum.channel2.data
    spectrum_ch3 = spectrum.channel3.data
    spectrum_ch4 = spectrum.channel4.data

    # Limpa os dados antigos do gráfico
    for ax in axs.flat:
        ax.clear()

    # Adiciona novos dados ao gráfico
    axs[0,0].plot(wavelengths, spectrum_ch1)
    axs[0,0].set_title('Canal 1')

    axs[0,1].plot(wavelengths, spectrum_ch2)
    axs[0,1].set_title('Canal 2')

    axs[1,0].plot(wavelengths, spectrum_ch3)
    axs[1,0].set_title('Canal 3')

    axs[1,1].plot(wavelengths, spectrum_ch4)
    axs[1,1].set_title('Canal 4')

    # Redesenha o gráfico e pausa por 0.1 segundos
    plt.draw()
    plt.pause(0.1)

    # Salvar dados num arquivo a cada iteração
    full_data = np.array([wavelengths, spectrum_ch1, spectrum_ch2, spectrum_ch3, spectrum_ch4]).T
    csv = pd.DataFrame(full_data, columns=['wavelengths', 'spectrum_ch1', 'spectrum_ch2', 'spectrum_ch3', 'spectrum_ch4'])
    
    csv['contador'] = spectrum.header['Counter']
    csv['numero_de_dados'] = len(csv)
    csv['data'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    csv.to_csv('saved_data.csv', mode='a', index=False)
  
    print('Contador:', spectrum.header['Counter'])

    f_name = './data/database_' + str(spectrum.header['Counter']) + '.csv'
    if spectrum.header['Counter'] % 10 == 9:
        shutil.copyfile('saved_data.csv', f_name)
        open('saved_data.csv', 'w').close()
    
    if spectrum.header['Counter'] >17000:
        break


plt.ioff()

interrogator.disconnect()
