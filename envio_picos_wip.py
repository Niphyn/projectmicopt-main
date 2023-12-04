import mysql.connector
from micronopt import *
import datetime
import numpy as np
import pandas as pd
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
        print('Picos inseridos')
    except Exception as e:
        print(e)
        print('Erro na leitura/insercao dos picos')
        break
 
cursor.close()
conexao.close()
interr.disconnect()
