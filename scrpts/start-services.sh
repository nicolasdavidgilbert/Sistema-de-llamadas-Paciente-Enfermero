#!/bin/bash

echo "🚀 Iniciando servicios Nginx y MariaDB..."

# Iniciar MariaDB directamente
echo "⏳ Iniciando MariaDB..."
mysqld_safe &

# Esperar unos segundos para que inicie correctamente
sleep 5

# Verificar si MariaDB está corriendo
if pgrep mysqld > /dev/null; then
    echo "✅ MariaDB iniciado correctamente."
else
    echo "❌ Error al iniciar MariaDB."
fi

# Iniciar Nginx
service nginx start

# Verificar estado de Nginx
if pgrep nginx > /dev/null; then
    echo "✅ Nginx iniciado correctamente."
else
    echo "❌ Error al iniciar Nginx."
fi

cd ..
source .venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# if [ $? -eq 0 ]; then
#     echo "✅ Aplicación iniciada correctamente con Gunicorn."
# else
#     echo "❌ Error al iniciar la aplicación Flask con Gunicorn."
#     exit 1
# fi


# Mostrar procesos
# echo "📋 Servicios en ejecución:"
# ps aux | grep -E 'nginx|mysqld' | grep -v grep
