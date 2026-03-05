from wtforms import Form, StringField, IntegerField, EmailField, SelectField, validators

class UserForm2(Form):
    id = IntegerField('id')

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=2, max=50, message="Mínimo 2 y máximo 50 caracteres")
    ])

    apaterno = StringField("Apellido Paterno", [
        validators.DataRequired(message="El apellido es requerido"),
        validators.Length(min=2, max=50, message="Máximo 50 caracteres")
    ])

    email = EmailField("Correo electrónico", [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo válido")
    ])

class MaestroForm(Form):
    matricula = IntegerField('Matrícula')

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=2, max=50, message="Nombre entre 2 y 50 caracteres")
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="Los apellidos son requeridos"),
        validators.Length(min=2, max=50, message="Apellidos entre 2 y 50 caracteres")
    ])

    especialidad = StringField("Especialidad", [
        validators.DataRequired(message="La especialidad es requerida"),
        validators.Length(min=2, max=50, message="Máximo 50 caracteres")
    ])

    email = EmailField("Correo electrónico", [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo válido"),
        validators.Length(max=50, message="El correo no debe exceder los 50 caracteres")
    ])

class CursoForm(Form):
    id = IntegerField('id')
    
    nombre = StringField("Nombre del curso", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=2, max=150, message="Máximo 150 caracteres")
    ])
    
    descripcion = StringField("Descripción", [
        validators.Length(max=500, message="Máximo 500 caracteres")
    ])
    
    maestro_id = SelectField("Maestro", coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un maestro")
    ])