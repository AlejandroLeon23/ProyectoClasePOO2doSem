from flask import Flask, render_template, request, redirect, url_for
from evento import Evento
from cultural import Cultural
from musical import Musical
from deportivo import Deportivo
from politico import Politico

app = Flask(__name__)

# Lista para almacenar eventos
eventos = []

@app.route('/')
def index():
    return render_template('index.html', eventos=eventos)

@app.route('/home')
def home():
    return render_template('index.html', eventos=eventos)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            # Verificar que todos los campos requeridos estén presentes
            campos_requeridos = ['tipo_evento', 'nombre', 'municipio', 'fecha', 'colonia', 'calle', 'numero']
            for campo in campos_requeridos:
                if campo not in request.form or not request.form[campo].strip():
                    raise MissingFormDataException(f"El campo '{campo}' es requerido.")

            tipo_evento = request.form['tipo_evento']
            nombre = request.form['nombre']
            municipio = request.form['municipio']
            fecha = request.form['fecha']
            colonia = request.form['colonia']
            calle = request.form['calle']
            numero = request.form['numero']

            # Crear el evento basado en el tipo
            if tipo_evento == 'Cultural':
                evento = Cultural(nombre, municipio, fecha, colonia, calle, numero)
            elif tipo_evento == 'Musical':
                evento = Musical(nombre, municipio, fecha, colonia, calle, numero)
            elif tipo_evento == 'Deportivo':
                evento = Deportivo(nombre, municipio, fecha, colonia, calle, numero)
            elif tipo_evento == 'Politico':
                evento = Politico(nombre, municipio, fecha, colonia, calle, numero)
            else:
                evento = Evento(nombre, municipio, fecha)

            eventos.append(evento)
            return redirect(url_for('index'))

        except MissingFormDataException as e:
            # Manejar el error si falta algún dato del formulario
            print(f"Error en el formulario: {e}")
            return f"Error en el formulario: {e}", 400

    return render_template('registro.html')

class MissingFormDataException(Exception):
    """Excepción para manejar la falta de datos en el formulario."""
    pass

imagenes_evento = {
    "Cultural": "Cultural.jpg",
    "Musical": "Musical.jpg",
    "Deportivo": "Deportivo.jpg",
    "Político": "Político.jpg"
}

@app.route('/evento/<tipo_evento>')
def mostrar_evento(tipo_evento):
    evento_seleccionado = None
    for evento in eventos:
        if tipo_evento == evento.tipo_evento:
            evento_seleccionado = evento
            break

    if evento_seleccionado is not None:
        ruta_imagen = imagenes_evento.get(tipo_evento, "imagen_default.jpg")
        return render_template('evento.html', evento=evento_seleccionado, ruta_imagen=ruta_imagen)
    else:
        return "Evento no encontrado", 404
    
    
@app.route('/eventos/culturales')
def mostrar_eventos_culturales():
    eventos_culturales = [evento for evento in eventos if evento.tipo_evento == 'Cultural']
    return render_template('evento.html', eventos=eventos_culturales)

@app.route('/eventos/deportivos')
def mostrar_eventos_deportivos():
    eventos_deportivos = [evento for evento in eventos if evento.tipo_evento == 'Deportivo']
    return render_template('evento.html', eventos=eventos_deportivos)

@app.route('/eventos/politicos')
def mostrar_eventos_politicos():
    eventos_politicos = [evento for evento in eventos if evento.tipo_evento == 'Politico']
    return render_template('evento.html', eventos=eventos_politicos)

@app.route('/eventos/musicales')
def mostrar_eventos_musicales():
    eventos_musicales = [evento for evento in eventos if evento.tipo_evento == 'Musical']
    return render_template('evento.html', eventos=eventos_musicales)

    
if __name__ == '__main__':
    app.run(debug=True)
