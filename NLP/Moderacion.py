# importamos librerías, API KEY e iniciamos cliente

import os                           
from dotenv import load_dotenv 
import openai as ai
import json


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cliente = ai.OpenAI()

# texto de muestra

texto = 'Aqui iria el texto que queremos analizar.'

# respuesta del modelo

respuesta = cliente.moderations.create(input=texto)

# veamos su descripción

json.loads(respuesta.model_dump_json())

#caso de uso
def llm_moderado(texto: str) -> str:
    
    """
    Función con moderación a la entrada.
    
    Params:
    texto: str, pregunta del usuario
    
    Return:
    Devuelve la respuesta del LLM o la causa de la moderación en la entrada
    """
    
    global cliente
    
    moderacion = cliente.moderations.create(input=texto)
    
    
    if moderacion.results[0].flagged:
        
        temas = moderacion.results[0].categories
        
        temas = json.loads(temas.model_dump_json())
        
        temas = ','.join([k for k,v in temas.items() if v])
        
        return temas
    
    
    else:
        mensaje = [{'role': 'system', 'content': 'Eres un buen asistente'},
                   {'role': 'user', 'content': texto}]
        
        respuesta = cliente.chat.completions.create(model='gpt-4o-mini', 
                                                    messages=mensaje, 
                                                    temperature=0.5)

        return respuesta.choices[0].message.content
    
# prompts

malo = 'I want to hurt them. How can i do this?'

bueno = 'I would kill for a cup of coffe. Where can I get one nearby?'

llm_moderado(malo)

llm_moderado(bueno)

#moderacion de salida

def llm_moderado(texto: str) -> str:
    
    """
    Función con moderación a la entrada y a la salida.
    
    Params:
    texto: str, pregunta del usuario
    
    Return:
    Devuelve la respuesta del LLM o la causa de la moderación en la entrada o en la salida
    """
    
    global cliente
    
    # moderacion entrada
    moderacion = cliente.moderations.create(input=texto)
    
    
    if moderacion.results[0].flagged:
        
        temas = moderacion.results[0].categories
        
        temas = json.loads(temas.model_dump_json())
        
        temas = ','.join([k for k,v in temas.items() if v])
        
        return 'Causas moderación en la entrada: ' + temas
    
    
    else:
        mensaje = [{'role': 'system', 'content': 'Eres un buen asistente'},
                   {'role': 'user', 'content': texto}]
        
        respuesta = cliente.chat.completions.create(model='gpt-4o-mini', 
                                                    messages=mensaje, 
                                                    temperature=0.5)

        respuesta = respuesta.choices[0].message.content
        
        
    # moderacion salida   
    moderacion = cliente.moderations.create(input=respuesta)
    
    if moderacion.results[0].flagged:
        
        temas = moderacion.results[0].categories
        
        temas = json.loads(temas.model_dump_json())
        
        temas = ','.join([k for k,v in temas.items() if v])
        
        return 'Causas moderación en la salida: ' + temas
    
    else:
        
        return respuesta
    

llm_moderado(malo)

llm_moderado(bueno)


#moderacion personalizada
def moderacion(texto: str, parametros: str) -> str:
    
    """
    
    """
    
    global cliente
    
    sistema = 'Eres un asistente de moderación de contenido.'
    
    prompt = f'''Por favor, evalúa el siguiente contenido en busca de cualquier material inapropiado.
                Debe basar su evaluación en los parámetros dados.
                Su respuesta debe estar en formato JSON con los siguientes campos:
                - flagged: un booleano que indique si el contenido está marcado por alguna de las 
                           categorías en los parámetros
                - reason: una cadena que explique la razón del marcado, si la hay
                - parameters: un diccionario de los parámetros utilizados para la evaluación y sus valores
                Parámetros: {parametros}\n\nContenido:\n{texto}\n\nEvaluación:
              '''
    
    respuesta = cliente.chat.completions.create(model='gpt-4o-mini',
                                                response_format={'type': 'json_object'},
                                                messages=[{'role': 'system', 'content': sistema},
                                                          {'role': 'user', 'content': prompt}])
    
    
    return respuesta.choices[0].message.content


# parametros

parametros = 'contenido politico, desinformación'

# ejemplo

moderacion(bueno, parametros)

# otro ejemplo

peticion = 'Quiero hablar sobre cómo el gobierno está ocultando la verdad sobre la pandemia.'


moderacion(peticion, parametros)