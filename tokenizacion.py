import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import random

# Intentamos cargar el modelo, si falla, intentamos descargarlo (fallback de seguridad)
try:
    nlp = spacy.load("es_core_news_md")
except OSError:
    print("Modelo de Spacy no encontrado. Descargando modelo básico...")
    from spacy.cli import download
    download("es_core_news_md")
    nlp = spacy.load("es_core_news_md")

def limpiar_texto(texto):
    """Limpia el texto eliminando stopwords y caracteres no alfabéticos."""
    tokens = word_tokenize(texto.lower(), language='spanish')
    stop_words = set(stopwords.words('spanish'))
    # Filtramos para dejar solo palabras significativas
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(tokens)

def similitud_semantica(prompt, texto):
    """Calcula qué tan parecidas son dos frases."""
    prompt_clean = limpiar_texto(prompt)
    texto_clean = limpiar_texto(texto)
    
    doc1 = nlp(prompt_clean)
    doc2 = nlp(texto_clean)
    
    # Seguridad: Si los vectores están vacíos (palabras no reconocidas), retornar 0
    if not doc1.vector.any() or not doc2.vector.any():
        return 0.0
    
    similitud = doc1.similarity(doc2)
    return round(similitud * 100, 2)

def probabilidad_tema(prompt, resultado):
    """
    Calcula la relevancia de un tema basándose en la acumulación de coincidencias.
    MEJORA: Ahora usa 'Suma de Similitudes' en lugar de promedio simple para no penalizar listas largas.
    """
    prompt_tokens = limpiar_texto(prompt)
    if not prompt_tokens:
        return 0.0

    # Convertimos a lista para verificar coincidencias exactas
    lista_prompt = prompt_tokens.split()
    prompt_doc = nlp(prompt_tokens)
    
    if not resultado: 
        return 0.0

    puntaje_total = 0.0
    # Umbral: Solo contamos coincidencias que sean al menos 75% similares
    UMBRAL_SIMILITUD = 0.75 

    for item in resultado:
        item_str = item.lower()
        
        # 1. Coincidencia Exacta (Suma 1 punto completo)
        if item_str in lista_prompt:
            # print(f"Match exacto: {item_str}") # Descomentar para depurar
            puntaje_total += 1.0
            continue # Pasamos al siguiente item para no sumar doble

        # 2. Similitud Semántica (Suma entre 0 y 1 punto según parecido)
        item_doc = nlp(item_str)
        
        # Verificamos vectores válidos
        if item_doc.vector_norm and prompt_doc.vector_norm:
            similitud = prompt_doc.similarity(item_doc)
        else:
            similitud = 0.0
        
        # Solo sumamos si la similitud es relevante (mayor al umbral)
        if similitud > UMBRAL_SIMILITUD:
            # print(f"Match semántico: {item_str} ({similitud:.2f})") # Descomentar para depurar
            puntaje_total += similitud

    # Retornamos el puntaje acumulado. 
    # Ejemplo: Si encuentra "fiebre" (1.0) y "tos" (1.0), devuelve 2.0.
    return round(puntaje_total, 2)

def generar_respuesta(tema, inferencias, kb):
    print(f"\n\nSolicitando respuesta para el tema: {tema}...\n")

    try:
        with open(kb, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return "Error: No se encontró el archivo de base de datos (JSON)."

    respuesta = ""

    # Lógica para temas específicos (Música y Medicina)
    if tema == "musica" or tema == "medicina":
        # 1. Buscamos frases de respuesta o usamos default
        posibles_respuestas = data.get("request", [])
        
        if posibles_respuestas:
            base_respuesta = random.choice(posibles_respuestas)
        else:
            base_respuesta = "Aquí está la información que encontré:"

        # 2. Procesamos las inferencias (los resultados encontrados)
        if isinstance(inferencias, list) and len(inferencias) > 0:
            respuesta = base_respuesta
            for inferencia in inferencias:
                respuesta = respuesta + "\n - " + str(inferencia)
        elif inferencias == -1 or not inferencias:
            respuesta = "Lo siento, analicé tu solicitud pero no encontré coincidencias exactas en mi base de datos."
        else:
            # Caso borde: inferencias no es lista
            respuesta = str(inferencias)

    # Lógica para Tema General (Charla)
    elif tema == "tema general":
        prompt = inferencias # En main.py pasas el user_message como 'inferencias'
        mejor_score = 0
        respuesta = "No estoy seguro de entenderte, vaya nub"

        for categoria, subcategorias in data.items():
            if not isinstance(subcategorias, dict): 
                continue
                
            for subcat, contenido in subcategorias.items():
                if not isinstance(contenido, dict):
                    continue
                
                # Buscamos en las keywords de cada entrada
                for keyword in contenido.get("keywords", []):
                    score = similitud_semantica(prompt, keyword)
                    if score > mejor_score:
                        mejor_score = score
                        # Priorizamos 'respuesta', si no hay, buscamos 'funcion' (aunque no se ejecute aquí)
                        if "respuesta" in contenido:
                            respuesta = contenido["respuesta"]
                        elif "funcion" in contenido and "respuesta" in contenido:
                             respuesta = contenido["respuesta"]
        
        # Filtro de calidad para no responder disparates
        if mejor_score < 50: # Umbral semántico (0-100)
            respuesta = "No tengo suficiente información sobre eso en mi base de datos general."

    return respuesta