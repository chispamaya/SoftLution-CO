import sqlite3

conn = sqlite3.connect('blackiron.db')
cursor = conn.cursor()

def validar_longitud(numero):
    if len(str(numero)) >= 6 and len(str(numero)) < 10:
        print("\n")
        print("Número de documento válido.")
        return True
    else:
        print("Ingrese un número de documento válido con 8 dígitos.")
        return False

def validar_gmail(gmail):
        if '@' not in gmail:
                print('El gmail debe contener ''@''. Intentelo nuevamente. ')
                toma_pedido()
        return True

def toma_pedido():
        total = 0
        listPro = {}
        listKit = []
        listCant = []
        listCantP = []
        listCantK = []
        print('Ha seleccionado la opción de anotar un pedido...')
        print('Datos del cliente...')
        print('------------------------------')
        try:
                dni = int(input('Ingrese el DNI o documento de identidad: '))
        except Exception as e:
                print(f'Ingrese un número válido por favor.')
                toma_pedido()
        try:
                if validar_longitud(dni):
                        fac = input('''
                        ¿Yá tiene una factura en curso?
                        S/N - ''')
                        if fac.lower() == 'n':
                                opcion = int(input('''
                                El pedido es de productos sueltos, o kits de productos conjuntos?
                                
                                1 - Producto(s)
                                
                                2 - Kit(s)
                                
                                3 - Producto(s) + Kit(s)
                                
                                - '''))
                                print('------------------------------')
                                nombre = input('Ingrese el nombre: ')
                                print('------------------------------')
                                apellido = input('Ingrese su apellido: ')
                                print('------------------------------')
                                direccion = input('Ingrese la dirección de destino: ')
                                print('------------------------------')
                                gmail = input('Ingrese el gmail: ')
                                if validar_gmail(gmail):
                                        
                                        print('------------------------------')

                                        cursor.execute('''
                                        INSERT INTO cliente
                                        VALUES(?, ?, ?, ?, ?)
                                        ''', (dni, gmail, direccion, apellido, nombre))

                                        if opcion == 1:
                                                total = 0
                                                listPro = {}
                                                listCant = []
                                                cant = int(input('¿De cuantos productos diferentes es el pedido?: '))
                                                print('''Se le va a pedir que ingrese una cantidad  de productos acorde al número ingresado.
                                                Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
                                                for i in range(cant):
                                                        nombre = input(f'Ingrese el nombre del producto {i+1}: ')
                                                        marca = input(f'Ingrese la marca del producto {i+1}: ')
                                                        listPro[nombre] = marca
                                                        canti = int(input('¿Cuanta cantidad?: '))
                                                        listCant.append(canti)
                                                        cursor.execute('''
                                                        SELECT precio FROM producto
                                                        WHERE nombre_producto = ? AND marca = ?
                                                        ''', (nombre, marca))
                                                        p = cursor.fetchone()
                                                        for i in p:
                                                                pr = i
                                                                total = total + pr * canti
                                                cursor.execute('''
                                                INSERT into factura(total, DNI)
                                                VALUES(?, ?)
                                                ''', (total, dni))
                                                id_factura = cursor.lastrowid
                                                cursor.execute('''
                                                INSERT into pedido(estado, id_factura)
                                                VALUES('En armado', ?)
                                                ''', (id_factura,))
                                                id_pedido = cursor.lastrowid
                                                for i in listCant:
                                                        for nombre, marca in listPro.items():
                                                                cursor.execute('''
                                                                SELECT id_producto from producto
                                                                where nombre_producto = ? AND marca = ?
                                                                ''', (nombre, marca))
                                                                id_producto = cursor.fetchone()
                                                                id_producto = id_producto[0]
                                                                cursor.execute('''
                                                                INSERT into llevar(id_pedido, cantidad, id_producto)
                                                                VALUES(?, ?, ?)
                                                                ''', (id_pedido, i, id_producto))
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
                                                deseo = input('''¿Desea agregar más pedidos a su factura?: 
                                                        
                                                        S/N - ''')
                                                if deseo.lower() == 'n':
                                                        toma_pedido()
                                                elif deseo.lower() == 's':
                                                        seguir_pedido(id_factura, dni)

                                        elif opcion == 2:
                                                total = 0
                                                listKit = []
                                                listCant = []
                                                cant = int(input('¿De cuantos kits diferentes es el pedido?: '))
                                                print('''Se le va a pedir que ingrese los nombres de los respectivos kits deseados acorde al número ingresado.
                                                Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
                                                for i in range(cant):
                                                        nombre = input(f'Ingrese el nombre del kit {i+1}: ')
                                                        canti = int(input('¿Cuanta cantidad?: '))
                                                        listKit.append(nombre)
                                                        cursor.execute('''
                                                        SELECT precio FROM kits
                                                        WHERE nombre = ?
                                                        ''', (nombre,))
                                                        
                                                        p = cursor.fetchone()
                                                        for i in p:
                                                                pr = i
                                                                total = total + pr * canti
                                                cursor.execute('''
                                                INSERT into factura(total, DNI)
                                                VALUES(?, ?)
                                                ''', (total, dni))
                                                id_factura = cursor.lastrowid
                                                cursor.execute('''
                                                INSERT into pedido(estado, id_factura)
                                                VALUES('En armado', ?)
                                                ''', (id_factura,))
                                                id_pedido = cursor.lastrowid
                                                for i in listCant:
                                                        for n in listKit:
                                                                cursor.execute('''
                                                                INSERT into pedido_kit(id_pedido, cantidad, id_kit)
                                                                VALUES(?, ?, ?)
                                                                ''', (id_pedido, i, n))
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
                                                deseo = input('''¿Desea agregar más pedidos a su factura?: 
                                                        
                                                        S/N - ''')
                                                if deseo.lower() == 'n':
                                                        toma_pedido()
                                                elif deseo.lower() == 's':
                                                        seguir_pedido(id_factura, dni)
                                        
                                        elif opcion == 3:
                                                total = 0
                                                totalK = 0
                                                totalP = 0
                                                listPro = {}
                                                listKit = []
                                                listCantP = []
                                                listCantK = []
                                                print('A continuación, se le pedirán ingresar especificaciones acerca del pedido:')
                                                kits = int(input('¿Cuantos kits va a encargar?: '))
                                                for i in range(kits):
                                                        nombre = input('Ingrese el nombre del kit: ')
                                                        listKit.append(nombre)
                                                        cantid = int(input('¿Cuanta cantidad?: '))
                                                        listCantK.append (cantid)
                                                        cursor.execute('''
                                                        SELECT precio FROM kits
                                                        WHERE nombre = ?
                                                        ''', (nombre,))
                                                        pK = cursor.fetchone()
                                                        pK = pK[0]
                                                        totalK = totalK + pK * cantid

                                                productos = int(input('¿Cuantos productos va a encargar?: '))
                                                for i in range(productos):
                                                        nombre = input(f'Ingrese el nombre del producto {i+1}: ')
                                                        marca = input(f'Ingrese la marca del producto {i+1}: ')
                                                        listPro[nombre] = marca
                                                        canti = int(input('¿Cuanta cantidad?: '))
                                                        listCantP.append(canti)
                                                        cursor.execute('''
                                                        SELECT precio FROM producto
                                                        WHERE nombre_producto = ? AND marca = ?
                                                        ''', (nombre, marca))
                                                        p = cursor.fetchone()
                                                        for i in p:
                                                                pr = i  
                                                                totalP = totalP + pr * canti
                                                total = totalK + totalP
                                                cursor.execute('''
                                                INSERT INTO factura(total, DNI)
                                                        VALUES(?, ?)   
                                                ''', (total, dni))
                                                id_factura = cursor.lastrowid
                                                cursor.execute('''
                                                INSERT INTO pedido(estado, id_factura)
                                                                VALUES('En armado', ?)
                                                ''', (id_factura,))
                                                id_pedido = cursor.lastrowid
                                                for n in listCantK:
                                                        for i in listKit:
                                                                cursor.execute('''
                                                                INSERT INTO pedido_kit(id_pedido, cantidad, id_kit)
                                                                        VALUES(?, ?, ?)
                                                                ''', (id_pedido, n, i))
                                                for n in listCantP:
                                                        for nombre, marca in listPro.items():
                                                                cursor.execute('''
                                                                        SELECT id_producto from producto
                                                                        WHERE nombre_producto = ? AND marca = ?
                                                                ''',(nombre, marca))
                                                                idPr = cursor.fetchone()
                                                                idPr = idPr[0]
                                                                cursor.execute('''
                                                                INSERT INTO llevar(id_pedido, cantidad, id_producto)
                                                                        VALUES(?, ?, ?)
                                                                ''', (id_pedido, n, idPr))
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
                                                deseo = input('''¿Desea agregar más pedidos a su factura?: 

                                                        S/N - ''')
                                                if deseo.lower() == 'n':
                                                        toma_pedido()
                                                elif deseo.lower() == 's':
                                                        seguir_pedido(id_factura, dni)
                                
                                
                        elif fac.lower() == 's':
                                siONo = False
                                id_factura = int(input('Ingrese la ID de su factura: '))
                                cursor.execute('''
                                SELECT id_factura 
                                        FROM factura
                                ''')
                                test = cursor.fetchall()
                                for i in test:
                                        if id_factura == i[0]:
                                                siONo = True
                                                break
                                        
                                if siONo == True:
                                        seguir_pedido(id_factura, dni)
                                else:
                                        print('No se ha encontrado la id de factura ingresada. Volviendo atrás...')
                                        toma_pedido()
                        else:
                                print('Ingrese una opción válida.')
                                toma_pedido()
                else:
                        toma_pedido()
        except Exception as e:
                print(f'Ha ocurrido un error: {e}')       
                toma_pedido()

def seguir_pedido(id_factura, dni):
        listPro = {}
        total = 0
        listKit = []
        listCant = []
        listCantP = []
        listCantK = []
        cursor.execute('''
        SELECT DNI from factura
        WHERE id_factura = ?
        ''', (id_factura,))
        comprobar = cursor.fetchone()
        comprobar = comprobar[0]
        try:
                if dni == comprobar:
                        opcion = int(input('''
                                El pedido es de productos sueltos, o kits de productos conjuntos?

                                1 - Producto(s)

                                2 - Kit(s)
                                        
                                3 - Producto(s) + Kit(s)

                                - '''))

                        if opcion == 1:
                                total = 0
                                listPro = {}
                                listCant = []
                                cant = int(input('¿De cuantos productos diferentes es el pedido?: '))
                                print('''Se le va a pedir que ingrese una cantidad  de productos acorde al número ingresado.
                                        Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
                                for i in range(cant):
                                        nombre = input(f'Ingrese el nombre del producto {i + 1}: ')
                                        marca = input(f'Ingrese la marca del producto {i + 1}: ')
                                        listPro[nombre] = marca
                                        canti = int(input('¿Cuanta cantidad?: '))
                                        listCant.append(canti)
                                        cursor.execute('''
                                        SELECT precio FROM producto
                                        WHERE nombre_producto = ? AND marca = ?
                                        ''', (nombre, marca))
                                        p = cursor.fetchone()
                                        p = p[0]
                                        total = total + p * canti
                                cursor.execute('''
                                        INSERT into pedido(estado, id_factura)
                                        VALUES('En armado', ?)
                                        ''', (id_factura,))
                                id_pedido = cursor.lastrowid
                                for n in listCant:
                                        for nombre, marca in listPro.items():
                                                cursor.execute('''
                                                SELECT id_producto from producto
                                                where nombre_producto = ? AND marca = ?
                                                ''', (nombre, marca))
                                                id_producto = cursor.fetchone()
                                                id_producto = id_producto[0]
                                                cursor.execute('''
                                                INSERT into llevar(id_pedido, cantidad, id_producto)
                                                VALUES(?, ?, ?)
                                                ''', (id_pedido, n, id_producto))
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
                                deseo = input('''¿Desea agregar más pedidos a su factura?: 
                                        
                                        S/N - ''')
                                if deseo.lower() == 'n':
                                        toma_pedido()
                                elif deseo.lower() == 's':
                                        seguir_pedido(id_factura, dni)

                        elif opcion == 2:
                                total = 0
                                listKit = []
                                listCant = []
                                cant = int(input('¿De cuantos kits diferentes es el pedido?: '))
                                print('''Se le va a pedir que ingrese los nombres de los respectivos kits deseados acorde al número ingresado.
                                Si desea salir y cancelar todo ingrese -1 en cualquier momento.''')
                                for i in range(cant):
                                        nombre = input(f'Ingrese el nombre del kit {i+1}: ')
                                        listKit.append(nombre)
                                        canti = int(input('¿Cuanta cantidad?: '))
                                        listCant.append(canti)
                                        cursor.execute('''
                                        SELECT precio FROM kits
                                        WHERE nombre = ?
                                        ''', (nombre,))
                                        p = cursor.fetchone()
                                        for i in p:
                                                pr = i
                                                total = total + pr * canti
                                cursor.execute('''
                                UPDATE factura
                                SET total = total + ?
                                WHERE id_factura = ?
                                ''', (total, id_factura))
                                cursor.execute('''
                                INSERT into pedido(estado, id_factura)
                                VALUES('En armado', ?)
                                ''', (id_factura,))
                                id_pedido = cursor.lastrowid
                                for i in listCant:
                                        for n in listKit:
                                                cursor.execute('''
                                                INSERT into pedido_kit(id_pedido, cantidad, id_kit)
                                                VALUES(?, ?, ?)
                                                ''', (id_pedido, i, n))
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
                                deseo = input('''¿Desea agregar más pedidos a su factura?: 
                                        
                                        S/N - ''')
                                if deseo.lower() == 'n':
                                        toma_pedido()
                                elif deseo.lower() == 's':
                                        seguir_pedido(id_factura, dni)
                        elif opcion == 3:
                                total = 0
                                totalK = 0
                                totalP = 0
                                listPro = {}
                                listKit = []
                                listCant = []
                                print('A continuación, se le pedirán ingresar especificaciones acerca del pedido:')
                                kits = int(input('¿Cuantos kits va a encargar?: '))
                                for i in range(kits):
                                        nombre = input('Ingrese el nombre del kit: ')
                                        listKit.append(nombre)
                                        cantid = int(input('¿Cuanta cantidad?: '))
                                        listCantK.append(cantid)
                                        cursor.execute('''
                                        SELECT precio FROM kits
                                        WHERE nombre = ?
                                        ''', (nombre,))
                                        pK = cursor.fetchone()
                                        pK = pK[0]
                                        totalK = totalK + pK * cantid

                                productos = int(input('¿Cuantos productos va a encargar?: '))
                                for i in range(productos):
                                        nombre = input(f'Ingrese el nombre del producto {i+1}: ')
                                        marca = input(f'Ingrese la marca del producto {i+1}: ')
                                        listPro[nombre] = marca
                                        canti = int(input('¿Cuanta cantidad?: '))
                                        listCantP.append(canti)
                                        cursor.execute('''
                                        SELECT precio FROM producto
                                        WHERE nombre_producto = ? AND marca = ?
                                        ''', (nombre, marca))
                                        p = cursor.fetchone()
                                        for i in p:
                                                pr = i  
                                                totalP = totalP + pr * canti
                                total = totalK + totalP
                                cursor.execute('''
                                UPDATE factura
                                        SET total = total + ?
                                ''', (total,))
                                cursor.execute('''
                                INSERT INTO pedido(estado, id_factura)
                                                VALUES('En armado', ?)
                                ''', (id_factura,))
                                id_pedido = cursor.lastrowid
                                for n in listCantK:
                                        for i in listKit:
                                                cursor.execute('''
                                                INSERT INTO pedido_kit(id_pedido, cantidad, id_kit)
                                                        VALUES(?, ?, ?)
                                                ''', (id_pedido, n, i))
                                for n in listCantP:
                                        for nombre, marca in listPro.items():
                                                cursor.execute('''
                                                        SELECT id_producto from producto
                                                        WHERE nombre_producto = ? AND marca = ?
                                                ''',(nombre, marca))
                                                idPr = cursor.fetchone()
                                                idPr = idPr[0]
                                                cursor.execute('''
                                                INSERT INTO llevar(id_pedido, cantidad, id_producto)
                                                        VALUES(?, ?, ?)
                                                ''', (id_pedido, n, idPr))
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
                                deseo = input('''¿Desea agregar más pedidos a su factura?: 

                                        S/N - ''')
                                if deseo.lower() == 'n':
                                        toma_pedido()
                                elif deseo.lower() == 's':
                                        seguir_pedido(id_factura, dni)
                        
                elif comprobar != dni:
                        print('Su DNI no corresponde con su ID de factura. Volviendo atrás...')
                        toma_pedido()    
        except Exception as e:
                print(f'Ha ocurrido un error: {e}')       
                toma_pedido()


