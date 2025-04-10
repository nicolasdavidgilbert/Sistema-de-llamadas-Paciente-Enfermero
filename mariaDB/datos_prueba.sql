USE paciente_enfermero;

-- 🔹 Habitaciones
INSERT INTO habitaciones (planta, numero) VALUES (1, 101);
INSERT INTO habitaciones (planta, numero) VALUES (1, 102);
INSERT INTO habitaciones (planta, numero) VALUES (1, 103);

-- 🔹 Camas para cada habitación (4 camas por habitación)
-- Habitación 101
INSERT INTO camas (habitacion_id, letra) VALUES (1, 'A'), (1, 'B'), (1, 'C'), (1, 'D');
-- Habitación 102
INSERT INTO camas (habitacion_id, letra) VALUES (2, 'A'), (2, 'B'), (2, 'C'), (2, 'D');
-- Habitación 103
INSERT INTO camas (habitacion_id, letra) VALUES (3, 'A'), (3, 'B'), (3, 'C'), (3, 'D');

-- 🔹 Asistentes
INSERT INTO asistentes (nombre, tlf, codigo) VALUES 
('Ana López', '612345678', 'A12345'),
('Carlos Ruiz', '622345679', 'B67890'),
('María Pérez', '632345680', 'C13579'),
('Juan Gómez', '642345681', 'D24680'),
('Elena Torres', '652345682', 'E11111'),
('Luis Sánchez', '662345683', 'F22222');
