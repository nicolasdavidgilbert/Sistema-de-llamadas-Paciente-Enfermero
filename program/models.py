from database import db
from datetime import datetime


class Habitacion(db.Model):
    __tablename__ = 'habitaciones'
    id = db.Column(db.Integer, primary_key=True)
    planta = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    camas = db.relationship('Cama', backref='habitacion', lazy=True)


class Cama(db.Model):
    __tablename__ = 'camas'
    id = db.Column(db.Integer, primary_key=True)
    ip_rele = db.Column(db.String(15), nullable=False)  # Added 'ip_rele' field
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitaciones.id'), nullable=False)
    letra = db.Column(db.String(1), nullable=False)
    llamadas = db.relationship('Llamada', backref='cama', lazy=True)


class Asistente(db.Model):
    __tablename__ = 'asistentes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tlf = db.Column(db.String(9), nullable=False)
    codigo = db.Column(db.String(6), unique=True, nullable=False)
    llamadas = db.relationship('Llamada', backref='asistente', lazy=True)

    @property
    def num_llamadas(self):
        return len(self.llamadas)


class Llamada(db.Model):
    __tablename__ = 'llamadas'
    id = db.Column(db.Integer, primary_key=True)
    cama_id = db.Column(db.Integer, db.ForeignKey('camas.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    fecha_aceptacion = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.Enum('pendiente', 'atendida', 'presente', name='estado_llamada'), default='pendiente')
    asistente_id = db.Column(db.Integer, db.ForeignKey('asistentes.id'), nullable=True)
    presencia = db.relationship('Presencia', backref='llamada', uselist=False)


class Presencia(db.Model):
    __tablename__ = 'presencias'
    id = db.Column(db.Integer, primary_key=True)
    llamada_id = db.Column(db.Integer, db.ForeignKey('llamadas.id'), nullable=False)
    fecha_presencia = db.Column(db.DateTime, nullable=False)
