import json
import os
import pickle
import random

from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np

from app.config.jwt import hash_password
from app.controllers.rol import RolController
from app.controllers.usuario import UsuarioController
from app.models.create_usuario_schema import CreateUsuarioSchema
from app.models.rol import NombreRol

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class UsuarioAdminNotFound(Exception):
    pass


class RolAdminNotFound(Exception):
    pass


def crear_usuario_admin():
    rol_controller = RolController()

    rol = rol_controller.get_by_nombre(NombreRol.administrador)
    if rol is None:
        raise RolAdminNotFound

    usuario = CreateUsuarioSchema(
        nombre=os.environ.get("ADMIN_NOMBRE", "Usuario"),
        apellido=os.environ.get("ADMIN_APELLIDO", "Admin"),
        code_country=os.environ.get("ADMIN_CODE_COUNTRY", "57"),
        phone_number=os.environ.get("ADMIN_NUMBER", "1234567890"),
        email=os.environ.get("ADMIN_EMAIL", "admin@email.com"),
        contrasena=os.environ.get("ADMIN_CONTRASENA", "admin123"),
        numero_documento=os.environ.get("ADMIN_NUM_DOC", "100200300400"),
        rol_id=rol["id"],
    )

    usuario_controller = UsuarioController()

    user_found = usuario_controller.get_by_email(usuario.email.lower())
    if user_found is not None:
        print("admin user already exists")
        return

    usuario.contrasena = hash_password(str(usuario.contrasena))
    usuario.email = usuario.email.lower()

    usuario_controller.create(usuario)
    print("admin user created")


chatbot_dir = os.path.join(BASE_DIR, "chatbot")
os.makedirs(chatbot_dir, exist_ok=True)


def training():
    words_pkl = os.path.join(chatbot_dir, "words.pkl")
    classes_pkl = os.path.join(chatbot_dir, "classes.pkl")
    chatbotmodel_keras = os.path.join(chatbot_dir, "chatbotmodel.keras")

    if (
        os.path.exists(words_pkl)
        and os.path.exists(classes_pkl)
        and os.path.exists(chatbotmodel_keras)
    ):
        print("already trained")
        return

    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)

    lemmatizer = WordNetLemmatizer()

    intents_json_file = os.path.join(BASE_DIR, "util", "intents.json")
    intents_json = open(intents_json_file).read()

    intents = json.loads(intents_json)

    words = []
    classes = []
    documents = []
    ignore_letters = ["?", "!", ".", ","]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            words_list = nltk.word_tokenize(pattern)
            words.extend(words_list)
            documents.append((words_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    classes = sorted(set(classes))

    pickle.dump(words, open(words_pkl, "wb"))
    pickle.dump(classes, open(classes_pkl, "wb"))

    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype="object")

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation="softmax"))

    optimizer = Adam(learning_rate=0.01)
    model.compile(
        loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"]
    )

    hist = model.fit(
        np.array(train_x),
        np.array(train_y),
        epochs=500,
        batch_size=5,
        verbose=1,
    )
    model.save(chatbotmodel_keras, hist)

    print("training done")
