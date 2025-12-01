# app.py
# Aplicación Flask conectada a PostgreSQL con SQLAlchemy
# Incluye login, registro, logout y panel de administración con creación/eliminación de usuarios

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# -------------------------------
# 1. Cargar variables de entorno
# -------------------------------
# Usamos dotenv para leer las variables desde el archivo .env
load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")  # URI de conexión a PostgreSQL
SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-dev")  # Clave para sesiones

# -------------------------------
# 2. Configuración de Flask
# -------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = SECRET_KEY

# Inicializamos SQLAlchemy
db = SQLAlchemy(app)

# -------------------------------
# 3. Modelo de Usuario
# -------------------------------
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="cliente")  # cliente o admin

# -------------------------------
# 4. Ruta principal
# -------------------------------
@app.route("/")
def index():
    return render_template("base.html")

# -------------------------------
# 5. Registro de usuario
# -------------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        # Validamos si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            flash("El email ya está registrado.", "warning")
            return redirect(url_for("registro"))

        # Creamos nuevo usuario con contraseña encriptada
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password),
            rol="cliente"
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Registro exitoso. Ahora podés iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")

# -------------------------------
# 6. Login
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.password, password):
            session["usuario_id"] = usuario.id
            flash("Login exitoso.", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenciales inválidas.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# -------------------------------
# 7. Logout
# -------------------------------
@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("index"))

# -------------------------------
# 8. Panel de administración
# -------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    # Validamos que haya sesión
    if "usuario_id" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("login"))

    usuario = Usuario.query.get(session["usuario_id"])
    if usuario.rol != "admin":
        flash("No tienes permisos para acceder al panel de administración.", "danger")
        return redirect(url_for("index"))

    # Crear usuario desde el formulario
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        rol = request.form["rol"]

        if Usuario.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "warning")
        else:
            nuevo = Usuario(
                nombre=nombre,
                email=email,
                password=generate_password_hash(password),
                rol=rol
            )
            db.session.add(nuevo)
            db.session.commit()
            flash("Usuario creado correctamente.", "success")

    usuarios = Usuario.query.all()
    return render_template("admin_dashboard.html", usuarios=usuarios)

# -------------------------------
# 9. Eliminar usuario
# -------------------------------
@app.route("/admin/eliminar/<int:usuario_id>", methods=["POST"])
def eliminar_usuario(usuario_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("login"))

    usuario = Usuario.query.get(session["usuario_id"])
    if usuario.rol != "admin":
        flash("No tienes permisos para esta acción.", "danger")
        return redirect(url_for("index"))

    usuario_a_eliminar = Usuario.query.get(usuario_id)
    if usuario_a_eliminar:
        db.session.delete(usuario_a_eliminar)
        db.session.commit()
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("Usuario no encontrado.", "warning")

    return redirect(url_for("admin_dashboard"))

# -------------------------------
# 10. Ejecutar app y crear tablas
# -------------------------------
# En Flask 3.x ya no existe @app.before_first_request
# Por eso usamos app.app_context() al inicio
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # crea las tablas si no existen
    app.run(debug=True)