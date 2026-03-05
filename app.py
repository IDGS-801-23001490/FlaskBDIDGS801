from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db
from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros, url_prefix='/maestros')
app.register_blueprint(alumnos, url_prefix='/alumnos')
app.register_blueprint(cursos, url_prefix='/cursos')

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)