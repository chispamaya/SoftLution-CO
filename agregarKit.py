import sqlite3

conn = sqlite3.connect('blackiron.db')

cursor = conn.cursor()

def ingresar_kit():
        print('Ha seleccionado la opción de ingresar un kit.')
        nombre = input('Ingrese el nombre del kit: ')
        cursor.execute('''SELECT * 
                    FROM kits
                    WHERE nombre = ?
                    ''', (nombre,))
        k = cursor.fetchone()
        if k is None:
            precio = float(input('Ingrese el precio del kit: '))
            total = int(input(f'¿De cuantos productos estará compuesto {nombre}?: '))
            cursor.execute('''INSERT INTO kits(nombre, precio)
                        VALUES(? , ?)
                        ''', (nombre, precio))
            conn.commit()
            for i in range(total):
                producto = input(f'Ingrese el nombre del producto {i+1}: ')
                marca = input(f'Ingrese la marca de {producto}: ')
                cursor.execute('''
                SELECT id_producto 
                from producto
                where nombre_producto = ? AND marca = ?
                ''', (producto, marca))
                p = cursor.fetchall()
                if p == []:
                    print(f'No se ha encontrado el producto {producto} con la marca {marca}.')
                    cursor.execute('''
                    DELETE FROM kits
                    WHERE nombre = ?
                    ''', (nombre,))
                    conn.commit()
                    ingresar_kit()
                else:
                    for i in p:
                        pr = i[0]
                        cant = int(input(f'¿Cuantos/as {producto} va a haber en el kit?: '))
                        for n in range(cant):
                            cursor.execute('''
                            INSERT into conjuntar(id_kit, id_producto)
                            VALUES(?, ?)
                            ''', (nombre, pr))
            conn.commit()
            print('Kit ingresado con éxito.')
            ingresar_kit()
        else:   
            print('Ha ocurrido un error: El kit ingresado ya existe.')            
            ingresar_kit()



def borrar_kit():
        print('Ha seleccionado la opción de eliminar un kit.')
        nombre = input('Ingrese el nombre del kit: ')
        cursor.execute('''SELECT * 
                    FROM kits
                    WHERE nombre = ?
                    ''', (nombre,))
        k = cursor.fetchone()
        if k is None:
            print('Ese kit no existe.')
            borrar_kit()
        else:
            cursor.execute('''
            DELETE FROM kits
            WHERE nombre = ?
            ''', (nombre,))
            conn.commit()
            print('Kit eliminado con éxito.')


def modificar_kit():
    print('Ha seleccionado la opción de modificar un kit.')
    nombre = input('Ingrese el nombre del kit: ')
    dicP = {}
    listCant = []
    cursor.execute('''SELECT * 
                FROM kits
                WHERE nombre = ?
                ''', (nombre,))
    k = cursor.fetchone()
    if k is None:
        print('Ese kit no existe.')
        modificar_kit()
    else:
        opcion = int(input('''
                            Seleccione una opción:
                           
                           1 - Modificar productos dentro de un kit.

                           2 - Modificar nombre/precio de un kit.

                           3 - Modificar productos + nombre/precio de un kit.

                           4 - Salir
        '''))
        if opcion == 1:
                cursor.execute('''
                    SELECT 
                        p.nombre_producto, 
                        p.marca, 
                        COUNT(c.id_producto)
                    FROM conjuntar AS c
                    JOIN producto AS p 
                    ON c.id_producto = p.id_producto
                    WHERE c.id_kit = ?
                    GROUP BY c.id_producto, p.nombre_producto, p.marca;
                ''', (nombre,))
                
                productos_en_kit = cursor.fetchall()

                if not productos_en_kit:
                    print("No se encontraron productos para ese kit.")
                    modificar_kit()
                
                print("\n--- Productos en el kit ---")
                for nom, marca, cantidad in productos_en_kit:
                    print(f'''
                ------------------------------------------
                Producto: {nom}
                Marca: {marca}
                Cantidad encontrada: {cantidad}
                ------------------------------------------
                            ''')
                
                    dicP[nom] = marca
                    listCant.append(cantidad)



                nuMo = int(input(f'\nDe los diferentes productos encontrados ({len(productos_en_kit)}), ¿Cuántos desea modificar?: '))

                if nuMo > len(productos_en_kit):
                    print('No hay tantos productos diferentes en la lista.')
                    modificar_kit()

                for i in range(nuMo):
                    nombr = input(f'Ingrese el nombre del producto {i+1}: ')
                    ma = input(f'Ingrese la marca de {nombr}: ')

                    for b in range(len(listCant)):
                        cursor.execute('''
                        SELECT count(id_producto)
                        FROM conjuntar
                        WHERE id_kit = ?
                        GROUP BY id_producto
                        HAVING id_producto = (SELECT id_producto
                                       FROM producto 
                                       WHERE nombre_producto = ? AND marca = ?)
                        ''', (nombre, nombr, ma))
                        cca = cursor.fetchone()
                        cca = cca[0]
                        if cca == listCant[b]:
                            canP = listCant[b]
                            break

                    print(f'Cantidad actual de {nombr}, {ma}): {canP}')
                    
                    nuCant = int(input('Ingrese la nueva cantidad: '))

                    if nuCant < 0:
                        print('Cantidad no válida. Debe ser un número mayor o igual a cero.')
                        modificar_kit()

                    cursor.execute('''
                        SELECT id_producto FROM producto
                        WHERE nombre_producto = ? AND marca = ?;
                    ''', (nombr, ma))
                    idP = cursor.fetchone()
                    
                    idP = idP[0]

                    for b in range(len(listCant)):
                        cursor.execute('''
                        SELECT count(id_producto)
                        FROM conjuntar
                        WHERE id_kit = ?
                        GROUP BY id_producto
                        HAVING id_producto = ?
                        ''', (nombre, idP))
                        cca = cursor.fetchone()
                        cca = cca[0]
                        if cca == listCant[b]:
                            canP = listCant[b]
                            break

                    if nuCant == 0:
                        cursor.execute('''
                            DELETE FROM conjuntar 
                            WHERE id_producto = ? AND id_kit = ?;
                        ''', (idP, nombre))
                    
                    elif nuCant < canP:
                        canT = canP - nuCant
                        cursor.execute('''
                        DELETE FROM conjuntar
                        WHERE id IN(SELECT id
                                                        FROM conjuntar
                                                        WHERE id_kit = ? AND id_producto = ?
                                                        LIMIT ?)
                                                        ''', (nombre, idP, canT))
                    elif nuCant > canP:
                        canT = nuCant - canP
                        for j in range(canT):
                            cursor.execute('''
                            INSERT INTO conjuntar(id_kit, id_producto)
                            VALUES(?, ?)
                            ''', (nombre, idP))

                conn.commit()
                print('\nKit modificado con éxito.')
                modificar_kit()
                



        elif opcion == 2:
            dicP = {}
            listCant = []
            print('Se le van a pedir unos datos sobre el kit. Si en cualquier momento quiere salir ingrese -1. Si quiere dejar el valor tal como está ingrese -2...')
            cursor.execute('''
            SELECT * from kits
            WHERE nombre = ?
            ''', (nombre,))
            dK = cursor.fetchall()
            for i in dK:
                nombre, precio = i
                print(f'''
                ------------------------------------------
                        Nombre: {nombre}

                        Precio: {precio}
                ------------------------------------------
                        ''')
            nNuevo = input('Ingrese el nuevo nombre: ')
            if nNuevo == '-1':
                print('Volviendo atrás...')
                modificar_kit()
            elif nNuevo == '-2':
                nNuevo = nombre
            pNuevo = float(input('Ingrese el precio nuevo: '))
            if pNuevo == -1:
                print('Volviendo atrás...')
                modificar_kit()
            elif pNuevo == -2:
                pNuevo = precio
            cursor.execute('''
                        UPDATE kits 
                        SET nombre = ?, precio = ?
                        WHERE nombre = ?
                        ''', (nNuevo, pNuevo, nombre))
            cursor.execute('''
            UPDATE conjuntar
            SET id_kit = ?
            WHERE id_kit = ?
            ''', (nNuevo, nombre))
            conn.commit()
            print('Kit modificado con éxito.')
            modificar_kit()


        elif opcion == 3:
            dicP = {}
            listCant = []
            print('Se le van a pedir unos datos sobre el kit. Si en cualquier momento quiere salir ingrese -1. Si quiere dejar el valor tal como está ingrese -2...')
            cursor.execute('''
            SELECT * from kits
            WHERE nombre = ?
            ''', (nombre))
            dK = cursor.fetchall()
            for i in dK:
                Nombre, precio = i
                print(f'''
                ------------------------------------------
                        Nombre: {nombre}

                        Precio: {precio}
                ------------------------------------------
                        ''')
            nNuevo = input('Ingrese el nuevo nombre')
            if nNuevo == '-1':
                print('Volviendo atrás...')
                modificar_kit()
            elif nNuevo == '-2':
                nNuevo == nombre
            pNuevo = float(input('Ingrese el precio nuevo: '))
            if pNuevo == -1:
                print('Volviendo atrás...')
                modificar_kit()
            elif pNuevo == -2:
                pNuevo = precio
            cursor.execute('''
                        UPDATE kits 
                        SET nombre = ?, precio = ?
                        WHERE nombre = ?
                        ''', (nNuevo, pNuevo, nombre))
            cursor.execute('''
            UPDATE conjuntar
            SET id_kit = ?
            WHERE id_kit = ?
            ''', (nNuevo, nombre))
            conn.commit()
            print('Datos del kit modificados con éxito. Continuando a la modificación de contenido.')


            cursor.execute('''
                SELECT 
                    p.nombre_producto, 
                    p.marca, 
                    COUNT(c.id_producto)
                FROM conjuntar AS c
                JOIN producto AS p 
                ON c.id_producto = p.id_producto
                WHERE c.id_kit = ?
                GROUP BY c.id_producto, p.nombre_producto, p.marca;
            ''', (nombre,))
            
            productos_en_kit = cursor.fetchall()

            if not productos_en_kit:
                print("No se encontraron productos para ese kit.")
                modificar_kit()
            
            print("\n--- Productos en el kit ---")
            for nom, marca, cantidad in productos_en_kit:
                print(f'''
            ------------------------------------------
            Producto: {nom}
            Marca: {marca}
            Cantidad encontrada: {cantidad}
            ------------------------------------------
                        ''')
            
                dicP[nom] = marca
                listCant.append(cantidad)



            nuMo = int(input(f'\nDe los diferentes productos encontrados ({len(productos_en_kit)}), ¿Cuántos desea modificar?: '))

            if nuMo > len(productos_en_kit):
                print('No hay tantos productos diferentes en la lista.')
                modificar_kit()

            for i in range(nuMo):
                nombr = input(f'Ingrese el nombre del producto {i+1}: ')
                ma = input(f'Ingrese la marca de {nombr}: ')

                for b in range(len(listCant)):
                    cursor.execute('''
                    SELECT count(id_producto)
                    FROM conjuntar
                    WHERE id_kit = ?
                    GROUP BY id_producto
                    HAVING id_producto = (SELECT id_producto
                                   FROM producto 
                                   WHERE nombre_producto = ? AND marca = ?)
                    ''', (nombre, nombr, ma))
                    cca = cursor.fetchone()
                    cca = cca[0]
                    if cca == listCant[b]:
                        canP = listCant[b]
                        break

                print(f'Cantidad actual de {nombr}, {ma}): {canP}')
                
                nuCant = int(input('Ingrese la nueva cantidad: '))

                if nuCant < 0:
                    print('Cantidad no válida. Debe ser un número mayor o igual a cero.')
                    modificar_kit()

                cursor.execute('''
                    SELECT id_producto FROM producto
                    WHERE nombre_producto = ? AND marca = ?;
                ''', (nombr, ma))
                idP = cursor.fetchone()
                
                idP = idP[0]

                for b in range(len(listCant)):
                    cursor.execute('''
                    SELECT count(id_producto)
                    FROM conjuntar
                    WHERE id_kit = ?
                    GROUP BY id_producto
                    HAVING id_producto = ?
                    ''', (nombre, idP))
                    cca = cursor.fetchone()
                    cca = cca[0]
                    if cca == listCant[b]:
                        canP = listCant[b]
                        break

                if nuCant == 0:
                    cursor.execute('''
                        DELETE FROM conjuntar 
                        WHERE id_producto = ? AND id_kit = ?;
                    ''', (idP, nombre))
                
                elif nuCant < canP:
                    canT = canP - nuCant
                    cursor.execute('''
                    DELETE FROM conjuntar
                    WHERE id IN(SELECT id
                                                    FROM conjuntar
                                                    WHERE id_kit = ? AND id_producto = ?
                                                    LIMIT ?)
                                                    ''', (nombre, idP, canT))
                elif nuCant > canP:
                    canT = nuCant - canP
                    for j in range(canT):
                        cursor.execute('''
                        INSERT INTO conjuntar(id_kit, id_producto)
                        VALUES(?, ?)
                        ''', (nombre, idP))

            conn.commit()
            print('\nKit modificado con éxito.')
            modificar_kit()
