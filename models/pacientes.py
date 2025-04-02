from conexion import *

class Pacientes:
    def consulta(self):
        sql = "SELECT * FROM pacientes WHERE borrado=0"
        mi_cursor.execute(sql)
        pacientes = mi_cursor.fetchall()
        return pacientes

    def busca(self, id):
        sql = f"SELECT * FROM pacientes WHERE id_paciente='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agrega(self, p):
        sql = f"INSERT INTO pacientes (id_paciente,nombre,celular,foto) VALUES ('{p[0]}','{p[1]}','{p[2]}','{p[3]}')"
        mi_cursor.execute(sql)
        mi_DB.commit()

    def actualiza(self, p):
        sql = f"UPDATE pacientes SET nombre='{p[1]}', celular='{p[2]}', foto='{p[3]}' WHERE id_paciente='{p[0]}'"
        mi_cursor.execute(sql)
        mi_DB.commit()

    def borra(id):
        sql = f"UPDATE pacientes SET borrado=1 WHERE id_paciente='{id}'"
        mi_cursor.execute(sql)
        mi_DB.commit()

mi_pacientes = Pacientes()