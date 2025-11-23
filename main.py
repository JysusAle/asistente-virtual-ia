import flet 
from flet import Page, TextField, Dropdown, Column, Text, ElevatedButton, Container, Colors, Row
"from openai import OpenAI"
import requests
from dotenv import load_dotenv
import os
from analisis import identificar_tema
from inferencia import *
from tokenizacion import generar_respuesta
from amor import resolver_ruta
from vetores_musica import recomendar_canciones

load_dotenv()

def main(page: Page):
    page.title = "DinoBot - Asistente Virtual"
    page.bgcolor = Colors.BLUE_GREY_900
    page.theme_mode = flet.ThemeMode.DARK 
    
    # 1. Primero definimos el área de chat (porque la función la necesita)
    chat_area = Column(scroll="auto", expand=True)

    # 2. Definimos la caja de texto SIN el on_submit todavía
    input_box = TextField(
        label="Escribe tu mensaje aquí",
        border_color=Colors.BLUE_200,
        focused_border_color=Colors.BLUE_400,
        text_style=flet.TextStyle(color=Colors.WHITE),
        expand=True
    )

    # 3. AHORA definimos la función (que usa chat_area e input_box)
    def send_message(e):
        kb_musica = "kb/kb_musica.json"
        kb_metro = "kb/kb_metro.json"
        kb_medico = "kb/kb_medico.json"
        kb_general = "kb/kb_general.json"

        user_message = input_box.value
        if not user_message:
            return
        
        chat_area.controls.append(Text(f"Tu: {user_message}", color=Colors.WHITE))

        tema = identificar_tema(user_message)

        # Estructura if-elif-else corregida
        tema = identificar_tema(user_message)

        if tema == "musica":
            kb_musica_vec = "kb/kb_musica_vectorial.json"
            lista_canciones = recomendar_canciones(user_message, kb_musica_vec)
        
            response = "Basado en tus gustos (Energía/Ánimo), te recomiendo:\n" + "\n".join(lista_canciones)
            
        elif tema == "medicina":
            response = generar_respuesta(tema,inferir_enfermedad(user_message,kb_medico),kb_medico)
        elif tema == "metro":
            response = resolver_ruta(user_message,kb_metro)
        else: 
            response = generar_respuesta(tema,user_message,kb_general)
        
        chat_area.controls.append(Text(f"DinoBot: {response}", color=Colors.BLUE_200))
        
        input_box.value = ""
        input_box.focus() # Truco extra: mantiene el cursor en la caja para seguir escribiendo
        page.update()

    # 4. FINALMENTE conectamos el enter y el botón con la función ya creada
    input_box.on_submit = send_message  # <--- AQUÍ ES SEGURO HACERLO

    send_button = ElevatedButton(
        text="Enviar",
        on_click=send_message,
        bgcolor=Colors.BLUE_700,
        color=Colors.WHITE
    )

    # 5. Armamos el diseño visual
    chat_container = Container(
        content=chat_area,
        bgcolor=Colors.BLUE_GREY_800,
        padding=10,
        border_radius=10,
        expand=True
    )
    
    input_container = Container(
        content=Row(  
            controls=[
                input_box,
                send_button
            ],
            spacing=10
        )
    )

    main_layout = Column(
        controls=[
            chat_container,
            input_container
        ],
        expand=True,
        spacing=10
    )

    page.add(main_layout)

    page.window.width = 800
    page.window.height = 600
    page.update()

if __name__ == "__main__":
    flet.app(target=main)