import serial
import time

# Reemplaza con el puerto correspondiente en tu sistema (ej: COM3 o /dev/ttyUSB0)
puerto = 'COM2'
velocidad = 9600

try:
    ser = serial.Serial(puerto, velocidad, timeout=1)
    ser.write(b'Papasito rico!\r\n')  # Texto que se mostrará
    time.sleep(1)
    ser.close()
except serial.SerialException as e:
    print("Error al abrir el puerto:", e)