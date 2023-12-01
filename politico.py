# politico.py

from evento import Evento

class Politico(Evento):
    def __init__(self, nombre, municipio, fecha, colonia, calle, numero):
        super().__init__(nombre, municipio, fecha, tipo_evento="Politico")
        self.colonia = colonia
        self.calle = calle
        self.numero = numero
