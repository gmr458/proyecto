CREATE TABLE `usuario` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `numero_documento` varchar(255) UNIQUE NOT NULL,
  `code_country` varchar(255) NOT NULL,
  `phone_number` varchar(255) UNIQUE NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT (now()),
  `activado` boolean NOT NULL DEFAULT true,
  `eliminado` boolean NOT NULL DEFAULT false
);

CREATE TABLE `tarea` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `prioridad` ENUM ('baja', 'media', 'alta') NOT NULL,
  `tipo_id` integer NOT NULL,
  `empleado_id` integer NOT NULL,
  `creador_id` integer NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT (now()),
  `fecha_limite` timestamp NOT NULL,
  `evidencia` varchar(255),
  `estado` ENUM ('sin_iniciar', 'en_proceso', 'ejecutada') NOT NULL DEFAULT "sin_iniciar",
  `eliminado` boolean NOT NULL DEFAULT false
);

CREATE TABLE `tipo_tarea` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) UNIQUE NOT NULL,
  `descripcion` varchar(255)
);

INSERT INTO `tipo_tarea` (`nombre`)
VALUES
  ('quimico'),
  ('agua'),
  ('aire'),
  ('reciclaje');

CREATE TABLE `observacion` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `tarea_id` integer NOT NULL,
  `creador_id` integer NOT NULL,
  `contenido` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT (now()),
  `eliminado` boolean NOT NULL DEFAULT false
);

CREATE TABLE `rol` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) UNIQUE NOT NULL,
  `descripcion` varchar(255)
);

INSERT INTO `rol` (`nombre`)
VALUES
  ('administrador'),
  ('empleado');

CREATE TABLE `roles_usuario` (
  `usuario_id` integer NOT NULL,
  `rol_id` integer NOT NULL,
  PRIMARY KEY (`usuario_id`, `rol_id`)
);

CREATE TABLE `atributo` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` varchar(255)
);

CREATE TABLE `atributos_usuario` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `usuario_id` integer NOT NULL,
  `atributo_id` integer NOT NULL,
  `valor` varchar(255) NOT NULL
);

ALTER TABLE `roles_usuario` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);
ALTER TABLE `roles_usuario` ADD FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);

ALTER TABLE `tarea` ADD FOREIGN KEY (`tipo_id`) REFERENCES `tipo_tarea` (`id`);
ALTER TABLE `tarea` ADD FOREIGN KEY (`empleado_id`) REFERENCES `usuario` (`id`);
ALTER TABLE `tarea` ADD FOREIGN KEY (`creador_id`) REFERENCES `usuario` (`id`);

ALTER TABLE `observacion` ADD FOREIGN KEY (`tarea_id`) REFERENCES `tarea` (`id`);
ALTER TABLE `observacion` ADD FOREIGN KEY (`creador_id`) REFERENCES `usuario` (`id`);

ALTER TABLE `atributos_usuario` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);
ALTER TABLE `atributos_usuario` ADD FOREIGN KEY (`atributo_id`) REFERENCES `atributo` (`id`);
