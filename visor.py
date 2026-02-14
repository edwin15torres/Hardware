import serial
import time

# Configuración
velocidades_a_probar = [9600, 4800, 19200, 38400, 115200, 2400]  # Velocidades comunes
mensaje_texto = "Hola, cliente!"  # Texto que se mostrará

# Lista de puertos COM a probar (COM1 a COM20)
puertos_a_probar = [f'COM{i}' for i in range(1, 21)]

print("Buscando puerto COM disponible...")
print(f"Probando puertos: {', '.join(puertos_a_probar[:5])}... hasta COM20")
print(f"Probando velocidades: {', '.join(map(str, velocidades_a_probar))} baudios\n")

puerto_encontrado = False

def enviar_mensaje_visor(ser, texto):
    """
    Envía mensaje al visor usando diferentes protocolos comunes.
    Prueba varios métodos hasta encontrar el que funcione.
    """
    texto_bytes = texto.encode('utf-8', errors='ignore')
    
    # Métodos comunes para visores de cliente
    metodos = [
        # Método 1: ESC/POS - Limpiar pantalla y mostrar texto
        ("ESC/POS (Clear + Text)", lambda: ser.write(b'\x1B[2J\x1B[H' + texto_bytes + b'\r\n')),
        
        # Método 2: Form Feed (limpiar pantalla) + texto
        ("Form Feed + Text", lambda: ser.write(b'\x0C' + texto_bytes + b'\r\n')),
        
        # Método 3: Reset ESC @ + texto
        ("Reset ESC @ + Text", lambda: ser.write(b'\x1B\x40' + texto_bytes + b'\r\n')),
        
        # Método 4: CLS (comando de limpieza) + texto
        ("CLS + Text", lambda: ser.write(b'CLS\r\n' + texto_bytes + b'\r\n')),
        
        # Método 5: Solo limpiar con ESC [2J y luego texto
        ("ESC Clear + Text", lambda: ser.write(b'\x1B[2J' + texto_bytes + b'\r\n')),
        
        # Método 6: Texto simple con CRLF (método original)
        ("Simple CRLF", lambda: ser.write(texto_bytes + b'\r\n')),
        
        # Método 7: Texto simple con LF
        ("Simple LF", lambda: ser.write(texto_bytes + b'\n')),
        
        # Método 8: Home cursor + texto
        ("Home + Text", lambda: ser.write(b'\x1B[H' + texto_bytes + b'\r\n')),
    ]
    
    print("  Probando diferentes protocolos de visor...")
    for nombre, metodo in metodos:
        try:
            print(f"    - {nombre}...", end=' ')
            metodo()
            time.sleep(0.3)  # Dar tiempo al visor para procesar
            print("[OK]")
            # No retornamos inmediatamente, probamos todos para ver cuál funciona
        except Exception as e:
            print(f"[FALLO]")
            continue
    
    return True

for puerto in puertos_a_probar:
    for velocidad in velocidades_a_probar:
        try:
            print(f"Intentando conectar al puerto {puerto} a {velocidad} baudios...", end=' ')
            ser = serial.Serial(
                puerto, 
                velocidad, 
                timeout=1,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"[OK]")
            print(f"[OK] Conexion exitosa al puerto {puerto} a {velocidad} baudios")
            
            print("Enviando mensaje al visor...")
            enviar_mensaje_visor(ser, mensaje_texto)
            
            print(f"\n[OK] Todos los metodos de envio probados en puerto {puerto} ({velocidad} baudios)")
            print("     Revisa el visor para ver cual metodo funciono.")
            print("     Si ninguno funciona, verifica:")
            print("     - El protocolo especifico de tu visor")
            print("     - Que el visor este encendido y configurado correctamente")
            print("     - El manual del visor para comandos especificos")
            
            time.sleep(1)
            ser.close()
            print(f"[OK] Puerto cerrado.")
            puerto_encontrado = True
            break  # Salir del ciclo de velocidades si se conectó
            
        except serial.SerialException as e:
            print(f"[FALLO] - {str(e)[:50]}...")
            continue  # Intentar con la siguiente velocidad
        except Exception as e:
            print(f"[ERROR] Error inesperado: {e}")
            continue  # Intentar con la siguiente velocidad
    
    if puerto_encontrado:
        break  # Salir del ciclo de puertos si se encontró uno funcional

if not puerto_encontrado:
    print("\n[ERROR] No se pudo conectar a ningun puerto COM disponible.")
    print("Verifica que:")
    print("  - El dispositivo este conectado")
    print("  - El dispositivo este encendido")
    print("  - No haya otro programa usando el puerto")
    print("  - Los drivers del dispositivo esten instalados correctamente")
