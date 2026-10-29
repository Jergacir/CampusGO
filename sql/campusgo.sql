DROP DATABASE IF EXISTS campusgo;
CREATE DATABASE campusgo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE campusgo;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    foto VARCHAR(255) NULL,
    foto_url VARCHAR(500) NULL,
    foto_public_id VARCHAR(255) NULL,
    rol ENUM('PASAJERO','CONDUCTOR','ADMINISTRADOR') NOT NULL,
    estado ENUM('ACTIVO','INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pasajero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE conductor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    licencia VARCHAR(30),
    calificacion DECIMAL(3,2) DEFAULT 0,
    marca_auto VARCHAR(80) NULL,
    modelo_auto VARCHAR(80) NULL,
    placa_auto VARCHAR(20) NULL,
    color_auto VARCHAR(40) NULL,
    foto_auto_url VARCHAR(500) NULL,
    foto_auto_public_id VARCHAR(255) NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conductor_id INT NOT NULL,
    origen VARCHAR(150) NOT NULL,
    destino VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    cupos INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    marca_auto VARCHAR(80) NULL,
    modelo_auto VARCHAR(80) NULL,
    placa_auto VARCHAR(20) NULL,
    color_auto VARCHAR(40) NULL,
    foto_auto_url VARCHAR(500) NULL,
    estado ENUM('DISPONIBLE','COMPLETO','FINALIZADO','CANCELADO') NOT NULL DEFAULT 'DISPONIBLE',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conductor_id) REFERENCES conductor(id)
);

CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pasajero_id INT NOT NULL,
    estado ENUM('CONFIRMADA','PARCIAL','CANCELADA') NOT NULL DEFAULT 'CONFIRMADA',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pasajero_id) REFERENCES pasajero(id)
);

CREATE TABLE reserva_viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    viaje_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    tipo_tramo ENUM('IDA','RETORNO') NOT NULL,
    orden_tramo INT NOT NULL DEFAULT 1,
    estado ENUM('CONFIRMADA','CANCELADA') NOT NULL DEFAULT 'CONFIRMADA',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reserva(id),
    FOREIGN KEY (viaje_id) REFERENCES viaje(id),
    UNIQUE (reserva_id, viaje_id)
);
