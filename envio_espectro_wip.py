import mysql.connector
from micronopt import *
import numpy as np
import pandas as pd
import datetime
import requests
import json


interrogator = Interrogator()
interrogator.connect()

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


webhook_url = 'http://127.0.0.1:8000/webhook/receive/spectrum'
count = 0
i = True

while i :
    try:
        start_time = datetime.time()
        try:
            spectrum = interrogator.get_spectrum
        except:
            print('Erro na leitura do espectro')
            i = False
            break
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
            
        wave_lengths = wavelengths[::50]
        spectrum_ch1 = spectrum_ch1[::50]
        spectrum_ch2 = spectrum_ch2[::50]
        spectrum_ch3 = spectrum_ch3[::50]
        spectrum_ch4 = spectrum_ch4[::50]
        spectrum_data = {
            'wave_lengths': wave_lengths,
            'channel_1_values': spectrum_ch1,
            'channel_2_values': spectrum_ch2,
            'channel_3_values': spectrum_ch3,
            'channel_4_values': spectrum_ch4,
        }
        response = send_to_webhook(webhook_url, spectrum_data)
        print(response)
        conexao.commit()
        print("Mandado um Spectro")
        
        try:
            cursor.execute(sql)
        except:
            print('Erro na inserção dos dados')
            i = False
            break
    except:
        print("Erro genêrico que não sei o que deu errado")
        break

cursor.close()
conexao.close()
interrogator.disconnect()
