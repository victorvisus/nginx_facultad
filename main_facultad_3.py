"""
Es crucial que importes tus modelos (Alumno, Asignatura, etc.) antes de ejecutar la creación de tablas; de lo contrario, SQLModel no sabrá qué tablas tiene que generar.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymysql import IntegrityError
from sqlmodel import select

# esta Aplicación se encarga de inicializar la base de datos al arrancar el servidor FastAPI
from BBDD.Conexion.database_facultad import (
    create_db_and_tables,
    inicializar_base_de_datos,
    session_dep,
)

# ¡IMPORTANTE! Importa aquí tus modelos para que SQLModel los registre
# from models import Alumno, Asignatura, Matricula
# Importar la clase `Alumno` desde el submódulo donde está definida
from BBDD.Modelo.Alumno import Alumno, AlumnoBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta al arrancar el servidor FastAPI antes de recibir peticiones
    print(
        "Reiniciando el servidor FastAPI... Verificando/Creando base de datos y tablas..."
    )
    inicializar_base_de_datos()
    create_db_and_tables()  # Crea las tablas basándose en los modelos importados
    yield


app = FastAPI(lifespan=lifespan)
# una vez que el servidor esté arrancado, la base de datos y
# las tablas estarán listas para usarse en los endpoints de la API.
# Por lo tanto, puedes definir tus endpoints aquí sin preocuparte por la
# inicialización de la base de datos, siendo inncesario para el uso del API Rest
# el reinicio del servidor tras la invocación de un endpoint.

# Configurar archivos estáticos (CSS, JS, etc.)
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")

templates = Jinja2Templates(directory="templates")

# una vez referida la carpeta de plantillas, se pueden crear endpoints que
# devuelvan HTML renderizado con Jinja2, en este caso para mostrar los alumnos matriculados en una asignatura concreta.


@app.get("/", response_model=list[Alumno])
async def name(session: session_dep, request: Request):
    alumnos = session.exec(select(Alumno)).all()
    # Convierte los objetos a un formato JSON serializable para pasarlos a la plantilla
    # print(f"Alumnos obtenidos de la base de datos: {alumnos}")
    alumnos_serializados = jsonable_encoder(alumnos)
    if alumnos is None:
        raise HTTPException(status_code=404, detail="No hay alumnos registrados")
    return templates.TemplateResponse(
        request, "alumnos.html", {"alumnos": alumnos_serializados}
    )


# End point para obtener un alumno por su ID
@app.get("/alumnos/{alumno_id}", response_model=Alumno)
async def obtener_alumno(alumno_id: int, request: Request, session: session_dep):
    alumno = session.get(Alumno, alumno_id)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "nombre": alumno.nombre,
            "fecha_nacimiento": alumno.fechaNacimiento,
            "NIF": alumno.NIF,
        },
    )


# Endpoint para consultar todos los alummos para mostrar en una tabla HTML:
@app.get("/alumnos/", response_model=list[Alumno])
async def obtener_alumnos(session: session_dep, request: Request):
    alumnos = session.exec(select(Alumno)).all()
    # Convierte los objetos a un formato JSON serializable para pasarlos a la plantilla
    # print(f"Alumnos obtenidos de la base de datos: {alumnos}")
    alumnos_serializados = jsonable_encoder(alumnos)
    if alumnos is None:
        raise HTTPException(status_code=404, detail="No hay alumnos registrados")
    return templates.TemplateResponse(
        request, "alumnos.html", {"alumnos": alumnos_serializados}
    )


# 2. Hacer otro para realizar una consulta de alumnos que el primer apellido comience por la letra que se introduzca en el formulario
# 3. Crear otro formulario que realice una busqueda de los alumnos mayores de una edad introducida en el formulario, para esto se puede calcular la edad a partir de la fecha de nacimiento del alumno y la fecha actual.
# 4. Hacer un endpoint para crear un alumno a través de un formulario HTML,

# Para todos los ejercicios se mostrarán los resultados en una tabla HTML, si debe mostrar un aviso si no se encuentran registros que cumplan con la consulta realizada a través del formulario.


# Endpoint para cargar el formulario de búsqueda de alumnos becados
@app.get("/formulario-becados/")
async def formulario_alumnos_becados(request: Request):
    return templates.TemplateResponse(request=request, name="formulario_alumnos.html")


# Endpoint para cargar el formulario de creación de alumnos
@app.get("/formulario-agregar-alumnos/")
async def formulario_agregar_alumnos(request: Request):
    return templates.TemplateResponse(
        request=request, name="formulario_crear_alumnos.html"
    )


# Endpoint alumnos becados
# 1. Hacer formulario que consulte los alumnos becados si o no, y los imprimar en una tabla HTML, mostrando un aviso si no hay alumnos becados registrados.
# 1. Quitamos el response_model porque devolvemos un HTML, no un JSON puro
@app.get("/alumnos/resultado/")
async def obtener_alumnos_becados(becado: int, session: session_dep, request: Request):
    try:
        # Validar que el parámetro becado sea 0 o 1
        if becado not in (0, 1):
            raise HTTPException(
                status_code=400, detail="El parámetro 'becado' debe ser 0 (No) o 1 (Sí)"
            )

        # FastAPI lee automáticamente ?becado=1 o ?becado=0 de la URL y lo convierte a int
        alumnos_becados = session.exec(
            select(Alumno).where(Alumno.beca == becado)
        ).all()
        # print(f"Alumnos obtenidos: {alumnos_becados}")

        # Serializamos los objetos para que Jinja2 los entienda
        alumnos_becados_serializados = jsonable_encoder(alumnos_becados)

        # Permitimos que las listas vacías pasen a la plantilla y ejecuten el bloque {% else %} del HTML
        # Especificamos qué columnas mostrar en la tabla
        columnas = [
            {"campo": "nombre", "label": "Nombre", "tipo": "texto"},
            {"campo": "apellido1", "label": "Primer Apellido", "tipo": "texto"},
            {"campo": "email", "label": "Email", "tipo": "texto"},
            {"campo": "beca", "label": "Beca", "tipo": "booleano"},
        ]

        return templates.TemplateResponse(
            request=request,
            name="resultado_alumnos.html",
            context={
                "alumnos": alumnos_becados_serializados,
                "columnas": columnas,
                "name": "Alumnos Becados",
            },
        )

    except HTTPException as e:
        # Re-lanzar las excepciones HTTP (como la validación de parámetros)
        print(f"Error de validación HTTP: {e.detail}")
        raise e

    except Exception as e:
        # Capturar cualquier otro error (conexión BD, serialización, etc.)
        print(f"Error inesperado al obtener alumnos becados: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la solicitud. Por favor, intente más tarde.",
        )


@app.post("/alumnos/", response_model=Alumno)
def crear_alumno(alumnoBase: AlumnoBase, session: session_dep):

    alumnoInvalido = False
    try:
        print("***************************")
        print(f"****************************NIF: {alumnoBase.NIF}")
        print(alumnoBase.email)

        # ---------------------------------------------------------------------
        # CONCURRENCIA & AISLAMIENTO: Bloqueo preventivo
        # Hacemos un SELECT del NIF pero metiendo un candado Pesimista (.with_for_update())
        # Si otra transacción está intentando registrar este mismo NIF a la vez,
        # MariaDB la congelará en este punto exacto hasta que hagamos commit o rollback.
        # ---------------------------------------------------------------------
        stmt_concurrencia = (
            select(Alumno).where(Alumno.NIF == alumnoBase.NIF).with_for_update()
        )
        alumno_existente = session.exec(stmt_concurrencia).first()

        if alumno_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El alumno con este NIF ya se encuentra registrado o en proceso de registro.",
            )

        # Validaciones de formato tuyas
        if alumnoBase.validar_NIF(alumnoBase.NIF) and alumnoBase.validar_correo_regex(
            alumnoBase.email
        ):
            print(
                f"Alumno válido: {alumnoBase.NIF} y {alumnoBase.email} han pasado las validaciones."
            )

            # Convierte el AlumnoBase a Alumno para la base de datos
            db_alumno = Alumno.model_validate(alumnoBase)
            print(f"id de Alumno: {db_alumno.id}")

            session.add(db_alumno)
            session.commit()  # <--- Aquí se guardan los datos de forma definitiva y SE LIBERA el candado
            session.refresh(db_alumno)
            return db_alumno
        else:
            alumnoInvalido = True
            print(
                f"-----------------Alumno no válido: {alumnoBase.NIF} o {alumnoBase.email} han fallado las validaciones."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alumno no válido: NIF o correo electrónico no cumplen con el formato requerido.",
            )

    except IntegrityError as ie:
        # Por si se salta el select y choca contra una "Unique Constraint" de MariaDB
        print(f"+++++++++++++++++++++Error de integridad concurrente: {ie}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de duplicidad: El NIF o Email ya existen en el sistema.",
        )
    except HTTPException as he:
        # Si es un error controlado de FastAPI, hacemos rollback y lo relanzamos tal cual
        session.rollback()
        raise he
    except Exception as e:
        # Errores críticos genéricos
        print(f"+++++++++++++++++++++Error crítico inesperado al crear alumno: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el servidor al procesar el alta.",
        )
    finally:
        if alumnoInvalido:
            print(
                f"Alumno no válido: {alumnoBase.NIF} o {alumnoBase.email} han fallado las validaciones. No se ha guardado."
            )
        else:
            print(f"****Proceso finalizado para el alumno: {alumnoBase.NIF}")

        # Cerramos la sesión de forma segura para liberar conexiones en el pool
        session.close()
