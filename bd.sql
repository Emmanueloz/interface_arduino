CREATE DATABASE IF NOT EXISTS arduino_bd;

use arduino_bd;

CREATE TABLE IF NOT EXISTS componentes(
    idComponente INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    nombre VARCHAR(50),
    descripcion VARCHAR(100)
)

CREATE TABLE IF NOT EXISTS registros(
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    idComponente INT UNSIGNED,
    valor FLOAT,
    fecha DATE,
    hora TIME
)
