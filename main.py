import flet 
from flet import Page, TextField, Dropdown, Column, Text, ElevatedButton, Container, Colors, Row, dropdown
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os
from inferir import inferir_tema

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def funcion():
    return "Hola soy dinoBot, tu asistente virtual"

"""""
def get_ai_reponse(inferencia, prompt):
    try: 
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": inferencia},
                {"role": "user", "content": prompt}
            ],

            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al generar la respuesta"
    
"""""

def main(page: Page):
    page.title = "DinoBot - Asistente Virtual"
    page.bgcolor = Colors.BLUE_GREY_900
    page.theme_mode = flet.ThemeMode.DARK 
    
    input_box = TextField(
        label="Escribe tu mensaje aquí",
        border_color=Colors.BLUE_200,
        focused_border_color=Colors.BLUE_400,
        text_style=flet.TextStyle(color=Colors.WHITE),
        expand=True
    )

    mode_dropdown = Dropdown(
        value="Conversación General",
        label="Modo",
        border_color=Colors.BLUE_200,
        color=Colors.WHITE,
        options=[
            dropdown.Option("Conversación General", "chat"),
            dropdown.Option("Modo Divertido", "fun"),
        ]
    )

    chat_area = Column(scroll="auto", expand=True)

    def send_message(e):
        user_message = input_box.value
        if not user_message:
            return
        
        chat_area.controls.append(Text(f"Tu: {user_message}", color=Colors.WHITE))

        response = inferir_tema(user_message)

        chat_area.controls.append(Text(f"DinoBot: {response}", color=Colors.BLUE_200))
        
        input_box.value = ""
        page.update()

    send_button = ElevatedButton(
        text="Enviar",
        on_click=send_message,
        bgcolor=Colors.BLUE_700,
        color=Colors.WHITE
    )

    chat_container = Container(
        content=chat_area,
        bgcolor=Colors.BLUE_GREY_800,
        padding=10,
        border_radius=10,
        expand=True
    )
    
    print("Chat container bgcolor:", chat_container.bgcolor)  # Debug

    input_container = Container(
        content=Row(  
            controls=[
                mode_dropdown,
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