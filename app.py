import json
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

app = Flask(__name__)

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIOS = os.path.join(CARPETA, "usuarios.json")


def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return []
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    error = None

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        cumpleanos = request.form["cumpleanos"]
        password = request.form["password"]
        color = request.form["color"]

        usuarios = cargar_usuarios()

        if any(u["nombre"].lower() == nombre.lower() for u in usuarios):
            error = "Ese nombre ya está en uso, elige otro."
        elif len(password) < 4:
            error = "La contraseña debe tener al menos 4 caracteres."
        else:
            usuarios.append({
                "nombre": nombre,
                "cumpleanos": cumpleanos,
                "password": generate_password_hash(password),
                "color": color,
            })
            guardar_usuarios(usuarios)
            return redirect(url_for("inicio"))

    return render_template("registro.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)