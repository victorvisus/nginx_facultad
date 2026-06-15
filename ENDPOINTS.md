# Documentación de Endpoints - Gestión de Alumnos

Este documento detalla todos los endpoints disponibles en la aplicación FastAPI para la gestión de alumnos.

---

## 📋 Tabla de Contenidos

1. [Endpoints GET](#endpoints-get)
2. [Endpoints POST](#endpoints-post)
3. [Modelos de Datos](#modelos-de-datos)
4. [Códigos de Estado HTTP](#códigos-de-estado-http)
5. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Endpoints GET

### 1. Listar todos los alumnos (Inicio)

**Endpoint:** `GET /`

**Descripción:** Obtiene la lista de todos los alumnos registrados en el sistema y los muestra en una tabla HTML.

**Parámetros:**

- No requiere parámetros

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `alumnos.html`)
- **Código:** 200 OK

**Campos devueltos:**

```json
[
  {
    "id": 1,
    "nombre": "Juan",
    "apellido1": "García",
    "apellido2": "López",
    "NIF": "12345678A",
    "email": "juan@ejemplo.com",
    "fechaNacimiento": "2000-05-15",
    "direccion": "Calle Principal 123",
    "codigoPostal": "28001",
    "municipio": "Madrid",
    "provincia": "Madrid",
    "beca": false
  }
]
```

**Ejemplo de uso:**

```bash
curl http://localhost:9090/
```

---

### 2. Obtener alumno por ID

**Endpoint:** `GET /alumnos/{alumno_id}`

**Descripción:** Obtiene los detalles de un alumno específico por su ID y los muestra en la página `home.html`.

**Parámetros:**

- `alumno_id` (path parameter, requerido): ID único del alumno (entero)

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `home.html`)
- **Código:** 200 OK
- **Error:** 404 Not Found si el alumno no existe

**Ejemplo de uso:**

```bash
curl http://localhost:9090/alumnos/1
```

---

### 3. Listar todos los alumnos (Ruta alternativa)

**Endpoint:** `GET /alumnos/`

**Descripción:** Obtiene la lista de todos los alumnos registrados. Ruta alternativa idéntica a `GET /`.

**Parámetros:**

- No requiere parámetros

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `alumnos.html`)
- **Código:** 200 OK

**Ejemplo de uso:**

```bash
curl http://localhost:9090/alumnos/
```

**Nota:** Este endpoint tiene la misma funcionalidad que `GET /`, pero con una ruta más específica.

---

### 4. Cargar formulario de búsqueda de alumnos becados

**Endpoint:** `GET /formulario-becados/`

**Descripción:** Carga el formulario HTML para buscar alumnos por estado de beca.

**Parámetros:**

- No requiere parámetros

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `formulario_alumnos.html`)
- **Código:** 200 OK

**Ejemplo de uso:**

```bash
curl http://localhost:9090/formulario-becados/
```

---

### 5. Resultado alumnos por estado de beca

**Endpoint:** `GET /alumnos/resultado/`

**Descripción:** Busca alumnos según su estado de beca (becados o no becados) y muestra los resultados en una tabla HTML.

**Parámetros:**

- `becado` (query parameter, requerido):
  - `0` = No becados
  - `1` = Becados
  - Otros valores generarán un error 400

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `resultado_alumnos.html`)
- **Código:** 200 OK
- **Error:** 400 Bad Request si el parámetro no es válido
- **Error:** 500 Internal Server Error si hay un problema en la base de datos

**Ejemplo de uso:**

```bash
curl "http://localhost:9090/alumnos/resultado/?becado=1"
curl "http://localhost:9090/alumnos/resultado/?becado=0"
```

---

### 6. Cargar formulario para agregar alumnos

**Endpoint:** `GET /formulario-agregar-alumnos/`

**Descripción:** Carga el formulario HTML para crear un nuevo alumno en el sistema.

**Parámetros:**

- No requiere parámetros

**Respuesta:**

- **Tipo:** HTML (Jinja2 Template: `formulario_crear_alumnos.html`)
- **Código:** 200 OK

**Ejemplo de uso:**

```bash
curl http://localhost:9090/formulario-agregar-alumnos/
```

---

## Endpoints POST

### 7. Crear nuevo alumno

**Endpoint:** `POST /alumnos/`

**Descripción:** Crea un nuevo alumno en el sistema. Valida el formato del NIF y correo electrónico antes de insertar los datos. Implementa bloqueos pesimistas para evitar inserciones duplicadas en caso de concurrencia.

**Headers requeridos:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "nombre": "Juan",
  "apellido1": "García",
  "apellido2": "López",
  "NIF": "12345678A",
  "email": "juan@ejemplo.com",
  "fechaNacimiento": "2000-05-15",
  "direccion": "Calle Principal 123",
  "codigoPostal": "28001",
  "municipio": "Madrid",
  "provincia": "Madrid",
  "beca": false
}
```

**Campos requeridos:**

- `nombre`: string (máx. 255 caracteres)
- `apellido1`: string (máx. 255 caracteres)
- `NIF`: string (máx. 9 caracteres, formato: 8 dígitos + 1 letra, único)
- `email`: string (máx. 255 caracteres, único, formato válido de email)
- `fechaNacimiento`: date (formato YYYY-MM-DD)
- `direccion`: string (máx. 255 caracteres)
- `codigoPostal`: string (máx. 10 caracteres)
- `municipio`: string (máx. 255 caracteres)
- `provincia`: string (máx. 255 caracteres)

**Campos opcionales:**

- `apellido2`: string (máx. 255 caracteres, nullable)
- `beca`: boolean (por defecto: false)

**Respuesta exitosa:**

- **Tipo:** JSON
- **Código:** 200 OK
- **Formato:**

```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido1": "García",
  "apellido2": "López",
  "NIF": "12345678A",
  "email": "juan@ejemplo.com",
  "fechaNacimiento": "2000-05-15",
  "direccion": "Calle Principal 123",
  "codigoPostal": "28001",
  "municipio": "Madrid",
  "provincia": "Madrid",
  "beca": false
}
```

**Posibles errores:**

| Código                    | Descripción                   | Causa                                                       |
| ------------------------- | ----------------------------- | ----------------------------------------------------------- |
| 400 Bad Request           | NIF o Email ya existen        | Se intenta crear un alumno con NIF o email duplicados       |
| 400 Bad Request           | NIF inválido                  | El formato del NIF no es correcto o la letra no coincide    |
| 400 Bad Request           | Email inválido                | El formato del email no es válido                           |
| 400 Bad Request           | Alumno en proceso de registro | El NIF está siendo procesado en otra transacción simultánea |
| 500 Internal Server Error | Error interno                 | Problema de conexión con la base de datos                   |

**Respuesta de error (ejemplo):**

```json
{
  "detail": "Error de duplicidad: El NIF o Email ya existen en el sistema."
}
```

**Ejemplo de uso con curl:**

```bash
curl -X POST http://localhost:9090/alumnos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido1": "García",
    "apellido2": "López",
    "NIF": "12345678A",
    "email": "juan@ejemplo.com",
    "fechaNacimiento": "2000-05-15",
    "direccion": "Calle Principal 123",
    "codigoPostal": "28001",
    "municipio": "Madrid",
    "provincia": "Madrid",
    "beca": false
  }'
```

**Ejemplo de uso con JavaScript/Fetch:**

```javascript
const alumnoData = {
  nombre: "Juan",
  apellido1: "García",
  apellido2: "López",
  NIF: "12345678A",
  email: "juan@ejemplo.com",
  fechaNacimiento: "2000-05-15",
  direccion: "Calle Principal 123",
  codigoPostal": "28001",
  municipio: "Madrid",
  provincia: "Madrid",
  beca: false
};

fetch('/alumnos/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(alumnoData),
})
.then(response => response.json())
.then(data => console.log('Éxito:', data))
.catch(error => console.error('Error:', error));
```

**Medidas de seguridad:**

- Validación de NIF mediante algoritmo estándar español
- Validación de formato de email con regex
- Bloqueo pesimista para evitar condiciones de carrera (race conditions)
- Aislamiento de transacciones REPEATABLE READ
- Control de integridad a nivel de base de datos

---

## Modelos de Datos

### Alumno (Modelo completo con ID)

```json
{
  "id": 1,
  "nombre": "string (1-255 caracteres)",
  "apellido1": "string (1-255 caracteres, requerido)",
  "apellido2": "string (1-255 caracteres, nullable)",
  "NIF": "string (9 caracteres, formato: 8 dígitos + letra, único)",
  "email": "string (1-255 caracteres, único, válido)",
  "fechaNacimiento": "date (YYYY-MM-DD)",
  "direccion": "string (1-255 caracteres)",
  "codigoPostal": "string (1-10 caracteres)",
  "municipio": "string (1-255 caracteres)",
  "provincia": "string (1-255 caracteres)",
  "beca": "boolean (default: false)"
}
```

### AlumnoBase (Modelo para crear/actualizar - sin ID)

```json
{
  "nombre": "string (1-255 caracteres)",
  "apellido1": "string (1-255 caracteres, requerido)",
  "apellido2": "string (1-255 caracteres, nullable)",
  "NIF": "string (9 caracteres, formato: 8 dígitos + letra, único)",
  "email": "string (1-255 caracteres, único, válido)",
  "fechaNacimiento": "date (YYYY-MM-DD)",
  "direccion": "string (1-255 caracteres)",
  "codigoPostal": "string (1-10 caracteres)",
  "municipio": "string (1-255 caracteres)",
  "provincia": "string (1-255 caracteres)",
  "beca": "boolean (default: false)"
}
```

---

## Códigos de Estado HTTP

| Código                    | Significado           | Cuando se usa                                     |
| ------------------------- | --------------------- | ------------------------------------------------- |
| 200 OK                    | Solicitud exitosa     | En todas las operaciones GET y POST exitosas      |
| 400 Bad Request           | Solicitud inválida    | Validación fallida, parámetros inválidos          |
| 404 Not Found             | Recurso no encontrado | Alumno no existe, tabla vacía                     |
| 500 Internal Server Error | Error del servidor    | Problemas de conexión con BD, errores inesperados |

---

## Ejemplos de Uso

### Ejemplo 1: Ver todos los alumnos

```bash
curl http://localhost:9090/alumnos/
```

### Ejemplo 2: Crear un nuevo alumno

```bash
curl -X POST http://localhost:9090/alumnos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María",
    "apellido1": "Martínez",
    "apellido2": "Sánchez",
    "NIF": "87654321Z",
    "email": "maria@ejemplo.com",
    "fechaNacimiento": "1999-10-20",
    "direccion": "Avenida Secundaria 456",
    "codigoPostal": "28002",
    "municipio": "Madrid",
    "provincia": "Madrid",
    "beca": true
  }'
```

### Ejemplo 3: Buscar alumnos becados

```bash
curl "http://localhost:9090/alumnos/resultado/?becado=1"
```

### Ejemplo 4: Obtener alumno específico

```bash
curl http://localhost:9090/alumnos/1
```

### Ejemplo 5: Acceder al formulario de creación

```bash
# Abre en el navegador:
http://localhost:9090/formulario-agregar-alumnos/
```

---

## Notas Importantes

- **Persistencia:** Todos los datos se almacenan en MariaDB
- **Concurrencia:** El endpoint POST implementa bloqueos pesimistas para evitar duplicados
- **Validación:** Los NIFs y emails se validan antes de insertarlos
- **Aislamiento:** Nivel de aislamiento REPEATABLE READ para evitar lecturas sucias
- **Proxy Inverso:** Nginx actúa como proxy inverso, exponiendo solo el puerto 9090

---

## Tabla de Rutas Resumida

| Método | Ruta                           | Descripción                            | Response |
| ------ | ------------------------------ | -------------------------------------- | -------- |
| GET    | `/`                            | Listar todos los alumnos               | HTML     |
| GET    | `/alumnos/`                    | Listar todos los alumnos (alternativo) | HTML     |
| GET    | `/alumnos/{alumno_id}`         | Obtener alumno por ID                  | HTML     |
| GET    | `/formulario-becados/`         | Cargar formulario de búsqueda becas    | HTML     |
| GET    | `/alumnos/resultado/?becado=X` | Buscar alumnos por beca                | HTML     |
| GET    | `/formulario-agregar-alumnos/` | Cargar formulario crear alumno         | HTML     |
| POST   | `/alumnos/`                    | Crear nuevo alumno                     | JSON     |

---

**Última actualización:** 2026-06-15
