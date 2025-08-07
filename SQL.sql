
create database if not exists blackiron;

use blackiron;



CREATE TABLE  producto(
id_producto INT AUTO_INCREMENT PRIMARY KEY, 
precio int,
nombre_producto varchar(50),
marca varchar(50),
categoria_producto varchar(100)

);


CREATE TABLE stock (
id INT AUTO_INCREMENT PRIMARY KEY,
minimo INT,
maximo INT,
real FLOAT, 
id_producto INT,
foreign key (id_producto) references producto(id_producto)
);
CREATE TABLE cliente(
DNI INT AUTO_INCREMENT PRIMARY KEY,
gmail VARCHAR(50),
direccion VARCHAR(50),
apellido VARCHAR(50)
nombre VARCHAR(50)
);

CREATE TABLE factura(
id_factura INT AUTO_INCREMENT PRIMARY KEY, 
total INT,
nombre_producto varchar(50),
DNI INT,
foreign key (DNI) references cliente(DNI),
);

CREATE TABLE facturar(
id_facturar INT AUTO_INCREMENT PRIMARY KEY,
DNI INT,
id_factura INT,
 foreign key (DNI) references cliente(DNI),
 foreign key (id_factura) references factura(id_factura),
);

CREATE TABLE pedido(
id_pedido INT AUTO_INCREMENT PRIMARY KEY,
 estado VARCHAR(50)
 cantidad INT,
 id_producto INT,
 id_factura INT,
 foreign key (id_producto) references producto(id_producto),
 foreign key (id_factura) references factura(id_factura),
);

CREATE TABLE empleados(
id_empleado INT AUTO_INCREMENT PRIMARY KEY,
nombre varchar(50)
apellido varchar(50)
contraseña varchar(50)
);

create table kits(
id_kits INT AUTO_INCREMENT PRIMARY KEY,
foreign key (id_producto) references producto(id_producto)
);