import serial
import time

# Reemplaza con el puerto correspondiente en tu sistema (ej: COM3 o /dev/ttyUSB0)
puerto = 'COM3'
velocidad = 9600

try:
    print(f"Intentando conectar al puerto {puerto} a {velocidad} baudios...")
    ser = serial.Serial(puerto, velocidad, timeout=1)
    print(f"[OK] Conexion exitosa al puerto {puerto}")
    
    print("Enviando mensaje al visor...")
    ser.write(b'Hola, cliente!\r\n')  # Texto que se mostrará
    time.sleep(1)
    
    ser.close()
    print("[OK] Mensaje enviado correctamente. Puerto cerrado.")
except serial.SerialException as e:
    print(f"[ERROR] Error al abrir el puerto {puerto}: {e}")
    print("Verifica que:")
    print("  - El dispositivo este conectado")
    print("  - El puerto COM sea correcto (puede ser COM1, COM2, COM4, etc.)")
    print("  - No haya otro programa usando el puerto")
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
