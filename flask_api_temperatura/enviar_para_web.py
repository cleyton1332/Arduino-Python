import serial
import requests

porta = 'COM3'   # Troque se for outra porta
baudrate = 9600
url_api = 'http://127.0.0.1:5000/temperatura'

arduino = serial.Serial(porta, baudrate)
arduino.reset_input_buffer()  # limpa o lixo da porta
print("Conectado ao Arduino. Enviando dados para o servidor...\n")

while True:
    if arduino.in_waiting:
        dado = arduino.readline().decode(errors='ignore').strip()
        print("🌡️ Temperatura recebida:", dado)

        try:
            response = requests.post(url_api, json={"temperatura": dado})
            if response.status_code == 200:
                print("✅ Enviado para a API:", response.json())
            else:
                print("⚠️ Erro ao enviar:", response.text)
        except Exception as e:
            print("❌ Erro de conexão com a API:", e)
