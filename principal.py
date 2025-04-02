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

@principal.route("/pacientes")
def pacientes():
    if session.get('login') == True:
        pacientes = mi_pacientes.consulta()
        return render_template("pacientes.html", paci = pacientes)
    else:
        return redirect("/")
    
@principal.route("/nuevopaciente")
def nuevopaciente():
    if session.get('login') == True:
        return render_template("nuevopaciente.html")
    else:
        return redirect("/")

@principal.route("/guardapaciente", methods=["POST"])
def guardapaciente():
    id = request.form['id']
    nom = request.form['nom']
    cel = request.form['cel']
    foto = request.files['foto']
    resultado = mi_pacientes.busca(id)
    if len(resultado) == 0:
        ahora = datetime.now()
        tiempo = ahora.strftime("%Y%m%d%H%M%S")
        nombre,extension = os.path.splitext(foto.filename)
        nuevonombre = "P" + tiempo + extension
        foto.save("uploads/"+nuevonombre)
        mi_pacientes.agrega([id,nom,cel,nuevonombre])
        return redirect("/pacientes")
    else:
        return render_template("nuevopaciente.html", msg="Id ya existe")

@principal.route("/editapaciente/<id>")
def editapaciente(id):
    resultado = mi_pacientes.busca(id)
    return render_template("editarpaciente.html", paci = resultado[0])

@principal.route("/confirmapaciente", methods=['POST'])
def confirmapaciente():
    id = request.form['id']
    nom = request.form['nom']
    cel = request.form['cel']
    foto = request.files['foto']
    nombre = mi_pacientes.busca(id)[0][3]
    if foto.filename!="":
        os.remove(os.path.join(principal.config['CARPETAU'],nombre))
        ahora = datetime.now()
        tiempo = ahora.strftime("%Y%m%d%H%M%S")
        nombre,extension = os.path.splitext(foto.filename)
        nuevonombre = "P" + tiempo + extension
        foto.save("uploads/"+nuevonombre)
    else:
        nuevonombre = nombre
    mi_pacientes.actualiza([id,nom,cel,nuevonombre])
    return redirect("/pacientes")

@principal.route("/borrapaciente/<id>")
def borrapaciente(id):
    mi_pacientes.borra(id)
    return redirect("/pacientes")

@principal.route("/usuarios")
def usuarios():
    cursor = mi_DB.cursor()
    sql = "SELECT * FROM usuarios WHERE borrado=0"
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    return render_template("usuarios.html", usua = usuarios)

if __name__=="__main__":
    principal.run(host="0.0.0.0", port=9090, debug=True)