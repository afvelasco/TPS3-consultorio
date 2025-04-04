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
    
    def busca(self, id):
        sql = f"SELECT * FROM usuarios WHERE id_usuario='{id}' and borrado=0"
        mi_cursor.execute(sql)
        usuario = mi_cursor.fetchall()[0]
        return usuario

    def enviacorreo(self, id):
        usuario = mi_usuarios.busca(id)
        nombre = usuario[1]
        destinatario = usuario[3]
        remitente = 'tps3-cab@outlook.com'
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Prueba desde Python"
        cuerpo = f"Hola {nombre}, este es un mensaje de prueba enviado desde E-Consultorio (Python)"
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        nombre_usuario = 'tps3-cab@outlook.com'
        password = 'C4b-S3n4-Tp5e'
        server = smtplib.SMTP('smtp.office365.com:587')
        server.starttls()
        server.login(nombre_usuario, password)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
        return True

mi_usuarios = Usuarios()