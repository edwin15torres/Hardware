# Instrucciones para ejecutar imprimir.py

## Instalación de dependencias

1. Asegúrate de estar en el entorno virtual (env):
   ```bash
   # Si no estás en el entorno virtual, actívalo primero
   # En Windows:
   env\Scripts\activate
   ```

2. Instala las dependencias desde el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

   O instala manualmente:
   ```bash
   pip install pywin32 PyQt5 Pillow
   ```

## Ejecución del script

Una vez instaladas las dependencias, ejecuta el script:

```bash
python imprimir.py
```

O si usas `py`:

```bash
py imprimir.py
```

## Notas

- El script requiere Windows (usa `win32print`, `win32ui`, `win32con`)
- Necesita una impresora configurada como predeterminada en Windows
- El archivo `logo.png` debe estar en el mismo directorio que `imprimir.py`
