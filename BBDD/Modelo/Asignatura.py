from sqlmodel import Field, SQLModel

# import re
"""
+--------------+--------------------------------+------+-----+---------+-------+
| Field        | Type                           | Null | Key | Default | Extra |
+--------------+--------------------------------+------+-----+---------+-------+
| curso        | int(3)                         | NO   | MUL | NULL    |       |
| id           | int(5)                         | NO   | PRI | NULL    |       |
| nombre       | varchar(150)                   | YES  | UNI | NULL    |       |
| cuatrimestre | enum('1','2')                  | YES  |     | NULL    |       |
| creditos     | double                         | NO   |     | NULL    |       |
| caracter     | enum('obligatoria','optativa') | NO   |     | NULL    |       |
| coordinador  | char(5)                        | NO   | MUL | NULL    |       |
+--------------+--------------------------------+------+-----+---------+-------+
"""


class AsignaturaBase(SQLModel):
    nombre: str = Field(max_length=150)
    curso: int = Field(lt=4, gt=0)  # Debe ser 1 o 2
    cuatrimestre: str = Field(default=None)  # Puede ser '1' o '2'
    creditos: float = Field(gt=0)  # Debe ser un valor positivo
    caracter: str = Field(default=None)  # Puede ser 'obligatoria' u 'optativa'
    coordinador: int = Field(max_length=5)


class Asignatura(AsignaturaBase, table=True):
    id: int = Field(primary_key=True)
