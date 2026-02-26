from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db, Alumnos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
@app.route("/index")
def index():
    alumnos = Alumnos.query.all()
    return render_template("index.html", alumnos=alumnos)

@app.route("/registrar", methods=["GET", "POST"])   # ← te recomiendo cambiar el nombre de la ruta
@app.route("/Alumnos", methods=["GET", "POST"])
def registrar_alumnos():
    form = forms.UserForm2(request.form)
    
    if request.method == "POST" and form.validate():
        nuevo_alumno = Alumnos(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            telefono=form.telefono.data
        )
        db.session.add(nuevo_alumno)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template("Alumnos.html", form=form)

@app.route("/detalles")
def detalles():
    id_alum = request.args.get('id')
    alumno = Alumnos.query.get_or_404(id_alum)
    
    return render_template("detalles.html", alumno=alumno)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    form = forms.UserForm2(request.form)
    id_alum = request.args.get('id') or form.id.data
    
    alumno = Alumnos.query.get_or_404(id_alum)
    
    if request.method == 'GET':
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apellidos.data = alumno.apellidos
        form.email.data = alumno.email
        form.telefono.data = alumno.telefono
    
    if request.method == 'POST' and form.validate():
        alumno.nombre = form.nombre.data
        alumno.apellidos = form.apellidos.data
        alumno.email = form.email.data
        alumno.telefono = form.telefono.data
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('modificar.html', form=form, alumno=alumno)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id_alum = request.args.get('id')
        alumno = Alumnos.query.get_or_404(id_alum)
        
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apellidos.data = alumno.apellidos
        form.email.data = alumno.email
        form.telefono.data = alumno.telefono
        
        return render_template("eliminar.html", form=form, alumno=alumno)

    if request.method == 'POST' and form.validate():
        alumno = Alumnos.query.get(form.id.data)
        if alumno:
            db.session.delete(alumno)
            db.session.commit()
        
        return redirect(url_for('index'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)