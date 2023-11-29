import json
import os
import pickle
import random
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np

from app.config.jwt import get_current_user
from app.controllers.rol import RolController
from app.models.message import Message
from app.models.rol import NombreRol
from app.startup import BASE_DIR, training
from app.util.api_router import APIRouter

training()

router = APIRouter()

rol_controller = RolController()


lemmatizer = WordNetLemmatizer()

intents_json_file = os.path.join(BASE_DIR, "util", "intents.json")
intents = json.loads(open(intents_json_file).read())

words_pkl = os.path.join(BASE_DIR, "chatbot", "words.pkl")
classes_pkl = os.path.join(BASE_DIR, "chatbot", "classes.pkl")
chatbotmodel_keras = os.path.join(BASE_DIR, "chatbot", "chatbotmodel.keras")

words = pickle.load(open(words_pkl, "rb"))
classes = pickle.load(open(classes_pkl, "rb"))
model = load_model(chatbotmodel_keras)


def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            return random.choice(i["responses"])

    return "No entiendo. Por favor intenta de nuevo."


@router.post("/", status_code=status.HTTP_200_OK)
def chatbot(
    payload: Message,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False
    es_empleado = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True
            break

    if es_admin is False and es_empleado is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "No tiene permisos para hacer esta operación",
                "cause": "bad_auth",
            },
        )

    ints = predict_class(payload.content)
    res = get_response(ints, intents)

    return {
        "msg": "Mensaje enviado",
        "data": {
            "message": {
                "content": res,
                "role": "bot",
            },
        },
    }
