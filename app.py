from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import routes
from admin_routes import admin_routes

# 🔧 Añade el parámetro template_folder
app = Flask(__name__, template_folder='web')
CORS(app, supports_credentials=True)

init_db(app)

# Registrar rutas
app.register_blueprint(routes)
app.register_blueprint(admin_routes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
