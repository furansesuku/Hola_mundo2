from datetime import datetime
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

@app.route("/")
def inicio():
    hoy = datetime.now()
    fecha = f"{DIAS[hoy.weekday()]}, {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"
    return f"<p>Buenos días, hoy es {fecha}</p><h1>Hola mundo</h1>"