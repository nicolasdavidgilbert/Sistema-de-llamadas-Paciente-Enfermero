from flask import Blueprint, request, jsonify, render_template, send_file
from models import db, Habitacion, Cama, Llamada, Presencia, Asistente
from datetime import datetime, timedelta
import logging
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from flask import send_file

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/admin/", methods=["GET"])
@admin_routes.route("/admin", methods=["GET"])
def index():
    return render_template("admin/index.html"),200

@admin_routes.route("/admin/asistencias", methods=['GET'])
def ver_llamadas():
    ahora = datetime.now()
    hace_24h = ahora - timedelta(hours=24)
    llamadas = Llamada.query.filter(Llamada.fecha >= hace_24h).all()
    return render_template("admin/llamadas.html", llamadas=llamadas), 200


@admin_routes.route('/admin/asistentes', methods=['GET'])
def ver_asistentes():
    asistentes = Asistente.query.all()
    return render_template('admin/asistentes.html', asistentes=asistentes), 200



@admin_routes.route('/admin/asistente-nuevo', methods=['POST'])
def asistente_nuevo():
    data = request.get_json()
    
    # Validar existencia de datos requeridos
    if not data or not all(k in data for k in ('nombre', 'telefono', 'password')):
        return jsonify({"error": "Faltan datos"}), 400

    nombre = data['nombre'].strip()
    telefono = data['telefono'].strip()
    codigo = data['password'].strip()

    # Validar longitud del código
    if len(codigo) > 6:
        return jsonify({"error": "El código debe tener como máximo 6 caracteres."}), 400

    # Validar formato del teléfono (9 dígitos)
    if not telefono.isdigit() or len(telefono) != 9:
        return jsonify({"error": "El teléfono debe tener 9 dígitos numéricos."}), 400

    # Comprobar si ya existe ese código
    if Asistente.query.filter_by(codigo=codigo).first():
        return jsonify({"error": "El código ya está en uso. Usa otro."}), 400

    nuevo_asistente = Asistente(
        nombre=nombre,
        tlf=telefono,
        codigo=codigo  # En producción, debería almacenarse con hash si es clave real
    )

    db.session.add(nuevo_asistente)
    db.session.commit()

    return jsonify({"mensaje": "Asistente creado correctamente", "id": nuevo_asistente.id}), 201


@admin_routes.route('/admin/eliminar_asistentes', methods=['POST'])
def eliminar_asistentes():
    ''':list'''
    ids = request.get_json() 
    for asistente_id in ids:
        asistente = Asistente.query.get(asistente_id)
        if asistente:
            db.session.delete(asistente)
    db.session.commit()
    return jsonify({"mensaje": "Asistentes eliminados correctamente", "ids": ids}), 200



@admin_routes.route('/admin/updatear_asistentes', methods=['POST'])
def updatear_asistentes():
    ''':list''' 
    lista_asistentes = request.get_json()

    for asistente_data in lista_asistentes:
        id = asistente_data.get('id')
        nombre = asistente_data.get('nombre')
        telefono = asistente_data.get('telefono')
        codigo = asistente_data.get('codigo')

        asistente = Asistente.query.get(id)
        if asistente:
            asistente.nombre = nombre
            asistente.tlf = telefono
            asistente.codigo = codigo

    db.session.commit()
    ids_actualizados = [i.get("id") for i in lista_asistentes]
    return jsonify({"mensaje": "Asistentes updateados correctamente", "ids": ids_actualizados}), 200

@admin_routes.route('/admin/llamadas/csv', methods=['GET'])
def exportar_csv():
    try:
        nombre_archivo = "registro_llamadas.csv"
        encabezados = [
            "habitacion", "cama", "fecha_llamada",
            "estado_llamada", "fecha_aceptacion","fecha_presencia",
            "nombre_asistente", "telefono_asistente"
        ]

        llamadas = Llamada.query.all()

        with open(nombre_archivo, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(encabezados)

            for l in llamadas:
                cama = Cama.query.get(l.cama_id)
                habitacion = Habitacion.query.get(cama.habitacion_id)
                presencia = Presencia.query.filter_by(llamada_id=l.id).first()
                asistente = Asistente.query.get(l.asistente_id) if l.asistente_id else None

                writer.writerow([
                    habitacion.numero,
                    cama.letra,
                    l.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    l.estado,
                    l.fecha_aceptacion.strftime("%Y-%m-%d %H:%M:%S") if l.fecha_aceptacion else "",
                    presencia.fecha_presencia.strftime("%Y-%m-%d %H:%M:%S") if presencia else "",
                    asistente.nombre if asistente else "",
                    asistente.tlf if asistente else ""
                    
                ])

        return send_file(nombre_archivo, as_attachment=True)

    except Exception as e:
        logging.error(f"❌ Error al exportar CSV: {e}")
        return jsonify({"error": "Error al exportar CSV"}), 500
    


@admin_routes.route('/admin/llamadas/pdf', methods=['GET'])
def exportar_pdf():
    try:
        nombre_pdf = "registro_llamadas.pdf"
        llamadas = Llamada.query.all()

        data = [[
            "Habitación", "Cama", "Fecha Llamada",
            "Estado", "Fecha Aceptación", "Fecha Presencia",
            "Nombre Asistente", "Teléfono Asistente"
        ]]

        for l in llamadas:
            cama = Cama.query.get(l.cama_id)
            habitacion = Habitacion.query.get(cama.habitacion_id)
            asistente = Asistente.query.get(l.asistente_id) if l.asistente_id else None
            presencia = Presencia.query.filter_by(llamada_id=l.id).first()

            data.append([
                str(habitacion.numero),
                cama.letra,
                l.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                l.estado,
                l.fecha_aceptacion.strftime("%Y-%m-%d %H:%M:%S") if l.fecha_aceptacion else "Sin aceptar",
                presencia.fecha_presencia.strftime("%Y-%m-%d %H:%M:%S") if presencia else "Sin presencia",
                asistente.nombre if asistente else "N/A",
                asistente.tlf if asistente else "N/A"
            ])

        # Crear PDF
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        width, height = A4

        tabla = Table(data, colWidths=[55, 35, 85, 55, 85, 85, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007acc")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ]))

        # Calcular tamaño de tabla
        ancho_tabla, alto_tabla = tabla.wrap(0, 0)
        x = (width - ancho_tabla) / 2
        y = height - 40 - alto_tabla

        tabla.drawOn(c, x, y)
        c.save()


        return send_file(nombre_pdf, as_attachment=True)

    except Exception as e:
        logging.error(f"❌ Error al exportar PDF: {e}")
        return jsonify({"error": "Error al exportar PDF"}), 500

