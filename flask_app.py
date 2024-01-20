from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

##Iniciamos con el framework de flask, para hacer páginas web en python con su  backend lite.
app = Flask(__name__)

#Condiguracion de las credenciales de la DB

#DB En Línea
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://aleonlomeli:EnsenadaITE2023@aleonlomeli.mysql.pythonanywhere-services.com/aleonlomeli$creaciones'
#DB Local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/creaciones'

#Para que se guarden las modificaciones dentro del framework SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Para que se esté reconectando a la DB
app.config['SQLALCHEMY_POOL_RECYCLE'] = 7200

#Reconección de la DB
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 280,
    'pool_pre_ping': True
}
#Inicio de SQL Alchemy
db = SQLAlchemy(app)

# Definir el modelo de la base de datos (Modelo Vista Controlador)
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

#Definicion de la ruta raiz, comando a DB de mostrar todos los eventos de la DB
@app.route('/')
def index():
    eventos = Eventos.query.all()  # Recupera todos los eventos de la base de datos
    return render_template('index.html', eventos=eventos)

#Definicion de HOME, Mismo comando para traer a todos los eventos de la DB
@app.route('/home')
def home():
    eventos = Eventos.query.all()  # Recupera todos los eventos de la base de datos
    return render_template('index.html', eventos=eventos)

#Definicion de la ruta registro, get y post para obtener los datos de los campos del template html
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
            db.session.add(nuevo_evento)
        # Comprometer la transacción a la DB
            db.session.commit()
    return render_template('registro.html')

#Definicion de la ruta con Filtro de los eventos tipo culturales    
@app.route('/eventos/culturales')
def mostrar_eventos_culturales():
    eventos_culturales = Eventos.query.filter_by(tipo_evento='Cultural').all()
    return render_template('eventocultural.html', eventos=eventos_culturales)

#Definicion de la ruta con Filtro de los eventos tipo deportivos
@app.route('/eventos/deportivos')
def mostrar_eventos_deportivos():
    eventos_deportivos = Eventos.query.filter_by(tipo_evento='Deportivo').all()
    return render_template('eventodeportivo.html', eventos=eventos_deportivos)

#Definicion de la ruta con Filtro de los eventos tipo Politicos
@app.route('/eventos/politicos')
def mostrar_eventos_politicos():
    eventos_politicos = Eventos.query.filter_by(tipo_evento='Politico').all()
    return render_template('eventopolitico.html', eventos=eventos_politicos)

#Definicion de la ruta con Filtro de los eventos tipo Musicales
@app.route('/eventos/musicales')
def mostrar_eventos_musicales():
    eventos_musicales = Eventos.query.filter_by(tipo_evento='Musical').all()
    return render_template('evento.html', eventos=eventos_musicales)


#Borrar evento de acuerdo al ID, seleccionado con el botón de cada evento en template
@app.route('/delete_evento/<int:id>', methods=['POST'])
def delete_evento(id):
    evento = Eventos.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/statsmaricos')
def statsmaricos():
    return render_template('statsmaricos.html')

@app.route('/player-stats')
def player_stats():
    api_key = 'RGAPI-da78d03d-0a0b-4020-b2ce-bc15bb97ab6e'
    summoner_names = ['Faenorr']
    region = 'NA1'
    player_stats = []

    for name in summoner_names:
        summoner_url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}'
        response = requests.get(summoner_url)
        if response.status_code == 200:
            summoner_info = response.json()
            # Aquí se puede agregar lógica adicional para obtener estadísticas como victorias/derrotas/rango
            player_stats.append(summoner_info)
        else:
            print(f"Error al obtener información de {name}")
    
    # Renderizar solo las filas de la tabla
    return render_template('player_stats_rows.html', players=player_stats)


#Cierre app flask con su debug true para que muestre los errores comunes
if __name__ == '__main__':
    app.run(debug=True)
