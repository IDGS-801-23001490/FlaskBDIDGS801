from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField, FloatField, RadioField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    id = IntegerField('id')
    nombre=StringField("nombre",[
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4,max=20,message="requiere min=4 max=20")
    ])
    apaterno=StringField("apaterno",[
        validators.DataRequired(message="El apellido es requerido"),
    ])
    correo=EmailField("correo",[
        validators.Email(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])