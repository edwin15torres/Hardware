import serial
import time

# Configuración
velocidad = 9600
mensaje = b'Hola, cliente!\r\n'  # Texto que se mostrará

# Lista de puertos COM a probar (COM1 a COM20)
puertos_a_probar = [f'COM{i}' for i in range(1, 21)]

print("Buscando puerto COM disponible...")
print(f"Probando puertos: {', '.join(puertos_a_probar[:5])}... hasta COM20\n")

puerto_encontrado = False

for puerto in puertos_a_probar:
    try:
        print(f"Intentando conectar al puerto {puerto} a {velocidad} baudios...", end=' ')
        ser = serial.Serial(puerto, velocidad, timeout=1)
        print(f"[OK]")
        print(f"[OK] Conexion exitosa al puerto {puerto}")
        
        print("Enviando mensaje al visor...")
        ser.write(mensaje)
        time.sleep(1)
        
        ser.close()
        print(f"[OK] Mensaje enviado correctamente al puerto {puerto}. Puerto cerrado.")
        puerto_encontrado = True
        break  # Salir del ciclo si se envió correctamente
        
    except serial.SerialException as e:
        print(f"[FALLO] - {str(e)[:50]}...")
        continue  # Intentar con el siguiente puerto
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        continue  # Intentar con el siguiente puerto

if not puerto_encontrado:
    print("\n[ERROR] No se pudo conectar a ningun puerto COM disponible.")
    print("Verifica que:")
    print("  - El dispositivo este conectado")
    print("  - El dispositivo este encendido")
    print("  - No haya otro programa usando el puerto")
    print("  - Los drivers del dispositivo esten instalados correctamente")
