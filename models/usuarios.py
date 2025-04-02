from conexion import *

class Usuarios:
    def login(self, id, contra):
        cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
        sql = f"SELECT nombre FROM usuarios WHERE id_usuario='{id}' and contrasena='{cifrada}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    def consulta(self):
        sql = "SELECT * FROM usuarios WHERE borrado=0"
        mi_cursor.execute(sql)
        usuarios = mi_cursor.fetchall()
        return usuarios


mi_usuarios = Usuarios()