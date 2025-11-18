# importamos librerías, API KEY e iniciamos cliente

import os                           
from dotenv import load_dotenv 
import openai as ai
from IPython.display import Audio
import librosa


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cliente = ai.OpenAI()

# llamada a la API

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='alloy',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')

# guardado del archivo

ruta = '../../files/salida.mp3'

respuesta.write_to_file(ruta)

# escuchar el audio

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)

# ejemplo echo

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='echo',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')


respuesta.write_to_file(ruta)

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)

# ejemplo fable

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='fable',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')


respuesta.write_to_file(ruta)

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)

# ejemplo onyx

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='onyx',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')


respuesta.write_to_file(ruta)

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)

# ejemplo nova

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='nova',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')


respuesta.write_to_file(ruta)

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)

# ejemplo shimmer

respuesta = cliente.audio.speech.create(model='tts-1',
                                        voice='shimmer',
                                        input='Hoy estamos aprendiendo como usar el modelo TTS.')


respuesta.write_to_file(ruta)

data, freq = librosa.load(ruta)

Audio(data=data, rate=freq)