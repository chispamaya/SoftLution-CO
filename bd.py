import sqlite3


conn = sqlite3.connect('blackiron.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE producto (
    id_producto INTEGER PRIMARY KEY,
    precio real,
    nombre_producto TEXT,
    marca TEXT,
    categoria_producto TEXT
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE stock (
    id INTEGER PRIMARY KEY,
    minimo INT,
    maximo INT,
    total int,
    id_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE cliente (
    DNI INTEGER PRIMARY KEY,
    gmail TEXT,
    direccion TEXT,
    apellido TEXT,
    nombre TEXT
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE factura (
    id_factura INTEGER PRIMARY KEY,
    total INT,
    DNI INTEGER,
    FOREIGN KEY (DNI) REFERENCES cliente(DNI)
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY,
    estado TEXT,
    cantidad INT,
    id_producto INTEGER,
    id_factura INTEGER,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE empleados (
    id_empleado INTEGER PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    contrasenia TEXT
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE kits (
    nombre INTEGER PRIMARY KEY,
    precio real
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE conjuntar(
    id INT PRIMARY KEY,
    id_kit INT,
    id_producto INT,
    foreign key (id_kit) references kits(id),
    foreign key (id_producto) references producto(id_producto)
)
''')

cursor.execute('''
CREATE TABLE llevar(
    id INT PRIMARY KEY,
    id_pedido INT,
    id_producto INT,
    foreign key (id_pedido) references pedido(id_pedido),
    foreign key (id_producto) references producto(id_producto)
)
''')

cursor.execute('''
CREATE TABLE pedido-kit(
    id INT PRIMARY KEY,
    id_pedido INT,
    id_kit INT,
    foreign key (id_kit) references kits(id),
    foreign key (id_pedido) references pedido(id_pedido)
)
''')

conn.commit()

cursor.execute('''
INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(25000, 'Proteína de suero', 'Optimum Nutrition', 'Suplemento')
''')


conn.commit()




cursor.execute('''
INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(12000, 'Creatina monohidratada', 'Universal Nutrition', 'Suplemento');
''')


conn.commit()




cursor.execute('''
INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(1500, 'Guantes de entrenamiento', 'Nike', 'Accesorio');
''')


conn.commit()




cursor.execute('''
INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(30000, 'BCAA en polvo', 'MuscleTech', 'Suplemento');
''')


conn.commit()




cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(10, 50, 30, 1);
''')


conn.commit()




cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(5, 20, 15, 2);
''')


conn.commit()




cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(20, 100, 50, 3);
''')


conn.commit()




cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(8, 40, 25, 4);
''')


conn.commit()




