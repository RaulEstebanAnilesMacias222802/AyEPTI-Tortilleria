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
	Rol varchar(50)

	CONSTRAINT PK_IDusuairo PRIMARY KEY (IDusuario)
)

CREATE TABLE Venta (
	IDventa int not null identity(1,1),
	Total money,
	IDusuario int not null,

	CONSTRAINT PK_IDventa PRIMARY KEY (IDventa),
	CONSTRAINT FK_IDusuario FOREIGN KEY (IDusuario) REFERENCES Usuario(IDusuario)
)

CREATE TABLE Producto(
	IDproducto int not null identity(1,1),
	Nombre varchar(50),
	Cantidad float,

	CONSTRAINT PK_IDproducto PRIMARY KEY (IDproducto)
)

CREATE TABLE Detalles_venta(
	IDdetalles int not null identity(1,1),
	Fecha date,
	Total int,
	IDventa int not null,
	IDproducto int not null,

	CONSTRAINT PK_IDdetalles PRIMARY KEY (IDdetalles),
	CONSTRAINT FK_IDventa FOREIGN KEY (IDventa) REFERENCES Venta(IDventa),
	CONSTRAINT FK_IDproducto FOREIGN KEY (IDproducto) REFERENCES Producto(IDproducto)
)

CREATE TABLE Reporte(
	IDreporte int not null identity(1,1),
	Tipo varchar(30),
	Fecha date,

	CONSTRAINT PK_IDreporte PRIMARY KEY (IDreporte)
)

