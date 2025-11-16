import json
from tokenizacion import probabilidad_tema

#extraer generos, artistas y canciones de un archivo json
def extraer_musica(ruta_json,palabras_clave):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []

    generos = data.get("generos", {})

    for genero, info_genero in generos.items():
        # conseguimos el genero
        resultados.append(genero)

        artistas = info_genero.get("artistas", {})

        for artista, info_artista in artistas.items():
            #conseguir artista
            resultados.append(artista)

            canciones = info_artista.get("canciones", [])
            for cancion in canciones:
                #conseguir caciones
                resultados.append(cancion)

    if palabras_clave == True: resultados = extraer_palabras_clave(ruta_json,resultados)

    return resultados

#hacer lo mismo con la kb_medicina.json
def extraer_medico(ruta_json, palabras_clave):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []

    enfermedades = data.get("enfermedades", {})
    for enfermedad, info in enfermedades.items():
        resultados.append(enfermedad)

        for sintoma in info.get("sintomas", []):
            resultados.append(sintoma)

    if palabras_clave == True: resultados = extraer_palabras_clave(ruta_json,resultados)

    return resultados

def extraer_metro(ruta_json,palabras_clave):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []

    lineas = data.get("lineas", {})
    for linea, info in lineas.items():
        resultados.append(linea)

        for estacion in info.get("estaciones", []):
            resultados.append(estacion)

    if palabras_clave == True: resultados = extraer_palabras_clave(ruta_json,resultados)

    return resultados

#hacer lo mismo con la kb_general.json
def extraer_conversacion_general(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    resultados = []

    for saludo in data.get("saludos", {}):
        resultados.append(saludo)
    
    for identidad in data.get("identidad", {}):
        resultados.append(identidad)

    for conversacion in data.get("conversacion", {}):
        resultados.append(conversacion)

    for conceptos in data.get("conceptos", {}):
        resultados.append(conceptos)
    
    for funciones in data.get("funcioness", {}):
        resultados.append(funciones)

    print(f"resultados = {resultados}\n")
    return resultados

def extraer_palabras_clave(ruta_json,resultados):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for palabra in data.get("palabras_clave", {}):
        if palabra not in resultados:
            resultados.append(palabra)

    return resultados

def identificar_tema(prompt):
    resultado_musica = extraer_musica("kb/kb_musica.json",True)
    resultado_medico = extraer_medico("kb/kb_medico.json",True)
    resultado_metro = extraer_metro("kb/kb_metro.json",True)
    resultado_general = extraer_conversacion_general("kb/kb_general.json")

    probabilidad_musica = probabilidad_tema(prompt,resultado_musica)
    probabilidad_medico = probabilidad_tema(prompt,resultado_medico)
    probabilidad_metro = probabilidad_tema(prompt,resultado_metro)
    probabilidad_general = probabilidad_tema(prompt,resultado_general)

    temas = {
        "musica": probabilidad_musica,
        "medicina": probabilidad_medico,
        "metro": probabilidad_metro,
        "tema general": probabilidad_general
    }

    if all(prob * 100 < 1.2 for prob in temas.values()):
        tema = "tema general"
    else:
        tema = max(temas, key=temas.get)

    print(f"\n\n probalidad: musica: {probabilidad_musica}% \n probabilidad medico: {probabilidad_medico}% \n probabilidad metro: {probabilidad_metro}%\n probabilidad tema general {probabilidad_general}\n\n\n")

    return tema