# seed_users_pg.py
# Script para poblar PostgreSQL con usuarios de prueba y un administrador
# Ejecutar con: python seed_users_pg.py

import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# -------------------------------
# 1. Cargar variables de entorno
# -------------------------------
load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASS = os.getenv("ADMIN_PASS")

# -------------------------------
# 2. Configurar Flask y SQLAlchemy
# -------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------------
# 3. Modelo Usuario
# -------------------------------
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="cliente")

# -------------------------------
# 4. Poblar la base de datos
# -------------------------------
def poblar():
    db.create_all()

    # Lista de usuarios de prueba
    clientes = [
        {"nombre": "Ana García", "email": "ana.garcia@example.com", "password": "Ana12345!"},
        {"nombre": "Bruno Díaz", "email": "bruno.diaz@example.com", "password": "Bruno12345!"},
        {"nombre": "Carla López", "email": "carla.lopez@example.com", "password": "Carla12345!"},
        {"nombre": "Diego Pérez", "email": "diego.perez@example.com", "password": "Diego12345!"},
        {"nombre": "Elena Torres", "email": "elena.torres@example.com", "password": "Elena12345!"},
        {"nombre": "Fabio Rivas", "email": "fabio.rivas@example.com", "password": "Fabio12345!"},
        {"nombre": "Giselle Gómez", "email": "giselle.gomez@example.com", "password": "Giselle12345!"},
        {"nombre": "Héctor Silva", "email": "hector.silva@example.com", "password": "Hector12345!"},
        {"nombre": "Ivana Campos", "email": "ivana.campos@example.com", "password": "Ivana12345!"},
        {"nombre": "Julián Vázquez", "email": "julian.vazquez@example.com", "password": "Julian12345!"},
    ]

    # Insertar usuarios
    for c in clientes:
        if not Usuario.query.filter_by(email=c["email"]).first():
            u = Usuario(
                nombre=c["nombre"],
                email=c["email"],
                password=generate_password_hash(c["password"]),
                rol="cliente"
            )
            db.session.add(u)
            print(f"Insertado: {c['email']}")
        else:
            print(f"Ya existe: {c['email']} — lo salto.")

    # Insertar administrador
    if ADMIN_EMAIL and ADMIN_PASS:
        if not Usuario.query.filter_by(email=ADMIN_EMAIL).first():
            admin = Usuario(
                nombre="Administrador",
                email=ADMIN_EMAIL,
                password=generate_password_hash(ADMIN_PASS),
                rol="admin"
            )
            db.session.add