# importamos la API KEY con dotenv

import os                           # libreria del sistema operativo
from dotenv import load_dotenv      # carga variables de entorno 


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# también podríamos hacerlo directamente de la siguiente manera

import openai as ai

ai.api_key = OPENAI_API_KEY

#gpt 3.5

# con API Key explícita

cliente = ai.OpenAI(api_key=OPENAI_API_KEY)

# como variable de entorno directamente

cliente = ai.OpenAI()

# definimos el modelo

modelo = 'gpt-3.5-turbo'

# definición de los mensajes

mensajes = [{'role': 'system', 'content': 'Eres un experto traductor de inglés a castellano.'},
            {'role': 'user', 'content': 'Traduce la siguiente frase: How are you?'}]

# llamada al modelo

respuesta = cliente.chat.completions.create(model=modelo, messages=mensajes)

# tipo de dato de la respuesta

type(respuesta)

# texto de la respuesta

respuesta.choices[0].message.content

# nueva llamada con temperatura 0

modelo = 'gpt-3.5-turbo'

mensajes = [{'role': 'system', 'content': 'Eres un poeta.'},
            {'role': 'user', 'content': 'Crea un poema sobre la IA'}]

respuesta = cliente.chat.completions.create(model=modelo, 
                                            messages=mensajes,
                                            temperature=0)

print(respuesta.choices[0].message.content)

# nueva llamada con temperatura 2 y 100 tokens máximo

respuesta = cliente.chat.completions.create(model=modelo, 
                                            messages=mensajes,
                                            temperature=2,
                                            max_tokens=100)

print(respuesta.choices[0].message.content)


def actualiza_conversación(frase: str, mensajes: list, usuario: str) -> list:
    
    """
    Esta función recibe la conversación y la actualiza para continuar con ella.
    
    Params:
    respuesta: string, pregunta del usuario o respuesta del modelo.
    mensajes: list, lista de la conversación actual.
    usuario: string, "user" o "assistant"
    
    Return:
    Devuelve la lista de diccionarios con la conversación actualizada
    """
    
    
    respuesta = {'role': usuario, 'content': frase}
    
    mensajes.append(respuesta)
    
    return mensajes

# ahora creamos una función para la llamada al modelo


modelo = 'gpt-3.5-turbo'

mensajes = [{'role': 'system', 'content': 'Eres un asistente de estudio.'}]


def chatbot(pregunta: str) -> str:
    
    """
    Función para llamar al chat. 
    Además actualiza la conversación.
    
    Params:
    pregunta: str, pregunta del usuario
    
    Return:
    Devuelve la respuesta del chatbot.
    """
    
    global modelo, mensajes
    
    
    mensajes = actualiza_conversación(frase=pregunta, mensajes=mensajes, usuario='user')
    
    
    respuesta = cliente.chat.completions.create(model=modelo, 
                                                messages=mensajes)
    
    
    respuesta = respuesta.choices[0].message.content
    
    
    mensajes = actualiza_conversación(frase=respuesta, mensajes=mensajes, usuario='assistant')
    
    return respuesta
    
#Ponemos todo en un clase llamada Chatbot
class ChatBot:
    
    def __init__(self, modelo: str, mensaje_sistema: str) -> None:
        
        """
        Método constructor, se definen modelo y mensajes.
        """
        
        self.modelo = modelo
        self.mensajes = [{'role': 'system', 'content': mensaje_sistema}]
        
    
    def actualiza_conversación(self, frase: str, usuario: str) -> None:
    
        """
        Este método recibe actualiza la conversación para continuar con ella.

        Params:
        respuesta: string, pregunta del usuario o respuesta del modelo.
        usuario: string, "user" o "assistant"

        Return:
        Devuelve la lista de diccionarios con la conversación actualizada
        """


        respuesta = {'role': usuario, 'content': frase}

        self.mensajes.append(respuesta)
        
        
    def chatbot(self, pregunta: str) -> str:
    
        """
        Método para llamar al chat. 
        Además actualiza la conversación.

        Params:
        pregunta: str, pregunta del usuario

        Return:
        Devuelve la respuesta del chatbot.
        """


        self.actualiza_conversación(frase=pregunta, usuario='user')


        respuesta = cliente.chat.completions.create(model=self.modelo, 
                                                    messages=self.mensajes)


        respuesta = respuesta.choices[0].message.content


        self.actualiza_conversación(frase=respuesta, usuario='assistant')

        return respuesta


# GPT 4

llm = ChatBot(modelo='gpt-4', mensaje_sistema='Eres un asistente de estudio.')

# definamos una función para pedir el clima de cierto lugar desde una API

import requests as req

def obtener_clima(lugar: str, latitud: str, longitud: str) -> dict:
    
    """
    Esta función es para obtener datos climáticos desde api.open-meteo
    
    Params:
    lugar: string, lugar consultado
    latitud: float, latitud del lugar consultado
    longitud: float, longitud del lugar consultado
    
    Return:
    diccionario con keys: lugar, latitud, longitud, temperatura y velocidad del viento
    """

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current=temperature_2m,wind_speed_10m'
    
    respuesta = req.get(url)

    data = respuesta.json()
    
    temperatura = data['current']['temperature_2m']
    
    viento = data['current']['wind_speed_10m']
    
    salida = {'lugar': lugar,
              'latitud': latitud, 
              'longitud': longitud,
              'temperatura': temperatura,
              'velocidad_viento': viento,
             }
    
    return salida

# definimos la configuración de las herramientas

config = [
          {
            'type': 'function',
            'function': {
              'name': 'obtener_clima',
              'description': 'Esta función es para obtener datos climáticos desde api.open-meteo',
              'parameters': {
                'type': 'object',
                  
                'properties': {
                    'lugar': {
                        'type': 'string',
                        'description': 'lugar consultado, por ejemplo Madrid'},
                    'latitud': {
                        'type': 'number',
                        'description': 'latitud del lugar consultado'},
                    'longitud': {
                        'type': 'number',
                        'description': 'longitud del lugar consultado'},
                },
                
                  'required': ['lugar', 'latitud', 'longitud'],
              },
            }
          }
        ]

# realizamos la llamada al modelo

mensaje = [{'role': 'user', 'content': '¿Qué clima hace hoy en Madrid?'}]


respuesta = cliente.chat.completions.create(model='gpt-4', messages=mensaje, tools=config)

# parámetros de respuesta

llamada = respuesta.choices[0].message.tool_calls[0]

nombre_funcion = llamada.function.name

argumentos = llamada.function.arguments

import json

argumentos = json.loads(argumentos)

# llamada a la función

obtener_clima(**argumentos)


# gpt 4 o

llm = ChatBot(modelo='gpt-4o', mensaje_sistema='Eres un asistente de estudio.')

# visualización imagen 

from PIL import Image

url_img = 'https://upload.wikimedia.org/wikipedia/commons/e/e2/The_Algebra_of_Mohammed_Ben_Musa_-_page_82b.png'

respuesta = req.get(url=url_img, stream=True).raw

imagen = Image.open(fp=respuesta)

# creamos el mensaje con la imagen

mensajes = [{'role': 'system', 'content': 'Eres un asistente de estudio que responde en Markdown.'},
           
            {'role': 'user', 'content': [ {'type': 'text', 'text': '¿Cuál es el área del triángulo?'},
                                          {'type': 'image_url', 'image_url': {'url': url_img}}]}
           ]

# respuesta del modelo

respuesta = cliente.chat.completions.create(model='gpt-4o', messages=mensajes)

# display formato Markdown

from IPython.display import display, Markdown, Latex

display(Markdown(respuesta.choices[0].message.content))

# display formato Latex

display(Latex(respuesta.choices[0].message.content))

# visualización imagen 

from IPython.display import Image

import base64

ruta = '../../../images/triangulo.png'

Image(ruta)

# carga imagen y transforma

with open(ruta, 'rb') as file:
    
    imagen = base64.b64encode(file.read()).decode('utf-8')
    
    
imagen = f'data:image/png;base64,{imagen}'

# creamos el mensaje con la imagen

mensajes = [{'role': 'system', 'content': 'Eres un asistente de estudio que responde en Markdown.'},
           
            {'role': 'user', 'content': [ {'type': 'text', 'text': '¿Cuál es el área del triángulo?'},
                                          {'type': 'image_url', 'image_url': {'url': imagen}}]}
           ]
# respuesta del modelo

respuesta = cliente.chat.completions.create(model='gpt-4o', messages=mensajes)

# display formato Markdown

display(Latex(respuesta.choices[0].message.content))