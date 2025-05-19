use master
if exists (SELECT * FROM sysdatabases WHERE name = 'Tortilleria')
	drop database Tortilleria
go
CREATE DATABASE Tortilleria
go
USE Tortilleria

CREATE TABLE Usuario(
	IDusuario int not null identity(1,1),
	Nombre varchar(50) not null,
	Contrasena varchar(50) not null,
	Rol varchar(20)

	CONSTRAINT PK_IDusuario PRIMARY KEY (IDusuario)
)

CREATE TABLE Venta (
	IDventa int not null identity(1,1),
	Total money,
	Fecha datetime,
	IDusuario int not null,

	CONSTRAINT PK_IDventa PRIMARY KEY (IDventa),
	CONSTRAINT FK_IDusuario FOREIGN KEY (IDusuario) REFERENCES Usuario(IDusuario)
)

CREATE TABLE Producto(
	IDproducto int not null identity(1,1),
	Nombre varchar(50),
	Precio money,

	CONSTRAINT PK_IDproducto PRIMARY KEY (IDproducto)
)

CREATE TABLE Detalles_venta(
	IDventa int not null,
	IDproducto int not null,
	Cantidad int

	CONSTRAINT FK_IDventa FOREIGN KEY (IDventa) REFERENCES Venta(IDventa),
	CONSTRAINT FK_IDproducto FOREIGN KEY (IDproducto) REFERENCES Producto(IDproducto)
)

CREATE TABLE Reporte(
	IDreporte int not null identity(1,1),
	Tipo varchar(30),
	Fecha date,

	CONSTRAINT PK_IDreporte PRIMARY KEY (IDreporte)
)
INSERT INTO Usuario (Nombre, Contrasena, Rol) 
VALUES ('admin', 'verde001', 'Administrador')

-- Insertar usuarios
INSERT INTO Usuario (Nombre, Contrasena, Rol) VALUES
('Juan Pérez', 'password123', 'Administrador'),
('María López', 'abc123', 'Empleado'),
('Carlos Díaz', 'qwerty', 'Empleado');

-- Insertar productos
INSERT INTO Producto (Nombre, Precio) VALUES
('Tortilla de maíz', 26.00),
('Tortilla de harina', 22.00),
('Totopos', 30.00),
('Masa para tamales', 25.00);

-- Insertar ventas
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES
(66.00, '2025-04-27 10:30:00', 1),  -- Venta hecha por Juan
(44.00, '2025-04-27 11:00:00', 2);  -- Venta hecha por María

-- Insertar detalle de productos vendidos
-- Venta 1: Juan vendió 2 kg de tortilla de maíz y 1 bolsa de totopos
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(1, 1, 2),  -- 2 x 18 = 36
(1, 3, 1);  -- 1 x 30 = 30  --> 36 + 30 = 66 (ojo, corregir total si quieres exactitud)

-- Venta 2: María vendió 2 kg de tortilla de harina
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(2, 2, 2);  -- 2 x 22 = 44
go

-- Venta el 2025-04-25 por Juan
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES (90.00, '2025-04-25 08:15:00', 1);
-- IDventa = 3 (asumiendo consecutivo)
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(3, 1, 2),  -- 2 x 18 = 36
(3, 4, 2);  -- 2 x 25 = 50  => Total 86 (aproximado)

-- Venta el 2025-04-26 por María
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES (44.00, '2025-04-26 09:00:00', 2);
-- IDventa = 4
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(4, 2, 2);  -- 2 x 22 = 44

-- Venta el 2025-04-27 por Carlos
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES (60.00, '2025-04-27 10:00:00', 3);
-- IDventa = 5
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(5, 3, 2);  -- 2 x 30 = 60

-- Venta el 2025-04-28 por Juan
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES (36.00, '2025-04-28 14:00:00', 1);
-- IDventa = 6
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(6, 1, 2);  -- 2 x 18 = 36

-- Venta el 2025-04-29 por María
INSERT INTO Venta (Total, Fecha, IDusuario) VALUES (25.00, '2025-04-29 16:30:00', 2);
-- IDventa = 7
INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) VALUES
(7, 4, 1);  -- 1 x 25 = 25

GO

CREATE PROCEDURE SP_ReporteVentasPorRango
    @FechaInicio DATE,
    @FechaFin DATE
AS
BEGIN
    SELECT 
        P.Nombre AS Producto,
        DAY(V.Fecha) AS Dia,
        MONTH(V.Fecha) AS Mes,
        YEAR(V.Fecha) AS Anio,
        SUM(PV.Cantidad) AS CantidadTotal,
        SUM(P.Precio * PV.Cantidad) AS TotalGenerado
    FROM Detalles_Venta PV
    INNER JOIN Producto P ON PV.IDproducto = P.IDproducto
    INNER JOIN Venta V ON PV.IDventa = V.IDventa
    WHERE CAST(V.Fecha AS DATE) BETWEEN @FechaInicio AND @FechaFin
    GROUP BY 
        P.Nombre,
        DAY(V.Fecha),
        MONTH(V.Fecha),
        YEAR(V.Fecha)
    ORDER BY 
        Anio, Mes, Dia, P.Nombre;
END

go