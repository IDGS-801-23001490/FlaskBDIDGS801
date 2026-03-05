from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos
from forms import UserForm2
from . import alumnos

@alumnos.route("/index")
def index():
    alumnos_list = Alumnos.query.all()
    return render_template("alumnos/index.html", alumnos=alumnos_list)

@alumnos.route("/registrar", methods=["GET", "POST"])
def registrar_alumnos():
    form = UserForm2(request.form)
    
    if request.method == "POST" and form.validate():
        nuevo_alumno = Alumnos(
            nombre=form.nombre.data,
            apaterno=form.apaterno.data, 
            email=form.email.data
        )
        try:
            db.session.add(nuevo_alumno)
            db.session.commit()
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar: {e}")
            
    return render_template("alumnos/Alumnos.html", form=form)

@alumnos.route("/detalles")
def detalles():
    id_alum = request.args.get('id')
    if not id_alum:
        return redirect(url_for('alumnos.index'))
        
    alumno = Alumnos.query.get_or_404(id_alum)
    return render_template("alumnos/detalles.html", alumno=alumno)

@alumnos.route("/modificar", methods=["GET", "POST"])
def modificar():
    form = UserForm2(request.form)
    id_alum = request.args.get('id') or form.id.data
    
    if not id_alum:
        return redirect(url_for('alumnos.index'))

    alumno = Alumnos.query.get_or_404(id_alum)
    
    if request.method == 'GET':
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apaterno.data = alumno.apaterno 
        form.email.data = alumno.email
    
    if request.method == 'POST' and form.validate():
        alumno.nombre = form.nombre.data
        alumno.apaterno = form.apaterno.data 
        alumno.email = form.email.data
        
        try:
            db.session.commit()
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al modificar: {e}")

    return render_template('alumnos/modificar.html', form=form, alumno=alumno)

@alumnos.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    form = UserForm2(request.form)
    
    if request.method == 'GET':
        id_alum = request.args.get('id')
        if not id_alum:
            return redirect(url_for('alumnos.index'))
            
        alumno = Alumnos.query.get_or_404(id_alum)
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apaterno.data = alumno.apaterno 
        form.email.data = alumno.email
        
        return render_template("alumnos/eliminar.html", form=form, alumno=alumno)

    if request.method == 'POST':
        alumno = Alumnos.query.get(form.id.data)
        if alumno:
            try:
                db.session.delete(alumno)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error al eliminar: {e}")
        
        return redirect(url_for('alumnos.index'))

    return redirect(url_for('alumnos.index'))