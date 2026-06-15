# Entorno Multicontenedor: Gestión de Alumnos (FastAPI + Nginx + MariaDB)

Este repositorio contiene la infraestructura dockerizada e independiente para el proyecto de gestión de alumnos de la facultad. La arquitectura está separada en **3 contenedores independientes**, garantizando el aislamiento del backend, la persistencia de los datos, la seguridad de acceso a través de un proxy inverso y un arranque secuencial controlado por diagnóstico de estado (_Healthcheck_).

---

## 🏗️ Arquitectura de Red y Puertos

Para entender cómo funciona el entorno, hay que diferenciar los puertos **internos** (cómo hablan los contenedores entre sí por la red privada de Docker) de los puertos **externos** (los que tú escribes en el navegador de tu máquina host Windows).

### Flujo de Comunicación y Aislamiento:

1. **Acceso Web (`Windows:9090` → `Nginx:80`):** Accedes desde tu navegador a `http://localhost:9090`. Nginx recibe esta petición en su puerto `80` interno.
2. **Proxy Inverso (`Nginx` → `FastAPI:8000`):** Nginx actúa como escudo. Desvía el tráfico internamente hacia el contenedor `app` al puerto `8000` utilizando el DNS interno de Docker (`http://app:8000`).
3. **Persistencia Directa (`FastAPI` → `MariaDB:3306`):** La aplicación Python procesa la petición y habla con el contenedor `db` en su puerto nativo `3306`.
4. **Acceso Externo BD (`Windows:3307` → `MariaDB:3306`):** El puerto de la base de datos se expone externamente en el `3307` para que puedas conectar un gestor de bases de datos (DBeaver, DataGrip, etc.) desde Windows sin interferir con otras instalaciones locales.

> ⚠️ **Nota de Seguridad:** El puerto `8000` de FastAPI **no está expuesto hacia Windows**. Está completamente blindado del exterior. La única forma de entrar a la aplicación es pasando obligatoriamente por el puerto `9090` de Nginx, el cual sirve de aterrizaje directo a tu plantilla `templates/home.html`.

---

## ⏱️ Secuencia de Arranque con Healthcheck

Para evitar que FastAPI intente inicializar las tablas antes de que la base de datos esté lista para aceptar conexiones (lo que provocaría un cierre inesperado del backend), se implementa un control de estado nativo:

- **MariaDB** cuenta con un script de diagnóstico interno (`healthcheck.sh`) que verifica el motor InnoDB y la conectividad cada 5 segundos.
- El contenedor **`app`** tiene una directiva `depends_on` condicionada a `service_healthy`. Esto retiene el inicio de Uvicorn en cola hasta que MariaDB responde con éxito, eliminando errores de conexión en el arranque.

---

## 🔐 Configuración de Variables de Entorno (`.env`)

El proyecto centraliza todas sus credenciales, nombres de bases de datos y mapeos de puertos físicos a través de un archivo `.env` en la raíz. Docker Compose inyecta dinámicamente estos valores en el orquestador:

```env
# Configuración de Base de Datos para MariaDB (Interno)
MARIADB_DATABASE=facultad
MARIADB_ROOT_PASSWORD=super_password_secreto_root

# Puertos Expuestos hacia el Host (Windows)
PUERTO_EXTERNO_NGINX=9090
PUERTO_EXTERNO_MARIADB=3307

# Parámetros de Conexión del Backend (FastAPI habla con MariaDB de forma interna)
DB_HOST=db
DB_PORT=3306
DB_NAME=facultad
DB_USER=app_user_blindado
DB_PASS=app_password_seguro
```

## 🔄 Concurrencia, Aislamiento y Control de Lecturas Sucias

Para evitar que múltiples usuarios pisen registros simultáneamente o generen estados inconsistentes en la base de datos (como "lecturas sucias" o inserciones duplicadas del mismo NIF en milisegundos de desfase), la arquitectura implementa dos capas de protección:

1. Nivel de Aislamiento Global (REPEATABLE READ): Forzado directamente en la creación del engine de SQLModel. Bloquea de raíz la lectura de datos no confirmados (dirty reads) por otras transacciones en curso.

2. Bloqueo Pesimista en Código (with_for_update()): En las rutas críticas (como el POST /alumnos/), antes de validar e insertar, el backend realiza un SELECT preventivo del NIF aplicando un candado de exclusión mutua. Si llega otra transacción simultánea para el mismo alumno, MariaDB la obliga a hacer cola de forma atómica hasta que la primera finalice su session.commit() o ejecute un session.rollback().

---

## ⏱️ Secuencia de Arranque con Healthcheck

Para evitar que FastAPI intente inicializar las tablas antes de que la base de datos esté lista para recibir tráfico, se implementa un control de estado nativo:

- MariaDB cuenta con un script de diagnóstico interno (healthcheck.sh) que verifica el motor InnoDB y la conectividad del socket cada 5 segundos.

- El contenedor app retiene el inicio de Uvicorn en cola mediante la directiva condition: service_healthy, eliminando por completo los errores de conexión de red durante el arranque inicial.

---

## 📁 Estructura del Proyecto

El proyecto debe mantener estrictamente esta disposición de archivos para asegurar que las rutas de importación de Python y los montajes de Docker no fallen:

```text
nginx_facultad/
├── BBDD/
│   ├── Conexion/
│   │   └── database_facultad.py   # Configuración de la URL de conexión
│   └── Modelo/
│       └── Alumno.py              # Modelos de SQLModel
├── html/
│   └── index.html                 # (Opcional) Respaldos estáticos
├── templates/                     # Vistas HTML (Jinja2) renderizadas por la App
│   ├── alumnos.html
│   ├── formulario_alumnos.html
│   ├── home.html
│   └── resultado_alumnos.html
├── .dockerignore                  # Exclusiones para aligerar la build de Docker
├── .gitignore                     # Exclusiones de Git (entornos virtuales, caches)
├── docker-compose.yml             # Orquestador de los 3 microservicios con Healthcheck
├── Dockerfile                     # Receta de construcción de la imagen de Python
├── main_facultad_3.py             # Punto de entrada de la App (FastAPI + Uvicorn)
├── nginx.conf                     # Configuración del Proxy Inverso de Nginx
└── requirements.txt               # Dependencias del proyecto (FastAPI, SQLModel, etc.)
```

## 🚀 Pasos para Replicar el Entorno desde Cero

Sigue estas instrucciones exactas en tu terminal de PowerShell para levantar todo el sistema:

1. Comprobación de Requisitos Previos
   Asegúrate de tener Docker Desktop abierto y que el icono de la ballena en la barra de tareas de Windows se encuentre en color verde (operativo).

2. Configurar la Conexión en el Código
   Antes de encender Docker, abre tu archivo BBDD/Conexion/database_facultad.py y asegúrate de que la URL de conexión apunte al nombre del servicio del contenedor (db) y no a localhost:

```Python
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

3. Comandos de Consola para el Ciclo de Vida

Montar e Inicializar el Entorno (Primera vez o cambios drásticos de dependencias):
Descarga las imágenes oficiales, limpia cachés obsoletas y compila el Dockerfile de Python desde cero aplicando los requerimientos locales.
Ejecuta el siguiente comando para descargar las imágenes base oficiales (Nginx y MariaDB), compilar el Dockerfile de Python con tus dependencias locales e iniciar los servicios en segundo plano (-d):

```bash
docker compose up -d --build
```

Levantar / Arrancar el Entorno Existente (En segundo plano):
Enciende los servicios respetando la cola secuencial del Healthcheck:

```Bash
docker compose up -d
```

Pausar Temporalmente los Contenedores:
Libera memoria RAM y recursos de CPU de tu Windows deteniendo los procesos sin destruir los contenedores:

```Bash
docker compose stop
```

Reiniciar los Servicios en Caliente:
Útil para aplicar de inmediato cambios en tus scripts de Python o modificaciones de diseño en la carpeta templates/:

```Bash
docker compose restart
```

Bajar e Interrumpir el Entorno por Completo:
Elimina los contenedores y las redes virtuales creadas. Los datos de los alumnos permanecen 100% seguros y persistentes en el volumen local:

```Bash
docker compose down
```

4. Verificar el Estado de la Infraestructura
   Para validar que los tres microservicios se han levantado estables y comprobar el Healthcheck, ejecuta:

```Bash
docker compose ps
```

Los tres contenedores (nginx-facultad, fastapi-facultad y mariadb-facultad) deben mostrar el estado Up o Running.

## 🔗 Enlaces de Acceso Local (Host Windows)

1. Aplicación Web (Landing Page): http://localhost:9090 (Muestra directamente el home.html renderizado por FastAPI).
2. Documentación Interactiva de la API: http://localhost:9090/docs (Swagger UI a través del túnel de Nginx).
3. Conexión a la Base de Datos:
   · localhost:3307
   · Usuario: facultad_user
   · Contraseña: facultad_pass
   · Base de datos: facultad

### 🛠️ Comandos de Mantenimiento Útiles

Si necesitas administrar el entorno sobre la marcha, usa estos comandos en la raíz del proyecto:

Ver los logs en tiempo real (útil para depurar errores de Python):

```bash
docker compose logs -f app
```

Apagar el entorno completamente (sin borrar los datos de los alumnos):

```bash
docker compose down
```

Reiniciar los servicios aplicando cambios de código drásticos:

```bash
docker compose up -d
```

### Acceso a la app : http://localhost:9090
