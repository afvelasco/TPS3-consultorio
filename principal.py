from conexion import *
from models.pacientes import mi_pacientes

@principal.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(principal.config['CARPETAU'],nombre)

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
        session["login"] = True
        session["id"] = id
        session["nombre"] = resultado[0][0]
        return redirect("/opciones")
    else:
        return render_template("index.html",msg = "Credenciales incorrectas")

@principal.route("/opciones")
def opciones():
    if session.get('login') == True:
        nom=session.get('nombre')
        return render_template("opciones.html", msg="Bienvenido(a) "+nom)
    else:
        return redirect("/")

@principal.route("/usuarios")
def usuarios():
    cursor = mi_DB.cursor()
    sql = "SELECT * FROM usuarios WHERE borrado=0"
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    return render_template("usuarios.html", usua = usuarios)

if __name__=="__main__":
    principal.run(host="0.0.0.0", port=9090, debug=True)