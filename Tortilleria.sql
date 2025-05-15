use master
if exists (SELECT * FROM sysdatabases WHERE name = 'Tortilleria')
	drop database Tortilleria
go
CREATE DATABASE Tortilleria
go
USE Tortilleria

CREATE TABLE Usuario(
	IDusuario int not null identity(1,1),
	Nombre varchar(50),
	Contrasena varchar(255) not null,
	Rol varchar(50)

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
	IDdetalles int not null identity(1,1),
	Fecha date,
	Total money,
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