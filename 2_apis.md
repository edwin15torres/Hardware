# Documentación de API REST

Esta documentación describe los endpoints disponibles para gestionar usuarios y productos en el sistema Chorizos.

## Iniciar el Servidor API

Para acceder a los endpoints de la API, primero debes iniciar el servidor Flask. El proyecto incluye un script dedicado para esto.

### Opción 1: Ejecutar desde la raíz del proyecto

```bash
# Desde la raíz del proyecto (F:\DevOps_local\Chorizos_app_local)
python src/backend/server_api.py
```

### Opción 2: Ejecutar como módulo

```bash
# Desde el directorio src
cd src
python -m backend.server_api
```

### Opción 3: Ejecutar desde el directorio backend

```bash
# Desde el directorio src/backend
cd src/backend
python server_api.py
```

Una vez iniciado, verás un mensaje similar a:

```
============================================================
Servidor API REST iniciado
============================================================
Base de datos: .../backend/database/chorizos.db
Endpoints disponibles en: http://localhost:5000

Endpoints:
  POST   /api/login
  GET    /api/usuarios
  POST   /api/usuarios
  GET    /api/usuarios/<id>
  PUT    /api/usuarios/<id>
  DELETE /api/usuarios/<id>

Presiona Ctrl+C para detener el servidor
============================================================
```

**Nota:** El servidor Flask debe estar ejecutándose para que los endpoints estén disponibles. La aplicación PyQt5 principal (`__main__.py`) no expone los endpoints REST automáticamente.

## Base URL

Por defecto, el servidor Flask se ejecuta en `http://localhost:5000`.

## Autenticación

Todos los endpoints (excepto `/api/login`) requieren autenticación mediante JWT (JSON Web Token). El token debe incluirse en el header `Authorization` de cada solicitud.

### Formato del Header de Autorización

```
Authorization: Bearer <token>
```


### Bootstrap: Crear primer usuario ADMINISTRADOR

Este endpoint se usa para crear el primer administrador del sistema.
No requiere JWT, pero solo funciona si todavia no existe ningun usuario con rol `ADMINISTRADOR`.

**Endpoint:** `POST /api/bootstrap/admin`

**Ejemplo en Git Bash (MINGW/Git):**
```bash
curl -X POST "http://localhost:5000/api/bootstrap/admin" -H "Content-Type: application/json" -d '{"nombre_usuario":"admin","contrasena":"123"}'

- Actualizar

curl -X PUT "http://localhost:5000/api/usuarios/password" -H "Content-Type: application/json" -d '{"nombre_usuario":"admin","nueva_contrasena":"admin"}'

```
```



**Respuestas esperadas:**
- `201` si se crea el primer administrador.
- `409` si ya existe un usuario `ADMINISTRADOR` o el nombre de usuario ya existe.


## Endpoints Disponibles

### 1. Login (Obtener Token JWT)

Autentica un usuario y devuelve un token JWT para acceder a los demás endpoints.

**Endpoint:** `POST /api/login`

**Autenticación:** No requerida

**Cuerpo de la solicitud (JSON):**
```json
{
  "nombre_usuario": "admin",
  "contrasena": "password123"
}
```

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "ADMINISTRADOR",
    "contrasena": "ADMINISTRADOR"
  }'

  curl -X POST https://subformative-marylee-solvently.ngrok-free.dev/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "ADMINISTRADOR",
    "contrasena": "ADMINISTRADOR"
  }'
  
```


**Respuesta exitosa (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "id_usuario": 1,
  "nombre_usuario": "admin",
  "rol": "ADMINISTRADOR"
}
```

**Respuesta de error (401):**
```json
{
  "mensaje": "Credenciales inválidas"
}
```

---

### 2. Obtener Todos los Usuarios

Obtiene una lista de todos los usuarios registrados en el sistema.

**Endpoint:** `GET /api/usuarios`

**Autenticación:** Requerida (JWT)

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MDc3MDkzMCwianRpIjoiMzE2MTlkNTAtOTUyMi00ODdmLTlkNmItOThjODE3MWYwYjg0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzcwNzcwOTMwLCJleHAiOjE3NzA3NzE4MzB9.HLJZKV4LpREzVTv783KPPPVSRNZAsvek02cWofQliDU"
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_usuario": 1,
    "nombre_usuario": "admin",
    "rol": "ADMINISTRADOR"
  },
  {
    "id_usuario": 2,
    "nombre_usuario": "cajero1",
    "rol": "CAJERO"
  }
]
```

**Respuesta de error (500):**
```json
{
  "mensaje": "Error al obtener usuarios: <descripción del error>"
}
```

---

### 3. Crear Nuevo Usuario

Crea un nuevo usuario en el sistema.

**Endpoint:** `POST /api/usuarios`

**Autenticación:** Requerida (JWT)

**Cuerpo de la solicitud (JSON):**
```json
{
  "nombre_usuario": "nuevo_usuario",
  "contrasena": "password123",
  "rol": "CAJERO"
}
```

**Parámetros:**
- `nombre_usuario` (requerido): Nombre único del usuario
- `contrasena` (requerido): Contraseña del usuario (se hasheará automáticamente)
- `rol` (opcional): Rol del usuario. Valores válidos: `"CAJERO"` o `"ADMINISTRADOR"`. Por defecto: `"CAJERO"`

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "nuevo_usuario",
    "contrasena": "password123",
    "rol": "CAJERO"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id_usuario": 3,
  "nombre_usuario": "nuevo_usuario",
  "rol": "CAJERO"
}
```

**Respuestas de error:**
- **400:** Datos inválidos
  ```json
  {
    "mensaje": "Se requieren nombre_usuario y contrasena"
  }
  ```
  o
  ```json
  {
    "mensaje": "El rol debe ser CAJERO o ADMINISTRADOR"
  }
  ```

- **409:** Usuario ya existe
  ```json
  {
    "mensaje": "El nombre de usuario ya existe"
  }
  ```

- **500:** Error del servidor
  ```json
  {
    "mensaje": "Error al crear usuario: <descripción del error>"
  }
  ```

---

### 4. Obtener Usuario por ID

Obtiene la información de un usuario específico por su ID.

**Endpoint:** `GET /api/usuarios/<id_usuario>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_usuario` (requerido): ID numérico del usuario

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "id_usuario": 1,
  "nombre_usuario": "admin",
  "rol": "ADMINISTRADOR"
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Usuario no encontrado"
}
```

---

### 5. Actualizar Usuario

Actualiza la información de un usuario existente.

**Endpoint:** `PUT /api/usuarios/<id_usuario>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_usuario` (requerido): ID numérico del usuario

**Cuerpo de la solicitud (JSON):**
```json
{
  "nombre_usuario": "usuario_actualizado",
  "contrasena": "nueva_password",
  "rol": "ADMINISTRADOR"
}
```

**Nota:** Todos los campos son opcionales. Solo se actualizarán los campos que se envíen en el JSON.

**Ejemplo con curl:**
```bash
curl -X PUT http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "usuario_actualizado",
    "contrasena": "nueva_password",
    "rol": "ADMINISTRADOR"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id_usuario": 1,
  "nombre_usuario": "usuario_actualizado",
  "rol": "ADMINISTRADOR"
}
```

**Respuestas de error:**
- **400:** Datos inválidos
  ```json
  {
    "mensaje": "Se requiere un cuerpo JSON con los datos a actualizar"
  }
  ```
  o
  ```json
  {
    "mensaje": "El rol debe ser CAJERO o ADMINISTRADOR"
  }
  ```

- **404:** Usuario no encontrado
  ```json
  {
    "mensaje": "Usuario no encontrado"
  }
  ```

- **409:** Nombre de usuario ya existe
  ```json
  {
    "mensaje": "El nombre de usuario ya existe"
  }
  ```

- **500:** Error del servidor
  ```json
  {
    "mensaje": "Error al actualizar usuario: <descripción del error>"
  }
  ```

---

### 6. Eliminar Usuario

Elimina un usuario del sistema.

**Endpoint:** `DELETE /api/usuarios/<id_usuario>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_usuario` (requerido): ID numérico del usuario

**Ejemplo con curl:**
```bash
curl -X DELETE http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Usuario eliminado exitosamente"
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Usuario no encontrado"
}
```

**Respuesta de error (500):**
```json
{
  "mensaje": "Error al eliminar usuario: <descripción del error>"
}
```

---

## Códigos de Estado HTTP

- **200 OK:** Solicitud exitosa
- **201 Created:** Recurso creado exitosamente
- **400 Bad Request:** Datos de entrada inválidos
- **401 Unauthorized:** Credenciales inválidas o token faltante/inválido
- **404 Not Found:** Recurso no encontrado
- **409 Conflict:** Conflicto (ej: usuario ya existe)
- **500 Internal Server Error:** Error del servidor

---

## Ejemplo de Flujo Completo

### 1. Obtener Token de Autenticación

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "admin",
    "contrasena": "password123"
  }' | jq -r '.token')

echo "Token obtenido: $TOKEN"
```

### 2. Usar el Token para Acceder a los Endpoints

```bash
# Obtener todos los usuarios
curl -X GET http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer $TOKEN"

# Crear un nuevo usuario
curl -X POST http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "nuevo_cajero",
    "contrasena": "password123",
    "rol": "CAJERO"
  }'

# Obtener un usuario específico
curl -X GET http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer $TOKEN"

# Actualizar un usuario
curl -X PUT http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rol": "ADMINISTRADOR"
  }'

# Eliminar un usuario
curl -X DELETE http://localhost:5000/api/usuarios/1 \
  -H "Authorization: Bearer $TOKEN"

# Obtener todos los productos
curl -X GET http://localhost:5000/api/productos \
  -H "Authorization: Bearer $TOKEN"


curl -X GET http://localhost:5000/api/productos \
  -H "Authorization: Bearer $TOKEN"


# Crear un nuevo producto
curl -X POST http://localhost:5000/api/productos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_producto": "Chorizo Especial",
    "precio": 6000,
    "id_usuario": 1
  }'

# Obtener un producto específico
curl -X GET http://localhost:5000/api/productos/1 \
  -H "Authorization: Bearer $TOKEN"

# Actualizar un producto
curl -X PUT http://localhost:5000/api/productos/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 7000
  }'

# Eliminar un producto
curl -X DELETE http://localhost:5000/api/productos/1 \
  -H "Authorization: Bearer $TOKEN"

# Obtener productos de un usuario
curl -X GET http://localhost:5000/api/usuarios/1/productos \
  -H "Authorization: Bearer $TOKEN"

# Obtener todas las transacciones
curl -X GET http://localhost:5000/api/transacciones \
  -H "Authorization: Bearer $TOKEN"


# Crear una nueva transacción
curl -X POST http://localhost:5000/api/transacciones \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_transaccion": "VENTA",
    "tipo_cuenta": "EFECTIVO",
    "id_usuario": 1,
    "items": [
      {
        "id_producto": 1,
        "cantidad": 2
      }
    ]
  }'

# Obtener una transacción específica
curl -X GET http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer $TOKEN"

# Actualizar una transacción
curl -X PUT http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cuenta": "BANCARIA"
  }'

# Eliminar una transacción
curl -X DELETE http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer $TOKEN"

# Obtener transacciones de un usuario
curl -X GET http://localhost:5000/api/usuarios/1/transacciones \
  -H "Authorization: Bearer $TOKEN"

# Obtener todos los items
curl -X GET http://localhost:5000/api/items \
  -H "Authorization: Bearer $TOKEN"

  curl -X GET http://localhost:5000/api/items \
  -H "Authorization: Bearer "

# Crear un nuevo item
curl -X POST http://localhost:5000/api/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id_producto": 1,
    "id_transaccion": 1,
    "cantidad": 2
  }'

# Obtener un item específico
curl -X GET http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer $TOKEN"

# Actualizar un item
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cantidad": 3
  }'

# Eliminar un item
curl -X DELETE http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer $TOKEN"

# Obtener items de una transacción
curl -X GET http://localhost:5000/api/transacciones/1/items \
  -H "Authorization: Bearer $TOKEN"

# Obtener items de un producto
curl -X GET http://localhost:5000/api/productos/1/items \
  -H "Authorization: Bearer $TOKEN"
```

---

## Endpoints de Transacciones

### 1. Obtener Todas las Transacciones

Obtiene una lista de todas las transacciones registradas en el sistema. Permite filtrar por tipo de transacción, tipo de cuenta y usuario.

**Endpoint:** `GET /api/transacciones`

**Autenticación:** Requerida (JWT)

**Query Parameters (opcionales):**
- `nombre_transaccion`: Filtrar por tipo de transacción (BASE, VENTA, COSTO, GASTO, ENTRADA_INV, SALIDA_INV)
- `tipo_cuenta`: Filtrar por tipo de cuenta (EFECTIVO, BANCARIA, ENTRADA)
- `id_usuario`: Filtrar por ID de usuario
- `include_items`: Incluir items asociados (true/false, por defecto: false)

**Ejemplo con curl:**
```bash
# Obtener todas las transacciones
curl -X GET http://localhost:5000/api/transacciones \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Obtener solo transacciones de tipo VENTA
curl -X GET "http://localhost:5000/api/transacciones?nombre_transaccion=VENTA" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Obtener transacciones con items incluidos
curl -X GET "http://localhost:5000/api/transacciones?include_items=true" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_transaccion": 1,
    "nombre_transaccion": "VENTA",
    "tipo_cuenta": "EFECTIVO",
    "id_factura": 1,
    "detalle_transaccion": "Venta",
    "fecha": "2024-01-15T10:30:00",
    "entrada": 15000.0,
    "egreso": 0.0,
    "id_usuario": 1
  }
]
```

---

### 2. Crear Nueva Transacción

Crea una nueva transacción en el sistema. Puede incluir items asociados.

**Endpoint:** `POST /api/transacciones`

**Autenticación:** Requerida (JWT)

**Cuerpo de la solicitud (JSON):**
```json
{
  "nombre_transaccion": "VENTA",
  "tipo_cuenta": "EFECTIVO",
  "id_usuario": 1,
  "entrada": 0.0,
  "egreso": 0.0,
  "detalle_transaccion": "Venta de productos",
  "items": [
    {
      "id_producto": 1,
      "cantidad": 2
    },
    {
      "id_producto": 2,
      "cantidad": 1
    }
  ]
}
```

**Parámetros:**
- `nombre_transaccion` (requerido): Tipo de transacción. Valores válidos: `BASE`, `VENTA`, `COSTO`, `GASTO`, `ENTRADA_INV`, `SALIDA_INV`
- `id_usuario` (requerido): ID del usuario que crea la transacción
- `tipo_cuenta` (opcional): Tipo de cuenta. Valores válidos: `EFECTIVO`, `BANCARIA`, `ENTRADA`. Por defecto: `EFECTIVO`
- `entrada` (opcional): Monto de entrada. Por defecto: `0.0`
- `egreso` (opcional): Monto de egreso. Por defecto: `0.0`
- `detalle_transaccion` (opcional): Detalle de la transacción. Por defecto: `"Venta"`
- `id_factura` (opcional): ID de factura. Para VENTA, se genera automáticamente si no se proporciona
- `items` (opcional): Array de items asociados. Cada item debe tener:
  - `id_producto` (requerido): ID del producto
  - `cantidad` (requerido): Cantidad del producto (número entero positivo)
  
**Nota:** Para transacciones de tipo `VENTA`, si se proporcionan items, el `entrada` se recalcula automáticamente como la suma de (cantidad × precio) de todos los productos.

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/transacciones \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_transaccion": "VENTA",
    "tipo_cuenta": "EFECTIVO",
    "id_usuario": 1,
    "detalle_transaccion": "Venta de productos",
    "items": [
      {
        "id_producto": 1,
        "cantidad": 2
      },
      {
        "id_producto": 2,
        "cantidad": 1
      }
    ]
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id_transaccion": 1,
  "nombre_transaccion": "VENTA",
  "tipo_cuenta": "EFECTIVO",
  "id_factura": 1,
  "detalle_transaccion": "Venta de productos",
  "fecha": "2024-01-15T10:30:00",
  "entrada": 15000.0,
  "egreso": 0.0,
  "id_usuario": 1,
  "items": [
    {
      "id_item": 1,
      "id_producto": 1,
      "cantidad": 2,
      "nombre_producto": "Chorizo",
      "precio_producto": 5000
    },
    {
      "id_item": 2,
      "id_producto": 2,
      "cantidad": 1,
      "nombre_producto": "Hamburguesa",
      "precio_producto": 8000
    }
  ]
}
```

**Respuestas de error:**
- **400:** Datos inválidos
  ```json
  {
    "mensaje": "Se requiere nombre_transaccion"
  }
  ```
  o
  ```json
  {
    "mensaje": "nombre_transaccion debe ser uno de: BASE, VENTA, COSTO, GASTO, ENTRADA_INV, SALIDA_INV"
  }
  ```

- **404:** Usuario o producto no existe
  ```json
  {
    "mensaje": "El usuario especificado no existe"
  }
  ```

---

### 3. Obtener Transacción por ID

Obtiene la información de una transacción específica por su ID.

**Endpoint:** `GET /api/transacciones/<id_transaccion>`

**Autenticación:** Requerida (JWT)

**Query Parameters (opcionales):**
- `include_items`: Incluir items asociados (true/false, por defecto: true)

**Parámetros de URL:**
- `id_transaccion` (requerido): ID numérico de la transacción

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "id_transaccion": 1,
  "nombre_transaccion": "VENTA",
  "tipo_cuenta": "EFECTIVO",
  "id_factura": 1,
  "detalle_transaccion": "Venta de productos",
  "fecha": "2024-01-15T10:30:00",
  "entrada": 15000.0,
  "egreso": 0.0,
  "id_usuario": 1,
  "items": [
    {
      "id_item": 1,
      "id_producto": 1,
      "cantidad": 2,
      "nombre_producto": "Chorizo",
      "precio_producto": 5000
    }
  ]
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Transacción no encontrada"
}
```

---

### 4. Actualizar Transacción

Actualiza la información de una transacción existente.

**Endpoint:** `PUT /api/transacciones/<id_transaccion>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_transaccion` (requerido): ID numérico de la transacción

**Cuerpo de la solicitud (JSON):**
```json
{
  "nombre_transaccion": "VENTA",
  "tipo_cuenta": "BANCARIA",
  "detalle_transaccion": "Venta actualizada",
  "entrada": 20000.0,
  "items": [
    {
      "id_producto": 1,
      "cantidad": 3
    }
  ]
}
```

**Nota:** Todos los campos son opcionales. Solo se actualizarán los campos que se envíen en el JSON. Si se proporcionan `items`, se reemplazarán todos los items existentes.

**Ejemplo con curl:**
```bash
curl -X PUT http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cuenta": "BANCARIA",
    "detalle_transaccion": "Venta actualizada"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id_transaccion": 1,
  "nombre_transaccion": "VENTA",
  "tipo_cuenta": "BANCARIA",
  "id_factura": 1,
  "detalle_transaccion": "Venta actualizada",
  "fecha": "2024-01-15T10:30:00",
  "entrada": 15000.0,
  "egreso": 0.0,
  "id_usuario": 1,
  "items": [...]
}
```

---

### 5. Eliminar Transacción

Elimina una transacción del sistema. Los items asociados se eliminan automáticamente.

**Endpoint:** `DELETE /api/transacciones/<id_transaccion>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_transaccion` (requerido): ID numérico de la transacción

**Ejemplo con curl:**
```bash
curl -X DELETE http://localhost:5000/api/transacciones/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Transacción eliminada exitosamente"
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Transacción no encontrada"
}
```

---

### 6. Obtener Transacciones por Usuario

Obtiene todas las transacciones asociadas a un usuario específico.

**Endpoint:** `GET /api/usuarios/<id_usuario>/transacciones`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_usuario` (requerido): ID numérico del usuario

**Query Parameters (opcionales):**
- `nombre_transaccion`: Filtrar por tipo de transacción
- `tipo_cuenta`: Filtrar por tipo de cuenta
- `include_items`: Incluir items asociados (true/false, por defecto: false)

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/usuarios/1/transacciones \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Filtrar solo ventas del usuario
curl -X GET "http://localhost:5000/api/usuarios/1/transacciones?nombre_transaccion=VENTA" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_transaccion": 1,
    "nombre_transaccion": "VENTA",
    "tipo_cuenta": "EFECTIVO",
    "id_factura": 1,
    "detalle_transaccion": "Venta",
    "fecha": "2024-01-15T10:30:00",
    "entrada": 15000.0,
    "egreso": 0.0,
    "id_usuario": 1
  }
]
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Usuario no encontrado"
}
```

---

## Endpoints de Items

### 1. Obtener Todos los Items

Obtiene una lista de todos los items registrados en el sistema. Permite filtrar por transacción y producto.

**Endpoint:** `GET /api/items`

**Autenticación:** Requerida (JWT)

**Query Parameters (opcionales):**
- `id_transaccion`: Filtrar por ID de transacción
- `id_producto`: Filtrar por ID de producto
- `include_producto_info`: Incluir información del producto (true/false, por defecto: true)

**Ejemplo con curl:**
```bash
# Obtener todos los items
curl -X GET http://localhost:5000/api/items \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Obtener items de una transacción específica
curl -X GET "http://localhost:5000/api/items?id_transaccion=1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Obtener items de un producto específico
curl -X GET "http://localhost:5000/api/items?id_producto=1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_item": 1,
    "cantidad": 2,
    "id_producto": 1,
    "id_transaccion": 1,
    "nombre_producto": "Chorizo",
    "precio_producto": 5000,
    "valor_total": 10000
  }
]
```

---

### 2. Crear Nuevo Item

Crea un nuevo item en el sistema.

**Endpoint:** `POST /api/items`

**Autenticación:** Requerida (JWT)

**Cuerpo de la solicitud (JSON):**
```json
{
  "id_producto": 1,
  "id_transaccion": 1,
  "cantidad": 2
}
```

**Parámetros:**
- `id_producto` (requerido): ID del producto
- `id_transaccion` (requerido): ID de la transacción
- `cantidad` (requerido): Cantidad del producto (número entero positivo)

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "id_producto": 1,
    "id_transaccion": 1,
    "cantidad": 2
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id_item": 1,
  "cantidad": 2,
  "id_producto": 1,
  "id_transaccion": 1,
  "nombre_producto": "Chorizo",
  "precio_producto": 5000,
  "valor_total": 10000
}
```

**Respuestas de error:**
- **400:** Datos inválidos
  ```json
  {
    "mensaje": "Se requiere id_producto"
  }
  ```
  o
  ```json
  {
    "mensaje": "La cantidad debe ser un número positivo"
  }
  ```

- **404:** Producto o transacción no existe
  ```json
  {
    "mensaje": "El producto especificado no existe"
  }
  ```

- **409:** Item ya existe
  ```json
  {
    "mensaje": "Ya existe un item con este producto en esta transacción"
  }
  ```

---

### 3. Obtener Item por ID

Obtiene la información de un item específico por su ID.

**Endpoint:** `GET /api/items/<id_item>`

**Autenticación:** Requerida (JWT)

**Query Parameters (opcionales):**
- `include_producto_info`: Incluir información del producto (true/false, por defecto: true)

**Parámetros de URL:**
- `id_item` (requerido): ID numérico del item

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "id_item": 1,
  "cantidad": 2,
  "id_producto": 1,
  "id_transaccion": 1,
  "nombre_producto": "Chorizo",
  "precio_producto": 5000,
  "valor_total": 10000
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Item no encontrado"
}
```

---

### 4. Actualizar Item

Actualiza la información de un item existente.

**Endpoint:** `PUT /api/items/<id_item>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_item` (requerido): ID numérico del item

**Cuerpo de la solicitud (JSON):**
```json
{
  "id_producto": 2,
  "cantidad": 3,
  "id_transaccion": 1
}
```

**Nota:** Todos los campos son opcionales. Solo se actualizarán los campos que se envíen en el JSON.

**Ejemplo con curl:**
```bash
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "cantidad": 3
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id_item": 1,
  "cantidad": 3,
  "id_producto": 1,
  "id_transaccion": 1,
  "nombre_producto": "Chorizo",
  "precio_producto": 5000,
  "valor_total": 15000
}
```

**Respuestas de error:**
- **400:** Datos inválidos
  ```json
  {
    "mensaje": "La cantidad debe ser un número positivo"
  }
  ```

- **404:** Item, producto o transacción no encontrado
  ```json
  {
    "mensaje": "Item no encontrado"
  }
  ```

- **409:** Conflicto (item duplicado)
  ```json
  {
    "mensaje": "Ya existe un item con este producto en esta transacción"
  }
  ```

---

### 5. Eliminar Item

Elimina un item del sistema.

**Endpoint:** `DELETE /api/items/<id_item>`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_item` (requerido): ID numérico del item

**Ejemplo con curl:**
```bash
curl -X DELETE http://localhost:5000/api/items/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Item eliminado exitosamente"
}
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Item no encontrado"
}
```

---

### 6. Obtener Items por Transacción

Obtiene todos los items asociados a una transacción específica.

**Endpoint:** `GET /api/transacciones/<id_transaccion>/items`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_transaccion` (requerido): ID numérico de la transacción

**Query Parameters (opcionales):**
- `include_producto_info`: Incluir información del producto (true/false, por defecto: true)

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/transacciones/1/items \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_item": 1,
    "cantidad": 2,
    "id_producto": 1,
    "id_transaccion": 1,
    "nombre_producto": "Chorizo",
    "precio_producto": 5000,
    "valor_total": 10000
  },
  {
    "id_item": 2,
    "cantidad": 1,
    "id_producto": 2,
    "id_transaccion": 1,
    "nombre_producto": "Hamburguesa",
    "precio_producto": 8000,
    "valor_total": 8000
  }
]
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Transacción no encontrada"
}
```

---

### 7. Obtener Items por Producto

Obtiene todos los items asociados a un producto específico.

**Endpoint:** `GET /api/productos/<id_producto>/items`

**Autenticación:** Requerida (JWT)

**Parámetros de URL:**
- `id_producto` (requerido): ID numérico del producto

**Query Parameters (opcionales):**
- `include_producto_info`: Incluir información del producto (true/false, por defecto: true)

**Ejemplo con curl:**
```bash
curl -X GET http://localhost:5000/api/productos/1/items \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
[
  {
    "id_item": 1,
    "cantidad": 2,
    "id_producto": 1,
    "id_transaccion": 1,
    "nombre_producto": "Chorizo",
    "precio_producto": 5000,
    "valor_total": 10000
  },
  {
    "id_item": 3,
    "cantidad": 1,
    "id_producto": 1,
    "id_transaccion": 2,
    "nombre_producto": "Chorizo",
    "precio_producto": 5000,
    "valor_total": 5000
  }
]
```

**Respuesta de error (404):**
```json
{
  "mensaje": "Producto no encontrado"
}
```

---

## Notas Importantes

1. **Seguridad de Contraseñas:** Las contraseñas se hashean automáticamente usando `werkzeug.security.generate_password_hash()` antes de almacenarse en la base de datos. Nunca se devuelven en las respuestas de la API.

2. **Roles Válidos:** Solo se aceptan los roles `"CAJERO"` y `"ADMINISTRADOR"`. Cualquier otro valor resultará en un error 400.

3. **Nombres de Usuario Únicos:** El campo `nombre_usuario` debe ser único. Intentar crear o actualizar un usuario con un nombre que ya existe resultará en un error 409.

4. **Nombres de Producto Únicos:** El campo `nombre_producto` debe ser único. Intentar crear o actualizar un producto con un nombre que ya existe resultará en un error 409.

5. **Precios de Productos:** Los precios deben ser números enteros positivos. Valores negativos o no numéricos resultarán en un error 400.

6. **Relación Usuario-Producto:** Cada producto debe estar asociado a un usuario existente. El `id_usuario` debe existir en la tabla de usuarios.

7. **Tipos de Transacción:** Los valores válidos para `nombre_transaccion` son: `BASE`, `VENTA`, `COSTO`, `GASTO`, `ENTRADA_INV`, `SALIDA_INV`.

8. **Tipos de Cuenta:** Los valores válidos para `tipo_cuenta` son: `EFECTIVO`, `BANCARIA`, `ENTRADA`.

9. **Items en Transacciones:** Los items se pueden incluir al crear o actualizar transacciones. Para transacciones de tipo `VENTA`, el campo `entrada` se recalcula automáticamente basado en los items proporcionados (cantidad × precio de cada producto).

10. **Eliminación en Cascada:** Al eliminar una transacción, todos los items asociados se eliminan automáticamente.

11. **Token JWT:** Los tokens JWT tienen una expiración. Si recibes un error 401, es posible que necesites obtener un nuevo token mediante el endpoint `/api/login`.

12. **Items Únicos por Transacción:** No puede haber dos items con el mismo producto en la misma transacción. Intentar crear un item duplicado resultará en un error 409.

13. **Relación Item-Producto-Transacción:** Cada item debe estar asociado a un producto y una transacción existentes. Tanto el `id_producto` como el `id_transaccion` deben existir en sus respectivas tablas.

14. **Cantidades de Items:** Las cantidades deben ser números enteros positivos. Valores negativos, cero o no numéricos resultarán en un error 400.

15. **Base de Datos:** La aplicación utiliza SQLite con la base de datos ubicada en `src/backend/database/chorizos.db`.

---

## Solución de Problemas

### Error: "Connection refused" o "Failed to connect to localhost port 5000"
**Causa:** El servidor Flask no está ejecutándose.

**Solución:**
1. Inicia el servidor Flask ejecutando:
   ```bash
   python src/backend/server_api.py
   ```
2. Verifica que el servidor esté corriendo revisando la salida en la terminal
3. Asegúrate de que el puerto 5000 no esté siendo usado por otra aplicación
4. Si el puerto está ocupado, puedes cambiar el puerto en `server_api.py` modificando la línea:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=True)
   ```
   Cambia `port=5000` por el puerto deseado (ej: `port=5001`)

### Error 401 Unauthorized
- Verifica que el token JWT sea válido y no haya expirado
- Asegúrate de incluir el header `Authorization: Bearer <token>`
- Obtén un nuevo token mediante `/api/login`

### Error 404 Not Found
- Verifica que el ID del usuario exista en la base de datos
- Asegúrate de usar el formato correcto de la URL

### Error 409 Conflict
- El nombre de usuario que intentas crear o actualizar ya existe
- Elige un nombre de usuario diferente

### Error 500 Internal Server Error
- Revisa los logs del servidor para más detalles
- Verifica que la base de datos esté accesible y configurada correctamente
