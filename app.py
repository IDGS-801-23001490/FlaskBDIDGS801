from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect  
from flask import g
from flask_migrate import Migrate
from config import DevelopmentConfig 
from models import db, Alumnos       
from forms import UserForm2
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
    create_form=forms.UserForm2(request.form)
    #ORM select * from alumnos
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form,alumnos=alumno)

@app.route("/Alumnos", methods=["GET", "POST"])
def registrar_alumnos():
    form = UserForm2(request.form)
    if request.method == "POST" and form.validate():
        nuevo_alumno = Alumnos(
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            email=form.correo.data
        )
        
        db.session.add(nuevo_alumno)
        db.session.commit()
        
        return redirect(url_for('index')) 
        
    return render_template("Alumnos.html", form=form)

@app.route("/detalles", methods=["GET", "POST"])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        id=request.args.get('id')
        nombre=alum1.nombre
        apaterno=alum1.apaterno
        email=alum1.email

    return render_template("detalles.html", id=id, nombre=nombre,apaterno=apaterno,email=email)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.correo.data = alum1.email 

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        alum1.nombre = create_form.nombre.data
        alum1.apaterno = create_form.apaterno.data
        alum1.email = create_form.correo.data 
        
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('modificar.html', form=create_form)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum:
            create_form.id.data = alum.id
            create_form.nombre.data = alum.nombre
            create_form.apaterno.data = alum.apaterno
            create_form.correo.data = alum.email
            return render_template("eliminar.html", form=create_form)
        else:
            return redirect(url_for('index'))  

    if request.method == 'POST':
        id = create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum: 
            db.session.delete(alum)
            db.session.commit()
        
        return redirect(url_for('index'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)