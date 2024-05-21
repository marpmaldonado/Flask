-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-05-2024 a las 20:12:50
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
(13, 'Trapear', '2024-05-20', '2024-05-24', 'en proceso', 5),
(22, 'recoger los niños', '2024-05-15', '2024-05-03', 'terminado', 8),
(23, 'Cocinar', '2024-05-11', '2024-05-07', 'por asignar', 8),
(24, 'tarea de mate', '2020-12-12', '2020-01-12', 'en proceso', 8),
(25, 'lavar el carro', '2022-09-07', '2023-09-08', 'por asignar', 8);

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
(5, 'Jack', 'Molina', 'jack@gmail.com', 'jackjack', 'scrypt:32768:8:1$BY0NzawrUyH1SFdY$fae6a5435b4c6c78e51858a52e153d600d0b543bca08795f060a2d3619aad56dcb19fc49c201823ca36755418fdd594f474464a9eeedf8e44d0150fd45a2c6d9', 'usuario'),
(6, 'Mariap', 'MM', 'cielopaulis1@gmail.com', 'MPMP', 'scrypt:32768:8:1$bVi6Z9PlaCEhIyPq$d5f81853089c862d10194ae9f72a2dcb0789fb13716d9729e39eceb9e54f256b9d14455a8aed6e18a4a4758705eac57c50a243403a40c450a7395dece59d32f3', 'admin'),
(7, 'Gatorade', 'Bebida Hidratante', 'gatorade@gmail.com', 'Gatorade', 'scrypt:32768:8:1$3Wr8Ut73ysucxRD0$bd40fa5cccee0979738f6f62521b342956652c473f033737d51d0cc5d3b5500bdc40184593fc2741d420d36e5cdb97ceaf387238be3fc46f1433f56c4e3c9f50', 'admin'),
(8, 'usuario', 'u', 'usuario@gmail.com', 'usuario', 'scrypt:32768:8:1$OX1lD4Bq5iZ2uQij$06e5447423878824d4dc1b34f8e23911698fefc8687964e657455da6a70b325501bbac8450d100084f631f261b84ff9685f3c3a56dc42d48e95110473414951e', 'usuario');

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
  MODIFY `IDtarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
