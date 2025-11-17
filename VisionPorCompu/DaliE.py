# importamos librerías, API KEY e iniciamos cliente

import os                           
from dotenv import load_dotenv 
import openai as ai
from PIL import Image
import requests as req
from io import BytesIO
import base64

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cliente = ai.OpenAI()

# creamos el prompt para generar la imagen

prompt = 'Un leon hacker cyberpunk soñando con una cebra, arte digital'

# llamada a la API con respuesta en formato url

respuesta = cliente.images.generate(model='dall-e-3',
                                    prompt=prompt,
                                    n=1,
                                    size='1024x1024',
                                    response_format='url')

# carga de la imagen con Pillow

imagen = Image.open(fp=req.get(url=respuesta.data[0].url, stream=True).raw)

# guardado de la imagen 

imagen.save(fp='../../images/leon_hacker_cyberpunk.png')

# llamada a la API con respuesta en formato b64_json

respuesta = cliente.images.generate(model='dall-e-3',
                                    prompt=prompt,
                                    n=1,
                                    size='1024x1024',
                                    response_format='b64_json')

# imagen en formato b64_json

json = respuesta.data[0].b64_json

# carga de la imagen con Pillow

imagen = Image.open(BytesIO(base64.b64decode(json)))

imagen.save(fp='../../images/leon_hacker_cyberpunk2.png')

# creamos variaciones

respuesta = cliente.images.create_variation(image=BytesIO(base64.b64decode(json)),  
                                            n=2,
                                            size='1024x1024',
                                            response_format='url')

# imagen 1

imagen = Image.open(fp=req.get(url=respuesta.data[0].url, stream=True).raw)

# imagen 2

imagen = Image.open(fp=req.get(url=respuesta.data[1].url, stream=True).raw)

#editar iamngenes
# primero creamos una mascara opaca

ancho = 1024
alto = 1024

mascara = Image.new('RGBA', (ancho, alto), (0, 0, 0, 1))  

# hacemos la mitad de abajo transparente, esta parte será modificada

for x in range(ancho):
    # todo el ancho, la mitad de altura
    for y in range(alto // 2, ancho):  
        mascara.putpixel((x, y), (0, 0, 0, 0))

# se guarda la mascara

mascara.save('../../images/mascara.png')

# editamos la imagen que hemos generado con la mascara

edicion = cliente.images.edit(image=open('../../images/leon_hacker_cyberpunk2.png', 'rb'),
                              prompt=prompt,
                              mask=open('../../images/mascara.png', 'rb'),  
                              n=1,
                              size='1024x1024',
                              response_format='url')

# convertimos la imagen a PIL

imagen = Image.open(fp=req.get(url=edicion.data[0].url, stream=True).raw)