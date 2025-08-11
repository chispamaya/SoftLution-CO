import sqlite3

conn = sqlite3.connect('blackiron.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE producto (
    id_producto INTEGER PRIMARY KEY,
    precio INT,
    nombre_producto TEXT,
    marca TEXT,
    categoria_producto TEXT
);

CREATE TABLE stock (
    id INTEGER PRIMARY KEY,
    minimo INT,
    maximo INT,
    real REAL,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE cliente (
    DNI INTEGER PRIMARY KEY,
    gmail TEXT,
    direccion TEXT,
    apellido TEXT,
    nombre TEXT
);

CREATE TABLE factura (
    id_factura INTEGER PRIMARY KEY,
    total INT,
    nombre_producto TEXT,
    DNI INTEGER,
    FOREIGN KEY (DNI) REFERENCES cliente(DNI)
);

CREATE TABLE facturar (
    id_facturar INTEGER PRIMARY KEY,
    DNI INTEGER,
    id_factura INTEGER,
    FOREIGN KEY (DNI) REFERENCES cliente(DNI),
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
);

CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY,
    estado TEXT,
    cantidad INT,
    id_producto INTEGER,
    id_factura INTEGER,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
);

CREATE TABLE empleados (
    id_empleado INTEGER PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    contrasenia TEXT
);

CREATE TABLE kits (
    id_kits INTEGER PRIMARY KEY,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);
''')

conn.commit()
