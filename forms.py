from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    id = IntegerField('id')

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=2, max=50, message="Mínimo 2 y máximo 50 caracteres")
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="Los apellidos son requeridos"),
        validators.Length(min=2, max=200, message="Máximo 200 caracteres")
    ])

    email = EmailField("Correo electrónico", [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo válido")
    ])

    telefono = StringField("Teléfono", [
        validators.DataRequired(message="El número de teléfono es obligatorio"),
        validators.Length(min=10, max=20, message="Ingrese un teléfono válido (mínimo 10 dígitos)")
    ])