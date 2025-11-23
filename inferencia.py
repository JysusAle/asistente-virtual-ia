from analisis import *
from grafos import *
from tokenizacion import similitud_semantica

def extraer_proposiciones(tema, prompt, kb):

    if tema == "medicina":
        proposiciones = extraer_medico(kb,False)
    if tema == "metro":
        proposiciones = extraer_metro(kb,False)
    if tema == "musica":
        proposiciones = extraer_musica(kb,False)
    if tema == "tema general":
        proposiciones = extraer_conversacion_general(kb)

    proposiciones_obetenidas = []

    for proposicion in proposiciones:
        if proposicion in prompt:
            proposiciones_obetenidas.append(proposicion)

    return proposiciones_obetenidas

def inferir_recomendacion_musica(prompt, kb):
    prompt = prompt.lower()

    lista_generos = cargar_kb_musica(kb)
    proposiciones = extraer_proposiciones("musica",prompt,kb)

    inferencias = []

    #Inferir Por silogismo hipotetico
    #buscar por genero: Si Rock -> Artistas de Rock, Artista Rock -> cancion_Artista Rock: Rock -> CancionesRock,ArtistasRock
    for genero in lista_generos:
        if genero.nombre in proposiciones:
            for artista in genero.artistas:
                if not(artista.nombre in proposiciones or artista.nombre in inferencias):
                    print(f"{genero.nombre} -> {artista.nombre}\n")
                    for cancion in artista.canciones:
                        if not(cancion.nombre in proposiciones or cancion.nombre in inferencias):
                            print(f"{genero.nombre} -> {artista.nombre} -> {cancion.nombre}")
                            print(f"{genero.nombre} -> {cancion.nombre}\n")
                            inferencias.append(cancion.nombre + " de " + artista.nombre)

    #Inferir por Artista
    #Si Artista -> Genero_Artista, Del Genero -> Artistas, Artista -> Canciones: Artista -> Canciones_Similares,Artistas_similares
        for Artista in genero.artistas:
            if Artista.nombre in prompt:
                for artista in genero.artistas:
                    if not(artista.nombre in prompt or artista.nombre in inferencias): 
                        print(f"{Artista.nombre} -> {artista.nombre}\n")

                    for cancion in artista.canciones:
                        if not(cancion.nombre in prompt or cancion.nombre in inferencias): 
                            inferencias.append(cancion.nombre + " de " + artista.nombre)
                            print(f"{Artista.nombre} -> {artista.nombre} -> {cancion.nombre}")
                            print(f"{Artista.nombre} -> {cancion.nombre}\n")

    #Similra para Canciones
            for cancion in Artista.canciones:
                if cancion.nombre in prompt:
                    for artista in genero.artistas:
                        if not(artista.nombre in prompt or artista.nombre in inferencias): 
                            print(f"{cancion.nombre} -> {genero.nombre}")                            
                            print(f"{genero.nombre} -> {artista.nombre}")
                            print(f"{cancion.nombre} -> {artista.nombre}\n")

                        for cancion in artista.canciones:
                            if not(cancion.nombre in prompt or cancion.nombre in inferencias): 
                                inferencias.append(cancion.nombre + " de " + artista.nombre)
                                print(f"{Artista.nombre} -> {artista.nombre} -> {cancion.nombre}")
                                print(f"{Artista.nombre} -> {cancion.nombre}\n")
    return inferencias
    

def inferir_enfermedad(prompt, kb_path):
    sintomas_usuario = inferir_sintomas(prompt, kb_path)
    print(f"\nsintomas inferidos: {sintomas_usuario}\n")

    if len(sintomas_usuario) <2:
        return -1
    
    enfermedades = cargar_kb_medicina(kb_path)

    enfermedades_probables = []

    for enf in enfermedades:
            sintomas_enf = [s.nombre for s in enf.sintomas]

            coincidencias = 0
            for s in sintomas_usuario:
                if s in sintomas_enf:
                    coincidencias += 1
                    print(f"{s} -> {enf.nombre}\n")
            
            if coincidencias == 0:
                continue  

            prob = coincidencias / len(sintomas_enf)

            enfermedades_probables.append(enf.nombre)
            print(f"{enf.nombre} con un {prob} de probabilidad\n")

    if not enfermedades_probables:
        return -1

    enfermedades_probables.sort(key=lambda x: x[2], reverse=True)
    print(f"{enfermedades_probables}\n")

    return enfermedades_probables


def inferir_sintomas(prompt, kb):

    with open(kb, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []
    sintomas = data.get("sintomas", {})

    for sintoma, descripciones in sintomas.items():
        for frase in descripciones:
            similitud = similitud_semantica(prompt, frase)
            if similitud >= 70:
                print(f"{frase} -> {sintoma} con un {similitud}%\n")
                resultados.append(sintoma)
                break  

    return resultados
