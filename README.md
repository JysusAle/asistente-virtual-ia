# 🦖 DinoBot - Asistente Virtual Inteligente

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Repo Size](https://img.shields.io/badge/repo-size--dynamic-lightgrey.svg)](https://github.com/tu-usuario/dinobot)

**DinoBot** es un asistente virtual de escritorio desarrollado en Python que combina múltiples disciplinas de la Inteligencia Artificial: procesamiento de lenguaje natural (NLP), sistemas expertos basados en conocimiento, algoritmos de búsqueda en grafos y sistemas de recomendación vectorial.

Su objetivo es interactuar con el usuario a través de una interfaz gráfica moderna para resolver tareas específicas: recomendaciones musicales basadas en emociones, diagnóstico médico preliminar por inferencia de síntomas, cálculo de rutas óptimas en el metro y conversación general.

---

## 📋 Tabla de Contenidos

1. [Características Principales](#-características-principales)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Requisitos Previos](#-requisitos-previos)
4. [Instalación y Configuración](#-instalación-y-configuración)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Módulos y Funcionamiento Técnico](#-módulos-y-funcionamiento-técnico)
7. [Bases de Conocimiento (Knowledge Base)](#-bases-de-conocimiento-knowledge-base)
8. [Uso](#-uso)
9. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
10. [Autores](#-autores)

---

## 🚀 Características Principales

* **Interfaz Gráfica (GUI):** Construida con **Flet**, ofrece un diseño oscuro y minimalista para una interacción fluida tipo chat.
* **Detección de Intención:** Clasifica automáticamente la entrada del usuario en cuatro categorías: Música, Metro, Medicina o Charla General mediante análisis de similitud semántica.
* **Sistema de Navegación (Metro CDMX):** Implementa el algoritmo **Dijkstra** para encontrar la ruta más rápida entre estaciones, considerando transbordos y costos de líneas.
* **Recomendación Musical Vectorial:** Utiliza **Similitud Coseno** y análisis de sentimientos para sugerir canciones basándose en la valencia (ánimo) y energía de la solicitud, detectando incluso negaciones (ej. "no quiero algo triste").
* **Diagnóstico Médico Básico:** Un sistema experto que infiere posibles enfermedades correlacionando los síntomas descritos por el usuario con una base de conocimientos.
* **Charla General:** Responde a saludos, preguntas sobre su identidad y definiciones conceptuales.

---

## 🏗 Arquitectura del Sistema

El flujo de datos de DinoBot sigue el siguiente esquema:

1. **Entrada:** El usuario escribe un mensaje en la GUI (`main.py`).
2. **Preprocesamiento:** El texto se limpia (stopwords, tokenización) usando `tokenizacion.py`.
3. **Clasificación:** `analisis.py` determina la probabilidad de pertenencia a cada tópico (Música, Metro, Medicina, General).
4. **Ejecución Lógica:** Dependiendo del tema clasificado, se llama al script especializado (`amor.py`, `inferencia.py` o `vetores_musica.py`).
5. **Generación de Respuesta:** El módulo correspondiente procesa los datos (JSON) y devuelve una respuesta en texto natural que se muestra en la interfaz.

### Diagrama (Mermaid)
> Este diagrama se renderiza en GitHub automáticamente si está habilitado el soporte de Mermaid.

```mermaid
flowchart LR
  U[Usuario] -->|mensaje| GUI[GUI - main.py]
  GUI --> Token[tokenizacion.py]
  Token --> Anal[analisis.py]
  Anal -->|Música| Vet[vetores_musica.py]
  Anal -->|Metro| Amor[amor.py]
  Anal -->|Medicina| Inf[inferencia.py]
  Anal -->|General| KB[kb/*.json]
  Vet --> KB
  Amor --> KB
  Inf --> KB
  KB --> GUI
```

---

## ⚙ Requisitos Previos

* **Python 3.8+**
* Conexión a internet (para la descarga inicial de modelos NLP).

---

## 🛠 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local.

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/dinobot.git
cd dinobot
```

### 2. Crear un entorno virtual (recomendado)

#### En Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Descargar modelos y corpus NLP
Ejecuta los siguientes comandos en tu terminal **o** en una consola de Python según prefieras:

```bash
# Spacy (modelo en español)
python -m spacy download es_core_news_md

# NLTK (desde consola Python):
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

> Nota: el conjunto exacto de paquetes NLTK puede variar según tu pipeline; `punkt` y `stopwords` son los más comúnmente usados para tokenización y limpieza de texto en español.

### 5. Configurar Variables de Entorno (Opcional)
Si planeas usar funciones que requieran API keys (p. ej. OpenAI), crea un archivo `.env` en la raíz con:

```
OPENAI_API_KEY=tu_clave_aqui
```

### 6. Ejecutar la aplicación
```bash
python main.py
```

---

## 📂 Estructura del Proyecto

```
DinoBot/
│
├── kb/                          # Bases de Conocimiento (JSON)
│   ├── kb_general.json
│   ├── kb_medico.json
│   ├── kb_metro.json
│   ├── kb_musica.json
│   └── kb_musica_vectorial.json
│
├── amor.py                      # Lógica de grafos y Dijkstra para el Metro
├── analisis.py                  # Identificación del tema de conversación (Router)
├── grafos.py                    # Clases abstractas de Nodos y Grafos
├── inferencia.py                # Motor de inferencia médica
├── main.py                      # Punto de entrada y GUI (Flet)
├── tokenizacion.py              # Funciones de NLP (Spacy/NLTK)
├── vetores_musica.py            # Recomendador basado en vectores y coseno
└── requirements.txt             # Lista de dependencias del proyecto
```

> Observación: mantuve los nombres de archivo `amor.py` y `vetores_musica.py` tal como están en tu repo. Si quieres renombrarlos (por ejemplo a `metro_logic.py` o `vectores_musica.py`), recuerda actualizar las importaciones en el código.

---

## 🧠 Módulos y Funcionamiento Técnico

### 1. Tokenización y NLP (`tokenizacion.py`)
* Usa Spacy con `es_core_news_md`.
* Limpieza: elimina caracteres no alfabéticos y stopwords.
* Similitud semántica: calcula distancia vectorial entre prompt y palabras clave.
* Asigna puntaje para decidir intención.

### 2. Motor de Rutas - Metro (`amor.py`)
* Modela la red del Metro de la CDMX como un grafo ponderado.
* Nodos: estaciones. Aristas: conexiones y transbordos.
* Algoritmo: Dijkstra (considera costo por transbordo).
* Normalización de cadenas para tolerar pequeños errores ortográficos.

### 3. Recomendador Musical (`vetores_musica.py`)
* Enfoque vectorial según modelo Valence-Arousal.
* Diccionario emocional mapea palabras clave a coordenadas (energía, valencia).
* Detecta negaciones para ajustar el vector emocional.
* Usa `cosine_similarity` para encontrar canciones más cercanas.

### 4. Sistema de Inferencia Médica (`inferencia.py`)
* Extrae síntomas del texto vía similitud semántica.
* Consulta `kb_medico.json` y calcula probabilidad basada en coincidencias.
* Devuelve diagnóstico ordenado por probabilidad.

---

## 📚 Bases de Conocimiento (Knowledge Base)

Los archivos JSON en `kb/` contienen la información estructurada que usan los módulos:

* `kb_general.json` — patrones de conversación y definiciones.
* `kb_metro.json` — estaciones, líneas y distancias.
* `kb_medico.json` — enfermedades con sus síntomas.
* `kb_musica_vectorial.json` — dataset con atributos de energía y valencia.

---

## 💻 Uso

Ejemplos de prompts:

* Música: `"Recomiéndame algo para hacer ejercicio intenso"` o `"Quiero música que no sea triste"`.
* Metro: `"¿Cómo llego de Observatorio a Zócalo?"` o `"Ruta desde Tacubaya hasta Pino Suárez"`.
* Medicina: `"Me duele mucho la cabeza y tengo sensibilidad a la luz"` o `"Tengo fiebre y tos seca"`.
* General: `"¿Quién te creó?"`, `"¿Qué es la inteligencia artificial?"` o `"Hola, buenos días"`.

---

## 🧪 Tecnologías Utilizadas

* Python 3
* Flet (GUI)
* Spacy, NLTK (NLP)
* Pandas, NumPy
* Scikit-learn (similitud coseno)
* Implementaciones propias de grafos

---

## ✒ Autores

Equipo Ingesaurios — Desarrollo e Implementación

Proyecto creado para la materia de Inteligencia Artificial.

Hecho con ❤️ y 🦕 en Python.
