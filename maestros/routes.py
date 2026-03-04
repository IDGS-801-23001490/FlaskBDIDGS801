from flask import render_template, request, redirect, url_for, flash
from models import db, Maestros
from forms import MaestroForm
from . import maestros

@maestros.route("/index")
def index():
    maestros_list = Maestros.query.all()
    return render_template("maestros/index.html", maestros=maestros_list)

@maestros.route("/registrar", methods=["GET", "POST"])
def registrar():
    form = MaestroForm(request.form)
    if request.method == "POST" and form.validate():
        maestro = Maestros(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for('maestros.index'))
    return render_template("maestros/registrar.html", form=form)

@maestros.route("/detalles")
def detalles():
    matricula = request.args.get('matricula')
    maestro = Maestros.query.get_or_404(matricula)
    return render_template("maestros/detalles.html", maestro=maestro)

@maestros.route("/modificar", methods=["GET", "POST"])
def modificar():
    form = MaestroForm(request.form)
    matricula = request.args.get('matricula') or form.matricula.data
    maestro = Maestros.query.get_or_404(matricula)
    
    if request.method == 'GET':
        form.matricula.data = maestro.matricula
        form.nombre.data = maestro.nombre
        form.apellidos.data = maestro.apellidos
        form.especialidad.data = maestro.especialidad
        form.email.data = maestro.email
    
    if request.method == 'POST' and form.validate():
        maestro.nombre = form.nombre.data
        maestro.apellidos = form.apellidos.data
        maestro.especialidad = form.especialidad.data
        maestro.email = form.email.data
        db.session.commit()
        return redirect(url_for('maestros.index'))
    return render_template('maestros/modificar.html', form=form, maestro=maestro)

@maestros.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    matricula = request.args.get('matricula')
    maestro = Maestros.query.get_or_404(matricula)
    if request.method == 'POST':
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('maestros.index'))
    return render_template("maestros/eliminar.html", maestro=maestro)