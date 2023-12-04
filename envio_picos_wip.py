import mysql.connector
from micronopt import *
import datetime
import numpy as np
import pandas as pd
import time
import requests
import json

interr = Interrogator()
interr.connect()

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='sensor_petrobras',
)

cursor = conexao.cursor()

def send_to_webhook(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.text


webhook_url = 'http://127.0.0.1:8000/webhook/receive/'
count = 0
i = True
while i:
    try: 
        response = interr.get_peaks
        wavelengths, levels, peaks = interr.decode_peaks(response, True)
        date_time = datetime.datetime.now()
        sql = f'INSERT INTO app_sensor_petrobras_peaks (date_time, n_peaks_ch1, channel_1_x, channel_1_y, n_peaks_ch2, channel_2_x, channel_2_y, n_peaks_ch3, channel_3_x, channel_3_y, n_peaks_ch4, channel_4_x, channel_4_y) VALUES ("{date_time}", {peaks[0]}, {wavelengths[0][0]}, {levels[0][0]}, {peaks[1]}, {wavelengths[1][0]}, {levels[1][0]}, {peaks[2]}, {wavelengths[2][0]}, {levels[2][0]}, {peaks[3]}, {wavelengths[3][0]}, {levels[3][0]})'
        cursor.execute(sql)
        conexao.commit()
        response = send_to_webhook(webhook_url, "Novo_Pico")
        #print(response)
        print('Picos inseridos')
        i = False
    except Exception as e:
        print(e)
        print('Erro na leitura/insercao dos picos')
        break
        try:
            spectrum = interr.get_spectrum
            date_time = datetime.datetime.now()
            wavelengths = spectrum.channel1.wavelenghts
            spectrum_ch1 = spectrum.channel1.data
            spectrum_ch2 = spectrum.channel2.data
            spectrum_ch3 = spectrum.channel3.data
            spectrum_ch4 = spectrum.channel4.data
            counter = spectrum.header['Counter']
            n = 0
            while n < len(wavelengths):
                sql = f'INSERT INTO app_sensor_petrobras_spectrum (date_time, wave_length, channel_1, channel_2, channel_3, channel_4, counter) VALUES ("{date_time}", {wavelengths[n]}, {spectrum_ch1[n]}, {spectrum_ch2[n]}, {spectrum_ch3[n]}, {spectrum_ch4[n]}, {counter})'
                n += 1
                cursor.execute(sql)
            conexao.commit()
            print('Espectro inserido')
        except:
            print('Erro na leitura/insercao do espectro')
            i = False
            break

    
cursor.close()
conexao.close()
interr.disconnect()
