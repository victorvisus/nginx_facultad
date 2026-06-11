from sqlmodel import Field, SQLModel

"""
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------+-----+---------+-------+
| Field        | Type                                                                                                                                                                                                                                                                                                                  | Null | Key | Default | Extra |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------+-----+---------+-------+
| id           | int(5)                                                                                                                                                                                                                                                                                                                | NO   | PRI | NULL    |       |
| NIF          | char(9)                                                                                                                                                                                                                                                                                                               | YES  | UNI | NULL    |       |
| nombre       | varchar(50)                                                                                                                                                                                                                                                                                                           | NO   |     | NULL    |       |
| apellido1    | varchar(50)                                                                                                                                                                                                                                                                                                           | NO   |     | NULL    |       |
| apellido2    | varchar(50)                                                                                                                                                                                                                                                                                                           | YES  |     | NULL    |       |
| email        | varchar(50)                                                                                                                                                                                                                                                                                                           | YES  | UNI | NULL    |       |
| direccion    | varchar(100)                                                                                                                                                                                                                                                                                                          | NO   |     | NULL    |       |
| codigoPostal | int(5)                                                                                                                                                                                                                                                                                                                | NO   |     | NULL    |       |
| municipio    | tinytext                                                                                                                                                                                                                                                                                                              | NO   |     | NULL    |       |
| provincia    | tinytext                                                                                                                                                                                                                                                                                                              | NO   |     | NULL    |       |
| categoria    | enum('Catedráticos de Universidad','Titulares Universidad','Catedráticos de Escuela Universitaria','Titulares de Escuela Universitaria','Eméritos','Contratados Doctores','Contratados Doctores Interinos','Asociados','Asociado Interino','Ayudantes Doctores','Otros Investigadores Doctores','PDI predoctoral')    | YES  |     | NULL    |       |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------+-----+---------+-------+
"""


class ProfesorBase(SQLModel):
    NIF: str = Field(
        max_length=9, unique=True, nullable=False
    )  # 8 dígitos + letra, único y no nulo
    # nombre: str = Field(max_length=50)
    # apellido1: str = Field(max_length=50, nullable=False)
    # apellido2: str = Field(max_length=50, default=None)
    # email: str = Field(max_length=50, default=None, index=True)  # Correo electrónico único y no nulo
    # direccion: str = Field(max_length=100)
    # codigoPostal: int = Field(gt=0)
    # municipio: str = Field(max_length=255)
    # provincia: str = Field(max_length=255)
    # categoria: str = Field(default=None)


class Profesor(ProfesorBase, table=True):
    id: int = Field(primary_key=True)


# no necesito esta clase, pero es una buena práctica tener un modelo específico para la creación de recursos,
# ya que el id se genera automáticamente al crear un profesor y no lo incluyo en ProfesorBase para no requerirlo en la creación.
class ProfesorCreate(ProfesorBase):
    pass
