from flask import Flask, redirect, render_template, request
import mysql.connector
import hashlib

principal = Flask(__name__)
mi_DB = mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="proyecto")


@principal.route("/")
def index():
    return render_template("index.html")

@principal.route("/login", methods=["POST"])
def login():
    id = request.form['id']
    contra = request.form['contra']
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    cursor = mi_DB.cursor()
    sql = f"SELECT nombre FROM usuarios WHERE id_usuario='{id}' and contrasena='{cifrada}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado)>0:
        return render_template("opciones.html",msg = "Bienvenido "+resultado[0][0])
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")

@principal.route("/pacientes")
def pacientes():
    cursor = mi_DB.cursor()
    sql = "SELECT * FROM pacientes"
    cursor.execute(sql)
    pacientes = cursor.fetchall()
    return render_template("pacientes.html", paci = pacientes)

@principal.route("/nuevopaciente")
def nuevopaciente():
    return render_template("nuevopaciente.html")

@principal.route("/guardapaciente", methods=["POST"])
def guardapaciente():
    id = request.form['id']
    nom = request.form['nom']
    cel = request.form['cel']
    cursor = mi_DB.cursor()
    sql = f"SELECT nombre FROM pacientes WHERE id_paciente='{id}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        sql = f"INSERT INTO pacientes (id_paciente,nombre,celular) VALUES ('{id}','{nom}','{cel}')"
        cursor.execute(sql)
        mi_DB.commit()
        return redirect("/pacientes")
    else:
        return render_template("nuevopaciente.html", msg="Id ya existe")

@principal.route("/editapaciente/<id>")
def editapaciente(id):
    cursor = mi_DB.cursor()
    sql = f"SELECT * FROM pacientes WHERE id_paciente='{id}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return render_template("editarpaciente.html", paci = resultado[0])

if __name__=="__main__":
    principal.run(host="0.0.0.0", port=9090, debug=True)