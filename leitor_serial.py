import serial

# Altere para a porta COM correta do seu Arduino (ex: COM3, COM4, etc)
porta = 'COM3'
baudrate = 9600

try:
    arduino = serial.Serial(porta, baudrate)
    print("Conectado ao Arduino na porta", porta)
except:
    print(
        f"❌ Não foi possível conectar à porta {porta}. Verifique a conexão e a porta correta.")
    exit()

print("Lendo dados do Arduino...\n")

while True:
    try:
        if arduino.in_waiting:
            linha = arduino.readline().decode('utf-8').strip()
            print("🌡️ Temperatura recebida:", linha)
    except Exception as e:
        print("Erro ao ler:", e)
        break
