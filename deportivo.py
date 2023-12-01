# deportivo.py

from evento import Evento

class Deportivo(Evento):
    def __init__(self, nombre, municipio, fecha, colonia, calle, numero):
        super().__init__(nombre, municipio, fecha, tipo_evento="Deportivo")
        self.colonia = colonia
        self.calle = calle
        self.numero = numero

