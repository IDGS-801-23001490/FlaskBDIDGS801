from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect  
from flask import g
from config import DevelopmentConfig 
from models import db, Alumnos       
from forms import UserForm2


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app) 

db.init_app(app)

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/Alumnos", methods=["GET", "POST"])
def Alumnos():
    form = UserForm2(request.form)
    if request.method == "POST" and form.validate():
        nuevo_alumno = Alumnos(
            id=form.id.data,
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            email=form.correo.data
        )
        
        db.session.add(nuevo_alumno)
        db.session.commit()
        
        flash("¡Alumno registrado con éxito!")
        return redirect(url_for('Alumnos'))
        
    return render_template("Alumnos.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)

