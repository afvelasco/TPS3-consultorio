from conexion import *
from routes.pacientes import *
from routes.usuarios import *

@principal.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(principal.config['CARPETAU'],nombre)

@principal.route("/")
def index():
    return render_template("index.html")

@principal.route("/opciones")
def opciones():
    if session.get('login') == True:
        nom=session.get('nombre')
        return render_template("opciones.html", msg="Bienvenido(a) "+nom)
    else:
        return redirect("/")

if __name__=="__main__":
    principal.run(host="0.0.0.0", port=9090, debug=True)