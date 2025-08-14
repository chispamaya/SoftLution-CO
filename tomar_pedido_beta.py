import sqlite3

conn = sqlite3.connect('blackiron.db')
cursor = conn.cursor()

def toma_pedido():
    total = 0
    listPro = {}
    print('Ha seleccionado la opción de anotar un pedido...')
    print('Datos del cliente...')
    print('------------------------------')
    dni = int(input('Ingrese el DNI o documento de identidad: '))
    print('------------------------------')
    nombre = input('Ingrese el nombre: ')
    print('------------------------------')
    apellido = input('Ingrese su apellido: ')
    print('------------------------------')
    direccion = input('Ingrese la dirección de destino: ')
    print('------------------------------')
    gmail = input('Ingrese el gmail: ')
    print('------------------------------')
    fac = input('''
    ¿Yá tiene una factura en curso?
    S/N - ''')
    if fac.lower() == 'n':
        opcion = int(input('''
        El pedido es de productos sueltos, o kits de productos conjuntos?
        
        1 - Producto(s)
        
        2 - Kit(s)
        
        - '''))

        if opcion == 1:
            cant = int(input('¿De cuantos productos es el pedido?: '))
            print('''Se le va a pedir que ingrese una cantidad  de productos acorde al número ingresado.
            Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
            for i in range(cant):
                nombre = input(f'Ingrese el nombre del producto {i+1}: ')
                marca = input(f'Ingrese la marca del producto {i+1}: ')
                canti = int(input(('¿Cuanta cantidad?: ')))
                cursor.execute('''
                SELECT precio FROM producto
                WHERE nombre_producto = ? AND marca = ?
                ''', (nombre, marca))
                p = cursor.fetchone()
                for i in p:
                    pr = i
                    total = total + pr * canti
                    listPro[nombre] = marca
            cursor.execute('''
            INSERT into factura(total, DNI)
            VALUES(?, ?)
            ''', (total, dni))
            id_factura = cursor.lastrowid
            print(id_factura)
            cursor.execute('''
            INSERT into pedido(estado, id_factura)
            VALUES('En armado', ?)
            ''', (id_factura,))
            id_pedido = cursor.lastrowid
            for nombre, marca in listPro.items():
                cursor.execute('''
                SELECT id_producto from producto
                where nombre_producto = ? AND marca = ?
                ''', (nombre, marca))
                id_producto = cursor.fetchone()
                id_producto = id_producto[0]
                cursor.execute('''
                INSERT into llevar(id_pedido, id_producto)
                VALUES(?, ?)
                ''', (id_pedido, id_producto))
            conn.commit()
            cursor.execute('''
            SELECT * FROM factura
            where id_factura = ?
            ''', (id_factura,))
            datosFa = cursor.fetchall()
            for i in datosFa:
                id, tot, dn = i
                print(f'''DATOS DE SU FACTURA:
                        ID: {id}
                        MONTO TOTAL: {total}
                        DNI del comprador: {dn}
                ''')
            deseo = input('''¿Desea agregar más pedidos a su factura?: 
                    
                    S/N - ''')
            if deseo.lower() == 'n':
                toma_pedido()
            elif deseo.lower() == 's':
                seguir_pedido(id_factura, dni, nombre, apellido, direccion, gmail)
    elif fac.lower() == 's':
        id_factura = int(input('Ingrese la ID de su factura: '))
        seguir_pedido(id_factura, dni, nombre, apellido, direccion, gmail)

def seguir_pedido(id_factura, dni, nombre, apellido, direccion, gmail):
    listPro = {}
    total = 0
    opcion = int(input('''
            El pedido es de productos sueltos, o kits de productos conjuntos?

            1 - Producto(s)

            2 - Kit(s)

            - '''))

    if opcion == 1:
        cant = int(input('¿De cuantos productos es el pedido?: '))
        print('''Se le va a pedir que ingrese una cantidad  de productos acorde al número ingresado.
                Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
        for i in range(cant):
            nombre = input(f'Ingrese el nombre del producto {i + 1}: ')
            marca = input(f'Ingrese la marca del producto {i + 1}: ')
            canti = int(input(('¿Cuanta cantidad?: ')))
            cursor.execute('''
                    SELECT precio FROM producto
                    WHERE nombre_producto = ? AND marca = ?
                    ''', (nombre, marca))
            p = cursor.fetchone()
            p = p[0]
            total = total + p * canti
            listPro[nombre] = marca
        cursor.execute('''
                INSERT into pedido(estado, id_factura)
                VALUES('En armado', ?)
                ''', (id_factura,))
        id_pedido = cursor.lastrowid
        for nombre, marca in listPro.items():
            cursor.execute('''
                    SELECT id_producto from producto
                    where nombre_producto = ? AND marca = ?
                    ''', (nombre, marca))
            id_producto = cursor.fetchone()
            id_producto = id_producto[0]
            cursor.execute('''
                    INSERT into llevar(id_pedido, id_producto)
                    VALUES(?, ?)
                    ''', (id_pedido, id_producto))
        cursor.execute('''
        UPDATE factura
        SET total = total + ?
        WHERE id_factura = ?
        ''', (total, id_factura))
        conn.commit()
        cursor.execute('''
                SELECT * FROM factura
                where id_factura = ?
                ''', (id_factura,))
        datosFa = cursor.fetchall()
        for i in datosFa:
            id, tot, dn = i
            print(f'''DATOS DE SU FACTURA:
                            ID: {id}
                            MONTO TOTAL: {tot}
                            DNI del comprador: {dn}
                    ''')


toma_pedido()










