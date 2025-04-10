# 🏥 Sistema de Llamadas Paciente-Enfermero

Este proyecto implementa un sistema de asistencia en habitaciones hospitalarias, permitiendo que los pacientes llamen al personal sanitario mediante pulsadores. A su vez, los asistentes pueden aceptar las llamadas, registrar su presencia y consultar historiales mediante un entorno web.

## 📦 Estructura del Proyecto

```
.
├── docker
│   └── docker-compose.yml
├── mariaDB
│   ├── crear_tablas.sql
│   └── datos_prueba.sql
├── nginx
│   └── paciente_enfermero
├── program
│   ├── admin_routes.py
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── log.txt
│   ├── models.py
│   ├── por-hcer.txt
│   ├── prueba-pushover.py
│   ├── __pycache__  [error opening dir]
│   ├── registro_llamadas.csv
│   ├── registro_llamadas.pdf
│   ├── requirements.txt
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   ├── 404.css
│   │   │   ├── ack.css
│   │   │   ├── admin
│   │   │   │   ├── asistentes.css
│   │   │   │   └── llamadas.css
│   │   │   ├── api.css
│   │   │   ├── desenrolado.css
│   │   │   ├── enrolado.css
│   │   │   ├── enroll.css
│   │   │   ├── error_404.css
│   │   │   ├── habitacion.css
│   │   │   └── listado.css
│   │   ├── favicon
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon.ico
│   │   │   └── site.webmanifest
│   │   ├── favicon.ico
│   │   ├── favicon.png
│   │   ├── img
│   │   │   └── doctor.png
│   │   └── js
│   │       ├── admin
│   │       │   └── añadir-asistente.js
│   │       ├── enroll.js
│   │       ├── habitacion.js
│   │       └── listado.js
│   └── web
│       ├── 404.html
│       ├── ack.html
│       ├── admin
│       │   ├── asistentes.html
│       │   ├── index.html
│       │   └── llamadas.html
│       ├── desenrolado.html
│       ├── enrolado.html
│       ├── enroll.html
│       ├── error_404.html
│       ├── habitacion.html
│       ├── index.html
│       ├── listado.html
│       ├── prueba_error_404.css
│       └── prueba_error_404.html
├── README.md
├── scripts
│   ├── start-gunicorn.sh
│   └── start-services.sh
└── sounds
    └── red-alert_nuclear_buzzer-99741.mp3
```

## 🚀 Instrucciones de Uso

### 1. 📥 Requisitos Previos

- Docker y Docker Compose instalados.
- Red wifi operativa para pulsadores y relés.
- Cuenta en [Pushover](https://pushover.net) con licencia activa o en prueba.

### 2. ▶️ Arranque del Sistema PARA DESARROLLO
#### Todavía no está para producción

Desde la carpeta `docker/` ejecutar:

```bash
docker-compose up -d
```

Esto iniciará:
- El servidor Nginx.
- La base de datos MariaDB.

Luego, para iniciar el servidor:
- docker exec -it sistema-llamadasv2 /bin/bash
    Dentro del contenedor
    - Para inicar el entorno virtual:
    ```bash
    cd program
    source .venv/bin/activate
    ```
    - Para iniciar gunicorn:
    ```bash
    ./../scripts/start-gunicorn.sh
    ```
- El servicio web accesible en: `http://localhost:8080`

### 3. 🧪 Simulación de Llamadas

Usa un navegador o un pulsador WiFi configurado para enviar peticiones HTTP:

- Nueva llamada:  
  ```
  GET http://localhost:8080/llamada/104/b
  ```
- Confirmar presencia:  
  ```
  GET http://localhost:8080/presencia/104/b
  ```

### 4. 🔐 Autenticación y Enrolamiento

- Enrolar un terminal (introducir código de asistente):  
  ```
  http://localhost:8080/enroll
  ```

- Desenrolar (cerrar sesión):  
  ```
  http://localhost:8080/desenroll
  ```

> Los asistentes deben enrolarse para que sus acciones se registren correctamente.

### 5. 📋 Gestión desde el Portal Web

- Gestión de asistentes y llamadas:  
  ```
  http://localhost:8080/admin
  ```
  (Requiere autenticación HTTP básica)

- Visualización de llamadas últimas 24h:  
  ```
  http://localhost:8080/admin/llamadas
  ```

- Visualización y edición de los asistentes:  
  ```
  http://localhost:8080/admin/asistentes
  ```

- Exportación:  
  - CSV: `/admin/llamadas/csv`
  - PDF: `/admin/llamadas/pdf`

## 🔊 Notificaciones Push (Pushover)

Cada llamada genera una notificación push al móvil del asistente con:
- Mensaje de alerta.
- Enlace para aceptar la asistencia.
- Sonido personalizado. (carpeta sounds)
- Petición de ACK (confirmación).

Configurado en el archivo `.env`:

```env
IP=localhost
USER=tu_user_de_pushover
TOKEN=tu_token_de_aplicacion
```

## 🗄️ Base de Datos

- Motor: MariaDB
- Script de creación: `mariaDB/crear_tablas.sql`
- Datos de prueba: `mariaDB/datos_prueba.sql`

## 🧰 Tecnologías

- Python 3 + Flask + SQLAlchemy
- Gunicorn
- Nginx
- MariaDB
- Docker
- Pushover API

## 👨‍🔧 Autor

Proyecto desarrollado como trabajo final de grado superior.  
El sistema está preparado para entornos reales con múltiples habitaciones, asistentes y terminales móviles.