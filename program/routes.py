from flask import Blueprint, request, jsonify, redirect, make_response, render_template_string, Flask, render_template, send_from_directory, url_for
import requests
from models import db, Habitacion, Cama, Llamada, Presencia, Asistente
from datetime import datetime
import logging
import os
import csv
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env
URL_BASE = os.getenv("URL_BASE")
USER = os.getenv("USER")
TOKEN = os.getenv("TOKEN")


routes = Blueprint("routes", __name__)
app = Flask(__name__, template_folder='web')


@routes.route('/habitacion/<int:habitacion>/<string:cama>')
def habitacion(habitacion, cama):
    # Verificar si la cama existe realmente en la base de datos
    habitacion_obj = Habitacion.query.filter_by(numero=habitacion).first()
    if not habitacion_obj:
        return render_template("error_404.html", mensaje="Habitación no encontrada"), 404

    cama_obj = Cama.query.filter_by(habitacion_id=habitacion_obj.id, letra=cama.lower()).first()
    if not cama_obj:
        return render_template("error_404.html", mensaje="Cama no encontrada en esta habitación"), 404

    return render_template("habitacion.html",
                           habitacion=habitacion,
                           cama=cama)

@routes.route("/habitaciones")
def listado_habitaciones():
    # Consultar habitaciones y camas existentes
    habitaciones = Habitacion.query.all()
    datos = []

    for h in habitaciones:
        camas = Cama.query.filter_by(habitacion_id=h.id).all()
        for c in camas:
            datos.append({
                "habitacion": h.numero,
                "cama": c.letra
            })

    return render_template("listado.html", camas=datos)


@routes.route("/estado/<int:habitacion>/<string:cama>", methods=["GET"])
def estado_cama(habitacion, cama):
    try:
        habit = Habitacion.query.filter_by(numero=habitacion).first()
        cama_obj = Cama.query.filter_by(habitacion_id=habit.id, letra=cama).first()
        llamada = Llamada.query.filter_by(cama_id=cama_obj.id).order_by(Llamada.fecha.desc()).first()

        if not llamada:
            return jsonify({"estado": "sin_llamada"})

        return jsonify({"estado": llamada.estado})
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)})
    
@routes.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@routes.app_errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


@routes.route("/", methods=["GET"])
def index():
    return render_template("index.html"),200

# 🔴 1. Registrar nueva llamada
@routes.route("/llamada/<int:habitacion>/<string:cama>", methods=["GET"])
def nueva_llamada(habitacion, cama):
    try:
        habit = Habitacion.query.filter_by(numero=habitacion).first()
        if not habit:
            return render_template("error_404.html", mensaje="Habitación no encontrada"), 404


        cama_obj = Cama.query.filter_by(habitacion_id=habit.id, letra=cama).first()
        if not cama_obj:
            return render_template("error_404.html", mensaje="Cama no encontrada en esta habitación"), 404
        

        nueva = Llamada(cama_id=cama_obj.id)
        db.session.add(nueva)
        db.session.commit()

        mensaje = f"Solicitud de asistencia en habitación <b><font color='#ff0000'>{habitacion}</font></b> y cama <b><font color='#ff0000'>{cama}</font></b>."
        enlace_aceptar = f"{URL_BASE}/aceptar/{habitacion}/{cama}"
        url = "https://api.pushover.net/1/messages.json"
        data = {
            "token": TOKEN,
            "user": USER,
            "message": mensaje,
            "priority": 2,
            "sound": "alerta",
            "retry": 30,
            "expire": 180,
            "html": 1,
            "title": "Llamada de asistencia",
            "url": enlace_aceptar,
            "url_title": "Atender solicitud de asistencia"
        }
        requests.post(url, data=data)


        return jsonify({"message": "✅ Llamada registrada exitosamente"}), 201
    except Exception as e:
        logging.error(f"❌ Error al registrar llamada: {e}")
        return jsonify({"error": "Error al registrar llamada"}), 500


# 🟡 2. Aceptar llamada (por un asistente con código desde cookie)
@routes.route("/aceptar/<int:habitacion>/<string:cama>", methods=["GET"])
def aceptar_llamada(habitacion, cama):
    try:
        codigo_asistente = request.cookies.get('asistente')
        if not codigo_asistente:
            return redirect(url_for("routes.enroll_aceptar", habitacion=habitacion, cama=cama))
        
        habit = Habitacion.query.filter_by(numero=habitacion).first()
        cama_obj = Cama.query.filter_by(habitacion_id=habit.id, letra=cama).first()
        llamada = Llamada.query.filter_by(cama_id=cama_obj.id, estado='pendiente').order_by(Llamada.fecha.desc()).first()
        if not llamada:
            return jsonify({"error": "No hay llamada pendiente"}), 404

        asistente = Asistente.query.filter_by(codigo=codigo_asistente).first()
        if not asistente:
            return jsonify({"error": "Asistente no válido"}), 403
            

        llamada.estado = 'atendida'
        llamada.fecha_aceptacion = datetime.now()
        llamada.asistente_id = asistente.id
        db.session.commit()

        # Encender el relay asociado a la cama
        try:
            ip_rele = cama_obj.ip_rele  # Obtener la IP del relé asociado a la cama
            url = f"http://{ip_rele}/relay/0?turn=on"
            response = requests.get(url)
            if response.status_code != 200:
                logging.warning(f"⚠️ No se pudo encender el relay para la cama {cama} en la habitación {habitacion}")
        except Exception as e:
            logging.error(f"❌ Error al intentar encender el relay: {e}")

        return render_template("ack.html"), 200

    except Exception as e:
        logging.error(f"❌ Error al aceptar llamada: {e}")
        return jsonify({"error": "Error al aceptar llamada"}), 500


# 🟢 3. Registrar presencia física
@routes.route("/presencia/<int:habitacion>/<string:cama>", methods=["GET"])
def registrar_presencia(habitacion, cama):
    try:
        habit = Habitacion.query.filter_by(numero=habitacion).first()
        cama_obj = Cama.query.filter_by(habitacion_id=habit.id, letra=cama).first()
        llamada = Llamada.query.filter_by(cama_id=cama_obj.id, estado='atendida').order_by(Llamada.fecha.desc()).first()

        if not llamada:
            return jsonify({"error": "No hay llamada atendida"}), 404

        nueva_presencia = Presencia(llamada_id=llamada.id, fecha_presencia=datetime.now())
        llamada.estado = 'presente'

        db.session.add(nueva_presencia)
        db.session.commit()

        # Apagar el relay asociado a la cama
        try:
            ip_rele = cama_obj.ip_rele  # Obtener la IP del relé asociado a la cama
            url = f"http://{ip_rele}/relay/0?turn=off"
            response = requests.get(url)
            if response.status_code != 200:
                logging.warning(f"⚠️ No se pudo apagar el relay para la cama {cama} en la habitación {habitacion}")
        except Exception as e:
            logging.error(f"❌ Error al intentar apagar el relay: {e}")

        return jsonify({"message": "✅ Presencia registrada exitosamente"}), 200
    except Exception as e:
        logging.error(f"❌ Error al registrar presencia: {e}")
        return jsonify({"error": "Error al registrar presencia"}), 500


@routes.route("/enroll_aceptar", methods=["GET", "POST"])
def enroll_aceptar():
    error = None
    habitacion = request.args.get("habitacion")
    cama = request.args.get("cama")

    if request.method == "POST":
        codigo = request.form.get("codigo")
        habitacion = request.form.get("habitacion")
        cama = request.form.get("cama")
        asistente = Asistente.query.filter_by(codigo=codigo).first()

        if not asistente:
            error = "❌ Código de asistente no válido"
        else:
            response = redirect(url_for("routes.aceptar_llamada", habitacion=habitacion, cama=cama))
            response.set_cookie("asistente", codigo)
            return response

    return render_template("enroll.html", error=error, habitacion=habitacion, cama=cama)



@routes.route("/enroll", methods=["GET", "POST"])
def enroll():
    error = None

    if request.method == "POST":
        codigo = request.form.get("codigo")
        asistente = Asistente.query.filter_by(codigo=codigo).first()

        if not asistente:
            error = "❌ Código de asistente no válido"
        else:
            response = make_response(render_template("enrolado.html", codigo=codigo))
            response.set_cookie("asistente", codigo)
            return response

    return render_template("enroll.html", error=error)



@routes.route("/desenroll")
def desenroll():
    response = make_response(render_template("desenrolado.html"))
    response.delete_cookie("asistente")
    return response

@routes.route("/<string:ip>/relay/0", methods=["GET"])
def enceder_apagar_relay(ip):
    try:
        estado = request.args.get("turn")  # Captura el parámetro de consulta 'turn'
        if not estado:
            return jsonify({"error": "Falta el parámetro 'turn'"}), 400

        url = f"http://{ip}/relay/0?turn={estado}"
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify({"message": "✅ Estado del relay actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Error al actualizar el estado del relay"}), 500
    except Exception as e:
        logging.error(f"❌ Error al encender/apagar relay: {e}")
        return jsonify({"error": "Error al encender/apagar relay"}), 500


