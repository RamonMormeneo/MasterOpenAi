#Crear nuestro propio asistente

# importamos librerías, API KEY e iniciamos cliente

import os                           
from dotenv import load_dotenv 
import openai as ai
import json


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cliente = ai.OpenAI()

# creamos el asistente

asistente = cliente.beta.assistants.create(name='Tutor de matemáticas',
                                           instructions='''Eres un tutor personal de matemáticas. 
                                                        Responde preguntas brevemente, en una frase o menos.''',
                                           model='gpt-4o')

# veamos su descripción

json.loads(asistente.model_dump_json())

# creamos el hilo

thread = cliente.beta.threads.create()

# veamos su descripción

json.loads(thread.model_dump_json())

# ahora añadimos un mensaje al hilo

mensaje = cliente.beta.threads.messages.create(thread_id=thread.id,
                                               role='user',
                                               content='¿Puedes resolver la ecuación `3x + 11 = 14`?')

# veamos su descripción

json.loads(mensaje.model_dump_json())

# creamos una ejecución

run = cliente.beta.threads.runs.create(thread_id=thread.id,
                                       assistant_id=asistente.id)

# veamos su descripción

json.loads(run.model_dump_json())

# importamos time para manejo temporal

import time

# creamos función para espera de la respuesta

def esperar_ejecucion(run: object, thread: object) -> object:
    
    """
    Esta función espera a que se complete la ejecución
    revisando el status.
    
    Params:
    run: openai.types.beta.threads.run.Run, ejecución
    thread: openai.types.beta.thread.Thread, hilo
    
    Return:
    run: openai.types.beta.threads.run.Run, ejecución completada
    """
    
    while run.status == 'queued' or run.status == 'in_progress':
        
        run = cliente.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        time.sleep(0.5)
        
    return run

# espera de la ejecución y descripción

run = esperar_ejecucion(run, thread)

json.loads(run.model_dump_json())

# vista de los mensajes y respuesta

mensajes = cliente.beta.threads.messages.list(thread_id=thread.id)

json.loads(mensajes.model_dump_json())['data'][0]['content'][0]['text']['value']

# crea un mensaje para añadir al hilo
mensaje = cliente.beta.threads.messages.create(thread_id=thread.id, 
                                               role='user', 
                                               content='¿Puedes explicarlo?')

# ejecución
run = cliente.beta.threads.runs.create(thread_id=thread.id, assistant_id=asistente.id)

# esperar ejecución
run = esperar_ejecucion(run, thread)

# todos los mensajes
mensajes = cliente.beta.threads.messages.list(thread_id=thread.id, order='asc', after=mensaje.id)


mensajes.data[0].content[0].text.value

# añadimos code interpreter al asistente

asistente = cliente.beta.assistants.update(assistant_id=asistente.id,
                                           tools=[{'type': 'code_interpreter'}])

# veamos su descripción

json.loads(asistente.model_dump_json())

# creamos el hilo

thread = cliente.beta.threads.create()

# ahora añadimos un mensaje al hilo

usuario = 'Genera los 10 primeros números de la secuencia de Fibonacci con código.'

mensaje = cliente.beta.threads.messages.create(thread_id=thread.id,
                                               role='user',
                                               content=usuario)

# creamos una ejecución

run = cliente.beta.threads.runs.create(thread_id=thread.id,
                                       assistant_id=asistente.id)

# espera de la ejecución 

run = esperar_ejecucion(run, thread)

# vista de los mensajes y respuesta

mensajes = cliente.beta.threads.messages.list(thread_id=thread.id)

mensajes.data[0].content[0].text.value

# lista de pasos

pasos = cliente.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id, order='asc')

# detalle de cada paso

for p in pasos.data:
    
    detalles = p.step_details
    
    print(json.dumps(json.loads(detalles.model_dump_json()), indent=4))


# añadimos file search al asistente

asistente = cliente.beta.assistants.update(assistant_id=asistente.id,
                                           tools=[{'type': 'file_search'}])

# cargar un archivo en el asistente

ruta = '../../../files/language_models_are_unsupervised_multitask_learners.pdf'


archivo = cliente.files.create(file=open(ruta, 'rb'),
                               purpose='assistants')

# creamos el hilo y enviar mensaje

mensaje = 'extrae 10 bullet points del libro.'

config = [{'role': 'user', 'content': mensaje,
           'attachments': [{ 'file_id': archivo.id, 'tools': [{'type': 'file_search'}]}]}]

thread = cliente.beta.threads.create(messages=config)

# creamos una ejecución

run = cliente.beta.threads.runs.create(thread_id=thread.id,
                                       assistant_id=asistente.id)

# espera de la ejecución 

run = esperar_ejecucion(run, thread)

# vista de los mensajes y respuesta

mensajes = cliente.beta.threads.messages.list(thread_id=thread.id)

print(mensajes.data[0].content[0].text.value)