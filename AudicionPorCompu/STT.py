# importamos librerías, API KEY e iniciamos cliente

import os                           
from dotenv import load_dotenv 
import openai as ai
import json


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cliente = ai.OpenAI()

# extracción del texto

audio = open('../../files/Will AI kill everyone Heres what the godfathers of AI have to say.mp4', 'rb')

transcripcion = cliente.audio.transcriptions.create(model='whisper-1', 
                                                    file=audio)

# texto extraido del audio

print(transcripcion.text)

transcripcion = cliente.audio.transcriptions.create(model='whisper-1', 
                                                    file=audio,
                                                    response_format='verbose_json',
                                                    timestamp_granularities=['segment'])

# segmentos de texto con sus tiempos

print(transcripcion.segments[:2])

#crear subtitulos

from datetime import timedelta


def crear_subtitulos(segmentos: list) -> None:
    
    """
    Esta función crea un archivo de subtitulos con la transcripción del audio.
    
    Params:
    segmentos: list, lista de diccionarios con la transcripción y tiempos
    
    Return:
    No devuelve nada, solo guarda el archivo
    """


    for i,s in enumerate(segmentos):
        
        start = str(0)+str(timedelta(seconds=int(s['start'])))+',000'
        end = str(0)+str(timedelta(seconds=int(s['end'])))+',000'
        
        texto = s['text']
        
        segmento = f"{i+1}\n{start} --> {end}\n{texto[1:] if texto[0]==' ' else texto}\n\n"

        with open('../../files/subtitulos.srt', 'a', encoding='utf-8') as file:
            file.write(segmento)
            
    print('Hecho!')


# llamada función

crear_subtitulos(transcripcion.segments)


#Traducion

# carga del archivo de audio

ruta = '../../files/Es posible que una IA.m4a'

audio= open(ruta, 'rb')

# traducción es-en

translation = cliente.audio.translations.create(model='whisper-1', 
                                                file=audio)


# texto traducido

translation.text


#Uso de la propia api de whisper necesario pip instal whisper

# importamos la librería

import whisper

# se carga el modelo base de Whisper en local, 139M

modelo_whisper = whisper.load_model('base')

# cargamos el archivo de audio 

import librosa

data, freq = librosa.load(ruta)

# Whisper transcribe el audio a texto, en 32 bits (fp16=False)

transcripcion = modelo_whisper.transcribe(data, fp16=False)["text"].strip()

