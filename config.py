# config.py
# Este archivo centraliza la configuración de la aplicación.
# Lee las variables de entorno desde .env y prepara la conexión a MongoDB.

import os
from pymongo import MongoClient

class Config:
    # Clave secreta para proteger sesiones y formularios en Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_por_defecto")

    # URI de conexión a MongoDB (Atlas o local)
    MONGO_URI = os.environ.get("MONGO_URI")

    # Credenciales del administrador (definidas en .env)
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    ADMIN_PASS = os.environ.get("ADMIN_PASS")

    # Configuración SMTP para enviar correos de pedidos
    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")

    # Número de WhatsApp en formato internacional (ej: 54911...)
    BUSINESS_WHATSAPP = os.environ.get("BUSINESS_WHATSAPP")

# Conexión a MongoDB usando la URI
client = MongoClient(Config.MONGO_URI)

# Seleccionamos la base de datos (si la URI incluye nombre, se usa directamente)
db = client["por_ese_palpitar"]

# Colección de usuarios para login/registro
usuarios = db.usuarios