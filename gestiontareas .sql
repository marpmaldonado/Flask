-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-04-2024 a las 04:10:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestiontareas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `IDtarea` int(11) NOT NULL,
  `nombretar` varchar(200) NOT NULL,
  `fechainicio` date DEFAULT NULL,
  `fechafin` date DEFAULT NULL,
  `estado` enum('por asignar','en proceso','terminado') DEFAULT NULL,
  `Id_Usuario1` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`IDtarea`, `nombretar`, `fechainicio`, `fechafin`, `estado`, `Id_Usuario1`) VALUES
(9, 'Caminar', '2024-04-29', '2024-04-30', 'en proceso', 2),
(10, 'limpiar', '2024-05-01', '2024-05-02', 'por asignar', 3),
(11, 'jugar con make', '2024-05-05', '2024-05-06', 'en proceso', 2),
(12, 'besar', '2024-05-07', '2024-05-09', 'en proceso', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuarios` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `usuario` varchar(255) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('usuario','admin') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuarios`, `nombre`, `apellido`, `email`, `usuario`, `contraseña`, `rol`) VALUES
(1, 'Emmanuel', 'Sandoval', 'emmatwice.exo@gmail.com', 'Emma', 'scrypt:32768:8:1$B0r1FATUBIW4klf3$9ac95a8d38be497136e16506a6bfd803077f09c6a1579c78d6228851564f67b3e05853ae6960dd79faf5a415f0c94cfe860a69cefebbb43d97f4c58a52b337d7', 'admin'),
(2, 'Alejandrina', 'Polanias', 'aleja@gmail.com', 'Aleja', 'scrypt:32768:8:1$ljuziQTXdork3zJa$8aeb9cfbb4c2f081f85f718cc967bbd8828aa3e6bbf810820d69bd384de02b376dfa161c120db35934a479272b6e1cf14b2c563de33d07898bf5aee87fd11437', 'usuario'),
(3, 'Santiago', 'Ruiz', 'santi@gmail.com', 'khin0s', 'scrypt:32768:8:1$dvZF7Ijwh68Ri3p7$9916392ebff79e07e159b515c2c1d1f327f8fbb71e544651b7c13e6924a3a2080b10f9c0823efaa34dda0c3a1530fb1289ec336348876fce57b9acf972600684', 'usuario'),
(4, 'David', 'Contreras', 'davidc@gmail.com', 'davisito', 'scrypt:32768:8:1$rXfcqe0uy7m4nng9$912c00205f0f61e04ee8f5485cfde2c1fda461d5bc8396ae77884f258cfabf6d7c401c68e70275c8d211a6defa70682601ffba12cdb012b0c525ec8fef7ebf6c', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`IDtarea`),
  ADD KEY `tareas_ibfk_1` (`Id_Usuario1`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `IDtarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`Id_Usuario1`) REFERENCES `usuarios` (`idUsuarios`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
