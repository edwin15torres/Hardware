# 🌐 Guía de Configuración de ngrok para Acceso Remoto a la API REST

## 📁 Estructura del Proyecto

Este proyecto (`Chorizos_app_local`) tiene la siguiente estructura:

```
Chorizos_app_local/
├── src/
│   └── backend/
│       ├── server_api.py      # Servidor Flask principal
│       ├── model/              # Modelos de base de datos
│       ├── view/               # Vistas y rutas de la API
│       └── database/           # Base de datos SQLite
└── Documentacion/
    └── 2_NGROK_SETUP.md        # Este archivo
```

El servidor Flask se ejecuta desde `src/backend/server_api.py` y corre en el puerto **5000**.

---

## ¿Qué es ngrok?

**ngrok** es una herramienta que crea un túnel seguro desde internet hacia tu servidor local. Básicamente, convierte tu aplicación que corre en `localhost` (por ejemplo, `http://localhost:5000`) en una URL pública accesible desde cualquier lugar del mundo.

## ¿Para qué sirve en este proyecto?

Si quieres acceder a tu API REST desde **otro computador** o dispositivo en la misma red o en internet, necesitas exponer tu servidor Flask local. Como `localhost:5000` solo es accesible desde tu computador, usamos ngrok para crear una URL pública (como `https://abc123.ngrok-free.dev`) que redirige automáticamente a tu servidor local.

**Flujo:**
```
Otro computador/dispositivo → ngrok URL pública → Tu servidor local (localhost:5000)
```

Sin ngrok, otros dispositivos no podrían acceder a tu API porque está corriendo solo en tu computador local.

---

## 📋 Pasos para Configurar ngrok

### Paso 1: Crear cuenta en ngrok (GRATIS)

1. Ve a: [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. Puedes registrarte con:
   - Google
   - GitHub
   - Email
3. **No hay costo** para el plan gratuito que necesitamos.

---

### Paso 2: Obtener tu Authtoken

1. Una vez dentro del dashboard de ngrok:
   - Ve a la sección **"Getting Started"** o **"Your Authtoken"**
   - Copia el token (será algo largo, tipo `2Jd8x...` o `38VWjj5lhzKGk6UIsukX9WuYrfJ_3Ud1MyqYMZ3mVoy1Wc4RV`)

---

### Paso 3: Descargar ngrok

1. Ve a: [https://ngrok.com/download/windows?tab=download](https://ngrok.com/download/windows?tab=download)
   - (Si usas Linux o Mac, selecciona la versión correspondiente)
2. Extrae el archivo ejecutable (`ngrok.exe` en Windows) en una carpeta de tu preferencia.
   - Ejemplo: `C:\ngrok\ngrok.exe` o `F:\Driver_descargados\ngrok-v3-stable-windows-amd64\ngrok.exe`

---

### Paso 4: Configurar el Authtoken

**⚠️ IMPORTANTE:** Debes usar la **ruta completa** al ejecutable de ngrok. No puedes usar solo `ngrok` a menos que lo hayas agregado al PATH del sistema.

Abre una terminal (PowerShell, CMD o Git Bash) y ejecuta:

```bash
# Reemplaza la ruta con la ubicación de tu ngrok.exe
# Reemplaza TU_AUTHTOKEN_AQUI con el token que copiaste del dashboard

C:\ruta\a\ngrok.exe config add-authtoken TU_AUTHTOKEN_AQUI
```

**Ejemplo en PowerShell o CMD:**
```bash
# Si descargaste ngrok en F:\Driver_descargados\ngrok-v3-stable-windows-amd64\
F:\Driver_descargados\ngrok-v3-stable-windows-amd64\ngrok.exe config add-authtoken 38VWjj5lhzKGk6UIsukX9WuYrfJ_3Ud1MyqYMZ3mVoy1Wc4RV

# O si lo pusiste en C:\ngrok\
C:\ngrok\ngrok.exe config add-authtoken 38VWjj5lhzKGk6UIsukX9WuYrfJ_3Ud1MyqYMZ3mVoy1Wc4RV
```

**Ejemplo en Git Bash:**
```bash
# Si ngrok está en F:\Driver_descargados\ngrok-v3-stable-windows-amd64\


# En Git Bash, F:\ se convierte en /f/
/f/Driver_descargados/ngrok-v3-stable-windows-amd64/ngrok.exe config add-authtoken 38VWjj5lhzKGk6UIsukX9WuYrfJ_3Ud1MyqYMZ3mVoy1Wc4RV
```

**En Git Bash (Windows):**
```bash
# Si estás en Git Bash, usa la ruta con formato Unix (/f/ en lugar de F:\)
# Ejemplo si ngrok está en F:\Driver_descargados\ngrok-v3-stable-windows-amd64\
/f/Driver_descargados/ngrok-v3-stable-windows-amd64/ngrok.exe config add-authtoken TU_AUTHTOKEN_AQUI

# O también puedes usar la ruta de Windows con barras invertidas dobles
F:\\Driver_descargados\\ngrok-v3-stable-windows-amd64\\ngrok.exe config add-authtoken TU_AUTHTOKEN_AQUI
```

Deberías ver:
```
Authtoken saved to configuration file: C:\Users\TU_USUARIO\AppData\Local\ngrok\ngrok.yml
```

**Nota:** Este paso solo lo necesitas hacer **una vez**. El token se guarda y no necesitas volver a configurarlo.

**💡 Consejo:** Si quieres usar solo `ngrok` sin la ruta completa, puedes:
1. Agregar la carpeta de ngrok al PATH del sistema (Windows)
2. O crear un alias en tu terminal

---

### Paso 5: Iniciar tu servidor Flask

Antes de iniciar ngrok, asegúrate de que tu servidor Flask esté corriendo:

**⚠️ IMPORTANTE:** Asegúrate de estar en la raíz del proyecto (`Chorizos_app_local`) cuando ejecutes los comandos.

**Desde la raíz del proyecto (`Chorizos_app_local`):**

```bash
# Opción 1: Ejecutar directamente
python src/backend/server_api.py

# Opción 2: Ejecutar como módulo
python -m src.backend.server_api
```

**Si usas un entorno virtual (recomendado):**

```bash
# Activar el entorno virtual (si existe)
source env/Scripts/activate  # En Windows con Git Bash
# O simplemente: env\Scripts\activate  # En CMD/PowerShell

# Luego ejecutar el servidor
python src/backend/server_api.py
```

Deberías ver:
```
============================================================
Servidor API REST iniciado
============================================================
Base de datos: .../src/backend/database/chorizos.db
Endpoints disponibles en: http://localhost:5000

Endpoints:
  POST   /api/login
  GET    /api/usuarios
  ...
============================================================
 * Running on http://0.0.0.0:5000
```

**Mantén esta terminal abierta** mientras usas ngrok.

---

### Paso 6: Iniciar ngrok

Abre **otra terminal** (deja la de Flask corriendo) y ejecuta:

```bash
# Reemplaza la ruta con la ubicación de tu ngrok.exe
# El número 5000 es el puerto donde corre tu Flask

C:\ruta\a\ngrok.exe http 5000
```

**Ejemplo:**
```bash
# Usa la misma ruta que usaste en el Paso 4
F:\Driver_descargados\ngrok-v3-stable-windows-amd64\ngrok.exe http 5000

# O si lo pusiste en C:\ngrok\
C:\ngrok\ngrok.exe http 5000
```

**⚠️ Recuerda:** Debes usar la **ruta completa** al ejecutable. Si ves el error `bash: ngrok: command not found`, significa que no estás usando la ruta completa.

Deberías ver algo como:

```
ngrok                                                               (Ctrl+C to quit)

Session Status                online
Account                       tu-email@gmail.com (Plan: Free)
Version                       3.35.0
Region                        United States (us)
Forwarding                    https://abc123-def456.ngrok-free.dev -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**⚠️ IMPORTANTE:** 
- **Copia la URL que aparece en "Forwarding"** (la que termina en `.ngrok-free.dev`)
- **Mantén esta terminal abierta** mientras necesites acceso remoto. Si cierras ngrok, la API dejará de ser accesible desde otros dispositivos.
- Esta URL es tu **endpoint público** para acceder a la API desde cualquier lugar.

---

### Paso 7: Probar el acceso remoto

Ahora puedes acceder a tu API desde cualquier dispositivo usando la URL de ngrok.

**Ejemplo de uso desde otro computador:**

```bash
# Obtener token de autenticación
curl -X POST https://abc123-def456.ngrok-free.dev/api/login \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario": "tu_usuario", "contrasena": "tu_contrasena"}'

# Listar productos (requiere token JWT)
curl -X GET https://abc123-def456.ngrok-free.dev/api/productos \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

**Desde un navegador web:**
- Puedes acceder directamente a: `https://abc123-def456.ngrok-free.dev/api/productos` (si no requiere autenticación)
- O usar herramientas como Postman, Insomnia, o cualquier cliente HTTP

---

## ✅ Verificación

Para verificar que todo funciona:

1. **Revisa que ambos servicios estén corriendo:**
   - ✅ Flask en `http://127.0.0.1:5000`
   - ✅ ngrok mostrando la URL pública

2. **Prueba el acceso desde otro dispositivo:**
   - Desde otro computador en la misma red o en internet
   - Desde tu teléfono móvil
   - Usa la URL de ngrok (ej: `https://abc123-def456.ngrok-free.dev`)

3. **Prueba un endpoint simple:**
   ```bash
   # Desde otro computador o dispositivo
   curl https://TU_URL_NGROK.ngrok-free.dev/api/login \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"nombre_usuario": "test", "contrasena": "test"}'
   ```

4. **Revisa las terminales:**
   - En la terminal de Flask deberías ver logs de las peticiones recibidas
   - En la terminal de ngrok deberías ver conexiones activas en la sección "Connections"

---

## 🔄 Reiniciar ngrok

Cada vez que reinicies ngrok, **obtendrás una URL diferente**. Si esto pasa:

1. Copia la nueva URL de ngrok
2. **Actualiza la URL en tu cliente/aplicación** que esté usando la API
3. Si estás usando la API desde otro computador, actualiza la URL base en tu código o configuración

**Consejo:** Si necesitas una URL fija, considera usar un plan de pago de ngrok o desplegar tu API en un servidor en la nube.

---

## 💻 Ejemplos de Uso desde Otro Computador

Una vez que tengas ngrok corriendo, puedes usar la API desde cualquier dispositivo. Aquí tienes algunos ejemplos:

### Ejemplo 1: Login y obtener token

```bash
# Desde otro computador
curl -X POST https://abc123-def456.ngrok-free.dev/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "tu_usuario",
    "contrasena": "tu_contrasena"
  }'
```

**Respuesta esperada:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "id_usuario": 1,
  "nombre_usuario": "tu_usuario",
  "rol": "ADMINISTRADOR"
}
```

### Ejemplo 2: Listar productos (requiere autenticación)

```bash
# Usa el token obtenido en el paso anterior
curl -X GET https://abc123-def456.ngrok-free.dev/api/productos \
  -H "Authorization: Bearer TU_TOKEN_JWT_AQUI"
```

### Ejemplo 3: Crear un producto

```bash
curl -X POST https://abc123-def456.ngrok-free.dev/api/productos \
  -H "Authorization: Bearer TU_TOKEN_JWT_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_producto": "Chorizo Premium",
    "precio": 15000,
    "id_usuario": 1
  }'
```

### Ejemplo 4: Desde Python (otro computador)

```python
import requests

# URL base de tu API (usa la URL de ngrok)
BASE_URL = "https://abc123-def456.ngrok-free.dev"

# 1. Login
response = requests.post(
    f"{BASE_URL}/api/login",
    json={
        "nombre_usuario": "tu_usuario",
        "contrasena": "tu_contrasena"
    }
)
token = response.json()["token"]

# 2. Obtener productos
headers = {"Authorization": f"Bearer {token}"}
productos = requests.get(f"{BASE_URL}/api/productos", headers=headers)
print(productos.json())
```

### Ejemplo 5: Desde JavaScript/Node.js (otro computador)

```javascript
const axios = require('axios');

const BASE_URL = 'https://abc123-def456.ngrok-free.dev';

// 1. Login
const loginResponse = await axios.post(`${BASE_URL}/api/login`, {
  nombre_usuario: 'tu_usuario',
  contrasena: 'tu_contrasena'
});

const token = loginResponse.data.token;

// 2. Obtener productos
const productosResponse = await axios.get(`${BASE_URL}/api/productos`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

console.log(productosResponse.data);
```

---

## ⚠️ Limitaciones del Plan Gratuito

- **URL temporal:** La URL cambia cada vez que reinicias ngrok (a menos que uses un plan de pago)
- **Límite de conexiones:** Puede haber límites en el número de conexiones simultáneas
- **Banner de advertencia:** Algunas veces ngrok muestra un banner de advertencia antes de acceder (esto es normal en el plan gratuito)

---

## 🚀 Alternativas para Producción

Para producción, en lugar de ngrok, deberías usar:
- **Servidor en la nube** (AWS, Google Cloud, Azure, Heroku, etc.)
- **Dominio propio** con certificado SSL
- **ngrok con plan de pago** (URL fija y sin límites)

---

## 📝 Resumen Rápido

```bash
# 1. Configurar authtoken (solo una vez)
# ⚠️ Usa la ruta completa a ngrok.exe
C:\ruta\a\ngrok.exe config add-authtoken TU_TOKEN

# 2. Iniciar Flask (desde la raíz del proyecto)
python src/backend/server_api.py

# 3. En otra terminal, iniciar ngrok (usa la misma ruta completa)
C:\ruta\a\ngrok.exe http 5000

# 4. Copiar la URL de ngrok (ej: https://abc123.ngrok-free.dev)
# Usa esta URL para acceder a la API desde otros dispositivos:
# https://TU_URL.ngrok-free.dev/api/login
# https://TU_URL.ngrok-free.dev/api/productos
# etc.
```

**Notas importantes:**
- Asegúrate de estar en la raíz del proyecto (`Chorizos_app_local`) cuando ejecutes el servidor Flask
- **Siempre usa la ruta completa** a `ngrok.exe` (ej: `C:\ngrok\ngrok.exe` o `F:\Downloads\ngrok.exe`)
- Si ves "command not found", significa que no estás usando la ruta completa

---

## 🆘 Solución de Problemas

### Error: "bash: ngrok: command not found" o "ngrok: command not found"

Este error significa que no estás usando la ruta completa al ejecutable de ngrok.

**Solución:**
1. **Encuentra dónde descargaste ngrok:**
   - Busca el archivo `ngrok.exe` en tu computador
   - Puede estar en: `Descargas`, `Downloads`, o donde lo hayas extraído

2. **Usa la ruta completa:**
   ```bash
   # En lugar de:
   ngrok config add-authtoken TU_TOKEN
   
   # Usa:
   C:\ruta\completa\a\ngrok.exe config add-authtoken TU_TOKEN
   ```

3. **Ejemplo si está en Descargas:**
   ```bash
   # En PowerShell o CMD:
   C:\Users\TU_USUARIO\Downloads\ngrok.exe config add-authtoken TU_TOKEN
   
   # En Git Bash:
   /c/Users/TU_USUARIO/Downloads/ngrok.exe config add-authtoken TU_TOKEN
   ```

4. **Alternativa: Agregar ngrok al PATH (opcional):**
   - Copia `ngrok.exe` a una carpeta como `C:\ngrok\`
   - Agrega `C:\ngrok` a las variables de entorno PATH de Windows
   - Luego podrás usar solo `ngrok` sin la ruta completa

### Error: "authtoken not found"
- Asegúrate de haber ejecutado `ngrok config add-authtoken` correctamente
- Verifica que usaste la ruta completa al ejecutable

### Error: "port 5000 already in use"
- Cierra otros programas que usen el puerto 5000, o cambia el puerto en Flask y ngrok
- Verifica que tu servidor Flask esté corriendo antes de iniciar ngrok

### No puedo acceder a la API desde otro dispositivo
- Verifica que ngrok esté corriendo (debe mostrar "Session Status: online")
- Verifica que estés usando la URL correcta de ngrok (la que aparece en "Forwarding")
- Asegúrate de incluir `https://` en la URL
- Revisa los logs de Flask para ver si llegan las peticiones
- Verifica que el firewall no esté bloqueando las conexiones
- Asegúrate de que tu servidor Flask esté corriendo en el puerto 5000

### La URL de ngrok cambia constantemente
- Esto es normal en el plan gratuito. Considera un plan de pago si necesitas una URL fija.

---

**¿Necesitas ayuda?** Revisa la documentación oficial de ngrok: [https://ngrok.com/docs](https://ngrok.com/docs)
