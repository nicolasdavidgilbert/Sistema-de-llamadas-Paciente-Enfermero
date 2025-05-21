USE paciente_enfermero;

-- 🔹 Habitaciones
INSERT INTO habitaciones (planta, numero) VALUES (1, 101);
INSERT INTO habitaciones (planta, numero) VALUES (1, 102);
INSERT INTO habitaciones (planta, numero) VALUES (1, 103);

-- 🔹 Camas para cada habitación (4 camas por habitación)
-- Habitación 101
INSERT INTO camas (habitacion_id, letra, ip_rele) VALUES 
(1, 'A', '127.0.100.1'),
(1, 'B', '127.0.100.2'),
(1, 'C', '127.0.100.3'),
(1, 'D', '127.0.100.4');
-- Habitación 102
INSERT INTO camas (habitacion_id, letra, ip_rele) VALUES 
(2, 'A', '127.0.100.5'),
(2, 'B', '127.0.100.6'),
(2, 'C', '127.0.100.7'),
(2, 'D', '127.0.100.8');
-- Habitación 103
INSERT INTO camas (habitacion_id, letra, ip_rele) VALUES 
(3, 'A', '127.0.100.9'),
(3, 'B', '127.0.100.10'),
(3, 'C', '127.0.100.11'),
(3, 'D', '127.0.100.12');

-- 🔹 Asistentes
INSERT INTO asistentes (nombre, tlf, codigo) VALUES 
('Ana López', '612345678', 'A12345'),
('Carlos Ruiz', '622345679', 'B67890'),
('María Pérez', '632345680', 'C13579'),
('Juan Gómez', '642345681', 'D24680'),
('Elena Torres', '652345682', 'E11111'),
('Luis Sánchez', '662345683', 'F22222');
