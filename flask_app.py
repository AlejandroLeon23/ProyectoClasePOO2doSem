from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/creaciones'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_evento = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    colonia = db.Column(db.String(100))
    calle = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    imagen_url = db.Column(db.String(255))

@app.route('/')
def index():
    eventos = Eventos.query.all()  # Recupera todos los eventos de la base de datos
    return render_template('index.html', eventos=eventos)


@app.route('/home')
def home():
    eventos = Eventos.query.all()  # Recupera todos los eventos de la base de datos
    return render_template('index.html', eventos=eventos)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
            nuevo_evento = Eventos(
            tipo_evento=request.form['tipo_evento'],
            nombre=request.form['nombre'],
            municipio=request.form['municipio'],
            fecha=request.form['fecha'],
            colonia=request.form['colonia'],
            calle=request.form['calle'],
            numero=request.form['numero']
            )
    return render_template('registro.html')

# Añade otras rutas según sea necesario
    
@app.route('/eventos/culturales')
def mostrar_eventos_culturales():
    eventos_culturales = Eventos.query.filter_by(tipo_evento='Cultural').all()
    return render_template('eventocultural.html', eventos=eventos_culturales)

@app.route('/eventos/deportivos')
def mostrar_eventos_deportivos():
    eventos_deportivos = Eventos.query.filter_by(tipo_evento='Deportivo').all()
    return render_template('eventodeportivo.html', eventos=eventos_deportivos)

@app.route('/eventos/politicos')
def mostrar_eventos_politicos():
    eventos_politicos = Eventos.query.filter_by(tipo_evento='Politico').all()
    return render_template('eventopolitico.html', eventos=eventos_politicos)

@app.route('/eventos/musicales')
def mostrar_eventos_musicales():
    eventos_musicales = Eventos.query.filter_by(tipo_evento='Musical').all()
    return render_template('eventomusical.html', eventos=eventos_musicales)

@app.route('/delete_evento/<int:id>', methods=['POST'])
def delete_evento(id):
    evento = Eventos.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
