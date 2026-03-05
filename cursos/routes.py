from flask import render_template, request, redirect, url_for
from models import db, Curso, Maestros, Alumnos
from forms import CursoForm
from cursos import cursos

@cursos.route('/')
def index():
    lista_cursos = Curso.query.all()
    return render_template('cursos/index.html', cursos=lista_cursos)

@cursos.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = CursoForm(request.form)
    
    maestros = Maestros.query.all()
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'POST' and form.validate():
        nuevo_curso = Curso(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            maestro_id=form.maestro_id.data
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect(url_for('cursos.index'))
        
    return render_template('cursos/registrar.html', form=form)

@cursos.route('/detalles/<int:id>', methods=['GET', 'POST'])
def detalles(id):
    curso = Curso.query.get_or_404(id)
    alumnos_disponibles = Alumnos.query.filter(~Alumnos.cursos.any(id=id)).all()

    if request.method == 'POST':
        action = request.form.get('action') 
        alumno_id = request.form.get('alumno_id')
        
        if alumno_id:
            alumno = Alumnos.query.get(alumno_id)
            if alumno:
                if action == 'inscribir':
                    curso.alumnos.append(alumno)
                elif action == 'desinscribir':
                    curso.alumnos.remove(alumno)
                
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error en la inscripción/desinscripción: {e}")
                    
        return redirect(url_for('cursos.detalles', id=curso.id))

    return render_template('cursos/detalles.html', curso=curso, alumnos_disponibles=alumnos_disponibles)

@cursos.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    curso = Curso.query.get_or_404(id)
    form = CursoForm(request.form)
    
    maestros = Maestros.query.all()
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'GET':
        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id

    if request.method == 'POST' and form.validate():
        curso.nombre = form.nombre.data
        curso.descripcion = form.descripcion.data
        curso.maestro_id = form.maestro_id.data
        
        try:
            db.session.commit()
            return redirect(url_for('cursos.index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al modificar el curso: {e}")

    return render_template('cursos/modificar.html', form=form, curso=curso)

@cursos.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    curso = Curso.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            curso.alumnos.clear() 
            
            db.session.delete(curso)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar el curso: {e}")
            
        return redirect(url_for('cursos.index'))
        
    return render_template('cursos/eliminar.html', curso=curso)