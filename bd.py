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
    total INTEGER,
    DNI INTEGER,
    FOREIGN KEY (DNI) REFERENCES cliente(DNI)
)
''')


conn.commit()


cursor.execute('''
CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY,
    estado TEXT,
    id_factura INTEGER,
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
    nombre TEXT PRIMARY KEY,
    precio real
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE conjuntar(
    id INTEGER PRIMARY KEY,
    id_kit TEXT,
    id_producto INT,
    foreign key (id_kit) references kits(nombre),
    foreign key (id_producto) references producto(id_producto)
)
''')

cursor.execute('''
CREATE TABLE llevar(
    id INTEGER PRIMARY KEY,
    id_pedido INT,
    cantidad INT,
    id_producto INT,
    foreign key (id_pedido) references pedido(id_pedido),
    foreign key (id_producto) references producto(id_producto)
)
''')

cursor.execute('''
CREATE TABLE pedido_kit(
    id INTEGER PRIMARY KEY,
    id_pedido INT,
    cantidad INT,
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


cursor.execute('''INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(78000, 'Banco Plano de Pesas', 'Cap Barbell', 'Equipo') 
''')
conn.commit()

cursor.execute('''INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES
(19500, 'Glutamina en Polvo', 'nowSports', 'Suplemento')
''')
conn.commit()

cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (5000, 'Mancuerna 10kg', 'Everlast', 'Pesas')")
cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (8000, 'Barra olímpica', 'Rogue', 'Pesas')")
cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (2000, 'Colchoneta antideslizante', 'Reebok', 'Yoga')")
cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (3500, 'Soga para saltar', 'Adidas', 'Cardio')")
cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (15000, 'Bicicleta fija', 'SpinningPro', 'Cardio')")
cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (7000, 'Kettlebell 16kg', 'Kong', 'Pesas')")
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


cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(0, 50, 30, 5);
''')
conn.commit()

cursor.execute('''
INSERT INTO stock (minimo, maximo, total, id_producto) VALUES
(0, 100, 80, 6);
''')
conn.commit()


cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (5, 30, 12, 7)")
cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (2, 20, 8, 8)") 
cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 50, 25, 9)") 
cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 40, 18, 10)") 
cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (1, 10, 4, 11)")
cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (3, 25, 10, 12)")
conn.commit()

cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Cardio', 9500)") 
cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Yoga', 13500)")  
cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Fuerza', 22000)")
conn.commit()

cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Cardio', 10)")
cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Cardio', 11)")

cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Yoga', 9)")
cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Yoga', 10)")

cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 7)")
cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 8)")
cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 12)")

conn.commit()
