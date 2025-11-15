import json

#extraer generos, artistas y canciones de un archivo json
def extraer_musica(ruta_json):
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

    return resultados

#hacer lo mismo con la kb_medicina.json
def extraer_medico(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []

    enfermedades = data.get("enfermedades", {})
    for enfermedad, info in enfermedades.items():
        resultados.append(enfermedad)

        for sintoma in info.get("sintomas", []):
            resultados.append(sintoma)


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

    return resultados


def probabilidad_tema(promt,resultado):

    contador = 0

    promt_array = promt.split()

    probabilidad_palabra = []

    for palabra in promt_array:
        palabra_minuscula = palabra.lower()
        for item in resultado:
            item_minuscula = item.lower()
            if palabra_minuscula in item_minuscula:
                contador = contador + 4
            
            probabilidad_palabra.append(contador / max(len(palabra),len(item)))
            contador = 0

    probabilidad_total = sum(probabilidad_palabra) / len(probabilidad_palabra)

    return probabilidad_total

def inferir_tema(promt):
    resultado_musica = extraer_musica("kb/kb_musica.json")
    resultado_medico = extraer_medico("kb/kb_medico.json")

    probabilidad_musica = probabilidad_tema(promt,resultado_musica)
    probabilidad_medico = probabilidad_tema(promt,resultado_medico)

    print(resultado_medico)

    if probabilidad_musica*100 < 1.2 and probabilidad_medico*100 < 1.2:
        tema = "tema general"
    
    elif probabilidad_musica > probabilidad_medico:
        tema = "musica"

    else: 
        tema = "medico"

    print(f"Probalidades: musica: {probabilidad_musica*100}%, probabilidad medico: {probabilidad_medico*100}%")

    return f"Estas hablado de {tema}"