from __future__ import division, print_function
from data import Data
import matplotlib.pyplot as plt
from micronopt import *
from Interrogator import *
import time
import datetime

if __name__ == "__main__":
    escolha = 0
    while escolha != 4:
        print("\nEscolha uma opção:\n")
        print("1 - Flush Buffer")
        print("2 - Ler Picos")
        print("3 - Fazer Gráficos")
        print("4 - Sair\n")

        escolha = int(input("Digite sua escolha: "))

        if escolha == 1:
            interrogator = Interrogator()
            interrogator.connect()

            interrogator.flush_buffer()

            spectrum = interrogator.get_spectrum

            interrogator.flush_buffer()

            interrogator.disconnect()
            
        elif escolha == 2:
            interr = Interrogator()
            interr.connect()
            print(interr.idn)
            response = interr.get_peaks
            file = open('Peak.txt', 'a')
            file.write(str(datetime.date.today())+"\n")
            
            wavelengths, levels, peaks = interr.decode_peaks(response, True)
            i = 0
            while i < 4:
                print("Canal: "+str(i+1))
                file.write("Canal: "+str(i+1)+"\n")
                file.write("Peaks: "+ str(peaks[i])+"\n")
                file.write(str(wavelengths[i])+" "+ str(levels[i])+"\n")
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
            
        elif escolha == 3:
            interrogator = Interrogator()
            interrogator.connect()
            spectrum = interrogator.get_spectrum

            # print(spectrum.channel1.data)

            wavelengths = spectrum.channel1.wavelenghts/10000
            spectrum_ch1 = spectrum.channel1.data
            spectrum_ch2 = spectrum.channel2.data
            spectrum_ch3 = spectrum.channel3.data
            spectrum_ch4 = spectrum.channel4.data

            interrogator.disconnect()


            # Plotagem
            if True:
                fig, axs = plt.subplots(2, 2)

                axs[0,0].plot(wavelengths, spectrum_ch1)
                axs[0,0].set_title('Canal 1')

                axs[0,1].plot(wavelengths, spectrum_ch2)
                axs[0,1].set_title('Canal 2')

                axs[1,0].plot(wavelengths, spectrum_ch3)
                axs[1,0].set_title('Canal 3')

                axs[1,1].plot(wavelengths, spectrum_ch4)
                axs[1,1].set_title('Canal 4')
                plt.show()


            # Salvar dados num arquivo
            filename = 'saved_data'
            if True: 
                full_data = np.array([wavelengths, spectrum_ch1, spectrum_ch2, spectrum_ch3, spectrum_ch4]).T
                np.savetxt(filename+'.txt', full_data)
        elif escolha == 4:
            print("Obrigado por utilizar o programa!")
            time.sleep(2)
            exit()    
        else:
            print("Opção inválida")
