#!/bin/bash

# Instalar dependencias
apt update
apt install -y nginx mariadb-server apache2-utils python3 python3-venv net-tools

echo "🚀 Iniciando servicios para simular máquina virtual Ubuntu..."

# Iniciar MariaDB
echo "⏳ Iniciando MariaDB..."
mysqld_safe &
sleep 5

# Verificar si MariaDB está corriendo
if netstat -tulnp | grep :3306 > /dev/null; then
    echo "✅ MariaDB iniciado correctamente."
else
    echo "❌ Error al iniciar MariaDB."
    exit 1
fi

# Crear usuario admin con permisos si no existe
echo "👤 Creando usuario MariaDB..."
mariadb -e "CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin'; GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION; FLUSH PRIVILEGES;"

# Ejecutar los scripts SQL
echo "🗂️ Ejecutando scripts SQL..."
if [ -f /mariaDB/crear_tablas.sql ] && [ -f /mariaDB/datos_prueba.sql ]; then
    mariadb -u admin -padmin < /mariaDB/crear_tablas.sql
    mariadb -u admin -padmin < /mariaDB/datos_prueba.sql
    echo "✅ Scripts SQL ejecutados correctamente."
else
    echo "❌ Error: Los archivos SQL no existen en /mariaDB."
    exit 1
fi

# Asegurar que /etc/nginx/sites-enabled existe
mkdir -p /etc/nginx/sites-enabled

# Limpiar configuración por defecto de nginx
rm -f /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Crear enlace simbólico del archivo de configuración personalizado
if [ -f /etc/nginx/sites-available/paciente_enfermero ]; then
    ln -sf /etc/nginx/sites-available/paciente_enfermero /etc/nginx/sites-enabled/
    echo "✅ Configuración de Nginx establecida."
else
    echo "❌ Error: El archivo /etc/nginx/sites-available/paciente_enfermero no existe."
    exit 1
fi

# Configurar autenticación básica
echo "🔐 Configurando autenticación básica..."
htpasswd -bc /etc/nginx/.htpasswd_usuarios user user
htpasswd -bc /etc/nginx/.htpasswd_admin admin admin

# Ejecutar comandos de Python
echo "🐍 Configurando entorno Python..."
if [ ! -d /program ]; then
    echo "❌ Error: El directorio ../program no existe."
    exit 1
fi
cd /program
if [ ! -f requirements.txt ]; then
    echo "❌ Error: requirements.txt no existe en /program."
    exit 1
fi
echo "Tu ip y los tockens" /program/.env
python3 -m venv .venv
source .venv/bin/activate
pip install -r /program/requirements.txt
deactivate
echo "✅ Dependencias de Python instaladas."

# Lanzar Nginx en primer plano (proceso principal del contenedor)
echo "📡 Sistema listo. Ejecutando Nginx en foreground..."
nginx -g "daemon off;"
