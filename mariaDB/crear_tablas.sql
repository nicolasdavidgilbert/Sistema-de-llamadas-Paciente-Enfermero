-- Crear base de datos (solo si aún no existe)
CREATE DATABASE IF NOT EXISTS paciente_enfermero;
USE paciente_enfermero;

-- Tabla: habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    planta INT NOT NULL,
    numero INT NOT NULL
);

-- Tabla: camas
CREATE TABLE IF NOT EXISTS camas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_rele VARCHAR(15) NOT NULL, -- Se añadió el campo 'ip_rele' para almacenar la IP del relé
    habitacion_id INT NOT NULL,
    letra CHAR(1) NOT NULL,
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

-- Tabla: asistentes
CREATE TABLE IF NOT EXISTS asistentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tlf VARCHAR(15) NOT NULL, -- Se añadió el campo 'tlf'
    codigo CHAR(6) UNIQUE NOT NULL
);

-- Tabla: llamadas
CREATE TABLE IF NOT EXISTS llamadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cama_id INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_aceptacion DATETIME DEFAULT NULL,
    estado ENUM('pendiente', 'atendida', 'presente') DEFAULT 'pendiente',
    asistente_id INT,
    FOREIGN KEY (cama_id) REFERENCES camas(id), -- Se corrigió para que apunte al campo 'id' de la tabla 'camas'
    FOREIGN KEY (asistente_id) REFERENCES asistentes(id)
);

-- Tabla: presencias
CREATE TABLE IF NOT EXISTS presencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    llamada_id INT NOT NULL,
    fecha_presencia DATETIME NOT NULL,
    FOREIGN KEY (llamada_id) REFERENCES llamadas(id)
);
