# -*- coding: utf-8 -*-
import json
import time
import redis
import settings
from pysentimiento import SentimentAnalyzer

# from classifier import SentimentClassifier
########################################################################

########################################################################
# COMPLETAR AQUI: Crear conexion a redis y asignarla a la variable "db".
########################################################################
# db=0 indice para la tabla dentro de la base de datos.

db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                 db=settings.REDIS_DB_ID)
########################################################################

########################################################################
# COMPLETAR AQUI: Instanciar modelo de análisis de sentimientos.
# Use classifier.SentimentClassifier de la libreria
# spanish_sentiment_analysis ya instalada
########################################################################
# model = SentimentClassifier()
model = SentimentAnalyzer()
########################################################################


def sentiment_from_score(score_dict):
    """
    Esta función recibe como entrada el score de positividad
    de nuestra sentencia y dependiendo su valor devuelve uno
    de las siguientes clases:
        - "Positivo": Cuando el score es mayor a 0.55.
        - "Neutral": Cuando el score se encuentra entre 0.45 y 0.55.
        - "Negativo": Cuando el score es menor a 0.45.

    Attributes
    ----------
    score : float
        Porcentaje de positividad.

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    """
    ####################################################################
    # COMPLETAR AQUI
    ####################################################################
    score = 0.0
    sentiment = ''

    for key, value in score_dict.items():
        score = value if value >= score else score
        sentiment = key if value >= score else sentiment

    if sentiment == 'NEG':
        sentiment = 'Negativo'
    elif sentiment == 'NEU':
        sentiment = 'Neutral'
    else:
        sentiment = 'Positivo'
    ####################################################################

    return sentiment, score


def predict(text: str):
    """
    Esta función recibe como entrada una oración y devuelve una
    predicción de su sentimiento acompañado del score de positividad.

    Attributes
    ----------
    text : str
        Sentencia para analizar

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    score : float
        Porcentaje de positividad.
    """

    ####################################################################
    # COMPLETAR AQUI: Utilice el clasificador instanciado previamente
    # ("model") para obtener el score de positividad.
    # Luego utilice la función "sentiment_from_score" de este módulo
    # para obtener el sentimiento ("sentiment") a partir del score.
    ####################################################################
    score_dict = model.predict_probas(text)
    sentiment, score = sentiment_from_score(score_dict)
    ####################################################################

    return sentiment, score


def classify_process():
    """
    Obtiene trabajos encolados por el cliente desde Redis. Los procesa
    y devuelve resultados.
    Toda la comunicación se realiza a travez de Redis, por ello esta
    función no posee atributos de entrada ni salida.
    """
    # Iteramos intentando obtener trabajos para procesar
    # Worker que se encuentra escuchando tod el dia.
    while True:
        ##################################################################
        # COMPLETAR AQUI: Obtenga un batch de trabajos encolados, use
        # lrange de Redis. Almacene los trabajos en la variable "queue".
        # Servidor de procesamiento obtiene 10 tareas encoladas a la base
        # de datos
        ##################################################################
        queue = db.lrange(name='service_queue', start=0, end=9)
        ##################################################################

        # Iteramos por cada trabajo obtenido
        for item in queue:
            ##############################################################
            # COMPLETAR AQUI:
            #     - Utilice nuestra función "predict" para procesar la
            #       sentencia enviada en el trabajo.
            #     - Cree un diccionario con dos entradas: "prediction" y
            #       "score" donde almacenara los resultados obtenidos.
            #     - Utilice la funcion "set" de Redis para enviar la
            #       respuesta. Recuerde usar como "key" el "job_id".
            #
            ##############################################################
            # item = {'text': 'hoy es un lindo dia', 'id': '2'}
            # el item se encuentra codificado, ya que el envio de bytes tiene
            # menos carga que enviar texto plano.

            item_raw = json.loads(item.decode(settings.CODE))
            job_id = item_raw[settings.KEY_ID]
            sentiment, score = predict(item_raw[settings.KEY_TEXT])

            response = {'prediction': sentiment, 'score': score}

            # el job_id es el idenficador de respuesta.
            db.set(name=job_id, value=json.dumps(response))
            ##############################################################

        ##################################################################
        # COMPLETAR AQUI: Use ltrim de Redis para borrar los trabajos ya
        # procesados. Luego duerma durante unos milisengundos antes de
        # pedir por mas trabajos.
        ##################################################################
        ##################################################################
        # se borran los mensaje de la fifo.
        # service_queue, es similar al topic de kafka
        db.ltrim(name='service_queue', start=len(queue), end=-1)

        time.sleep(2)
        ##################################################################


if __name__ == "__main__":
    print('Launching ML service...')
    classify_process()
