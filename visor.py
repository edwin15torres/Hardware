import serial
import time

# Reemplaza 'COM3' con el puerto correcto en tu sistema
puerto = 'COM3'  
baudrate = 9600  # Velocidad de baudios típica, verifica la tuya

ser = serial.Serial(puerto, baudrate, timeout=1)

try:
    if ser.is_open:
        ser.write(b'Hola, cliente!\n')
        time.sleep(1)
finally:
    ser.close()
