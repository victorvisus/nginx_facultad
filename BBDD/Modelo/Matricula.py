from sqlmodel import Field, SQLModel

"""
+--------------+---------+------+-----+---------+-------+
| Field        | Type    | Null | Key | Default | Extra |
+--------------+---------+------+-----+---------+-------+
| idAlumno     | int(5)  | NO   | MUL | NULL    |       |
| idProfesor   | int(5)  | NO   | MUL | NULL    |       |
| nota         | double  | NO   |     | NULL    |       |
+--------------+---------+------+-----+---------+-------+
"""


class MatriculaBase(SQLModel):
    idAlumno: int = Field(foreign_key="alumno.id")
    idProfesor: int = Field(foreign_key="profesor.id")
    nota: float = Field(gt=0, lt=10)  # La nota debe ser un valor entre 0 y 10


class Matricula(MatriculaBase, table=True):
    id: int = Field(primary_key=True)


class MatriculaCreate(MatriculaBase):
    pass
