#-------------------------------Grafos y nodos para Metro-----------------------------------------
import json
import heapq

class estacion:
    def __init__(self, nombre, sig_estacion, distancia_sig, ant_estacion, distancia_ant):
        self.nombre = nombre
        self.sig_estacion = sig_estacion
        self.distancia_sig = distancia_sig
        self.ant_estacion = ant_estacion
        self.distancia_ant = distancia_ant

        self.transbordos = []
    
class linea:
    def __init__(self,nombre):
        self.nombre = nombre
        self.estaciones = []

    def agregar_estacion(self,estacion):
        self.estaciones.append(estacion)

class mapa_metro:
    def __init__ (self):
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

#----------------------------------------Algoritmos para Metro----------------------------------------------

def iniciar_mapa(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    mapa = mapa_metro()
    estaciones_global = {}   # para detectar transbordos

    lineas_json = data.get("lineas", {})

    # RECORRER CADA LÍNEA
    for nombre_linea, info_linea in lineas_json.items():

        linea_obj = linea(nombre_linea)
        estaciones_json = info_linea.get("estaciones", {})

        estaciones_lista = list(estaciones_json.items())

        # CREAR TODAS LAS ESTACIONES DE LA LÍNEA
        for i in range(len(estaciones_lista)):
            nombre_est, (dist_ant, dist_sig) = estaciones_lista[i]

            # estación anterior
            if i == 0:
                ant = None
                distA = None
            else:
                ant = estaciones_lista[i-1][0]
                distA = dist_ant

            # estación siguiente
            if i == len(estaciones_lista) - 1:
                sig = None
                distS = None
            else:
                sig = estaciones_lista[i+1][0]
                distS = dist_sig

            # Crear el objeto estación
            est_obj = estacion(nombre_est, sig, distS, ant, distA)
            linea_obj.agregar_estacion(est_obj)

            # Guardar en el registro global para detectar transbordos
            if nombre_est not in estaciones_global:
                estaciones_global[nombre_est] = [est_obj]
            else:
                estaciones_global[nombre_est].append(est_obj)

        mapa.agregar_linea(linea_obj)

    # PROCESAR TRANSBORDOS
    for nombre, lista_est in estaciones_global.items():
        if len(lista_est) > 1:  # hay transbordo
            for est in lista_est:
                for otra in lista_est:
                    if est is not otra:
                        est.transbordos.append(otra)

    return mapa

# - - - - A* Para el metro - - - - - 

def a_star_ruta(origen, destino, mapa):
    start = buscar_estacion(mapa, origen)
    goal = buscar_estacion(mapa, destino)

    if not start or not goal:
        print("\nNo se encontro ninguna estacion")
        return None

    # Priority queue: (costo_total_estimado, costo_acumulado, estacion_actual, ruta)
    open_list = []
    heapq.heappush(open_list, (0, 0, start, [start.nombre]))

    visited = {}

    while open_list:
        _, costo_actual, actual, ruta = heapq.heappop(open_list)

        # Si ya llegamos
        if actual.nombre == goal.nombre:
            return ruta, costo_actual

        # Evitar reexploración si ya se llegó más barato
        if actual.nombre in visited and visited[actual.nombre] <= costo_actual:
            continue

        visited[actual.nombre] = costo_actual

        # Generar vecinos:
        vecinos = []

        # 1. Siguiente estación
        if actual.sig_estacion:
            sig = buscar_estacion(mapa, actual.sig_estacion)
            if sig:
                vecinos.append((sig, actual.distancia_sig))

        # 2. Estación anterior
        if actual.ant_estacion:
            ant = buscar_estacion(mapa, actual.ant_estacion)
            if ant:
                vecinos.append((ant, actual.distancia_ant))

        # 3. Transbordos (distancia 0)
        for t in actual.transbordos:
            vecinos.append((t, 0))

        # Explorar vecinos
        for vecino, costo in vecinos:
            new_cost = costo_actual + (costo if costo else 0)
            heuristic = 0  # sin info geográfica, A* se vuelve Dijkstra
            total_est = new_cost + heuristic

            heapq.heappush(open_list, (total_est, new_cost, vecino, ruta + [vecino.nombre]))

    print("\n-------------------------")
    return None

def buscar_estacion(mapa, nombre):
    for ln in mapa.lineas:
        for est in ln.estaciones:
            if est.nombre.lower() == nombre.lower():
                return est
    return None
