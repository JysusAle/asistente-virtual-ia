#-------------------------------Grafos y nodos para Metro-----------------------------------------
import json

class estacion:
    def __init__(self, nombre, sig_estacion, distancia_sig, ant_estacion, distancia_ant):
        self.nombre = nombre
        self.sig_estacion = sig_estacion
        self.distancia_sig = distancia_sig
        self.ant_estacion = ant_estacion
        self.distancia_ant = distancia_ant

        self.transbordos = []
    
class linea:
    def __int__(self,nombre):
        self.nombre = nombre
        self.estaciones = []

    def agregar_estacion(self,estacion):
        self.estaciones.append(estacion)

class mapa_metro:
    def __inti__ (self):
        self.lineas = []

    def agregar_linea(self,linea):
        self.lineas.append(linea)


def iniciar_mapa():
    mapa = mapa_metro()

#----------------------------------Grafos y nodos para musica--------------------------------------------

class genero:
    def __init__(self,nombre,artistas):
        self.nombre = nombre
        self.artistas = artistas

class artista:
    def __init__(self,nombre,canciones):
        self.nombre = nombre
        self.canciones = canciones

class cancion:
    def __init__(self,nombre):
        self.nombre = nombre

#--------------------------------Grefos y nodos para medicina-------------------------------------------

class enfermedad:
    def __init__(self,nombre,sintomas):
        self.nombre = nombre
        self.sintomas = sintomas

class sintoma:
    def __init__(self,nombre):
        self.nombre = nombre

#-------------------------------Algoritmos para musica-------------------------------------------------

def cargar_kb_musica(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    generos_lista = []

    generos_json = data.get("generos", {})

    for nombre_genero, info_genero in generos_json.items():

        artistas_dict = info_genero.get("artistas", {})
        lista_artistas = []

        for nombre_artista, info_artista in artistas_dict.items():

            canciones_lista = [
                cancion(nombre_cancion)
                for nombre_cancion in info_artista.get("canciones", [])
            ]

            artista_obj = artista(nombre_artista, canciones_lista)
            lista_artistas.append(artista_obj)

        genero_obj = genero(nombre_genero, lista_artistas)
        generos_lista.append(genero_obj)

    return generos_lista

#-------------------------------Algoritmos para medicina-----------------------------------------------

def cargar_kb_medicina(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    enfermedades_json = data.get("enfermedades", {})

    lista_enfermedades = []

    for nombre_enfermedad, info in enfermedades_json.items():

        sintomas_nombres = info.get("sintomas", [])

        lista_sintomas = [sintoma(nombre_s) for nombre_s in sintomas_nombres]

        enfermedad_obj = enfermedad(nombre_enfermedad, lista_sintomas)

        lista_enfermedades.append(enfermedad_obj)

    return lista_enfermedades