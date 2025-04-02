from conexion import *
from models.pacientes import mi_pacientes

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
    if session.get('login') == True:
        resultado = mi_pacientes.busca(id)
        return render_template("editarpaciente.html", paci = resultado[0])
    else:
        return redirect("/")

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
    if session.get('login') == True:
        mi_pacientes.borra(id)
        return redirect("/pacientes")
    else:
        return redirect("/")
