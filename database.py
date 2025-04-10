from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

# Configurar logging para registrar errores
logging.basicConfig(filename=Config.LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

db = SQLAlchemy()

def init_db(app):
    """Inicializa la base de datos con Flask"""
    try:
        app.config.from_object(Config)
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("✅ Base de datos conectada y tablas creadas correctamente.")
    except Exception as e:
        logging.error(f"❌ Error al conectar la base de datos: {e}")
        print("❌ Error al conectar la base de datos. Revisa el archivo log.txt")
