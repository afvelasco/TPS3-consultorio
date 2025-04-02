from conexion import *
from models.usuarios import mi_usuarios

@principal.route("/login", methods=["POST"])
def login():
    id = request.form['id']
    contra = request.form['contra']
    resultado = mi_usuarios.login(id,contra)
    if len(resultado)>0:
        session["login"] = True
        session["id"] = id
        session["nombre"] = resultado[0][0]
        return redirect("/opciones")
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")

@principal.route("/usuarios")
def usuarios():
    usuarios = mi_usuarios.consulta()
    return render_template("usuarios.html", usua = usuarios)

