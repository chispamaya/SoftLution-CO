import sqlite3


conn = sqlite3.connect('blackiron.db')


cursor = conn.cursor()
def ingresar_stock(id):
    try:
        min = int(input('Ingrese el stock mínimo: '))
        if min == -1:
            automatizar()
        max = int(input('Ingrese el stock máximo: '))
        if max == -1:
            automatizar()
        if min > max:
            print('Se ha detectado un error al ingresar los topes. Volviendo atrás.')
            automatizar()
        tot = int(input('Ingrese el stock disponible: '))
        if tot > max or tot < min:
            print('Se ha ingresado un stock que no contempla los límites establecidos. Volviendo atrás.')
            automatizar()
        if tot == -1:
            automatizar()
       
        cursor.execute('''
        INSERT into stock(minimo, maximo, total, id_producto)
                    VALUES(?, ?, ?, ?)
        ''', (min, max, tot, id))
    except Exception as e:
        print(f'Ha ocurrido un error durante el ingreso de stock. Por favor intente nuevamente: Error: {e}')
        automatizar()
    conn.commit()
    print('Datos del producto guardados correctamente.')


def automatizar():
    try:
        opcion = int(input('''
        Seleccione una opción:
       
        -----------------------------------------------
       
            1 - Ver productos y su stock.
           
            2 - Ingresar nuevos productos.
           
            3 - Modificar stock de un producto.
                       
            4 - Eliminar un producto.
           
            5 - Salir.    
       
        - '''))
    except Exception as e:
        print(f'Ha ocurrido un error durante la selección de opciones. Por favor intente nuevamente: Error: {e}')
        automatizar()
    if opcion == 1:
        cursor.execute('''
            SELECT minimo, maximo, total, id_producto FROM stock
            ''')
        datosStock = cursor.fetchall()
        for i in datosStock:
            minimo, maximo, total, id_p = i
            cursor.execute('''
                SELECT nombre_producto, marca, categoria_producto
                FROM producto
                WHERE id_producto = ?
            ''', (id_p,))
            datosProducto = cursor.fetchall()
            for n in datosProducto:
                nombre, marca, cat = n
                print(f'-------------------------------------------------------------------------------------------------------------------------------- \n Nombre: {nombre}, Marca: {marca}, Categoría: {cat} \n Stock Mínimo: {minimo}, Stock Máximo: {maximo}, Stock actual: {total}.')
        automatizar()
    elif opcion == 2:
        try:
            cant = int(input('Ingrese la cantidad de prodcutos que quiere ingresar. Ingrese -1 en cualquier momento para cualquiera de las siguientes opciones si desea salir: : '))
            for i in range(cant):
                nombre = input(f'Ingrese el nombre del producto {i+1}: ')
                if nombre == '-1':
                    automatizar()
                marca = input('Ingrese la marca: ')
                if marca == '-1':
                    automatizar()
                categoria = input('Ingrese la categoría correspondiente: ')
                if categoria == '-1':
                    automatizar()
                precio = float(input(f'Ingrese el precio de {nombre}: '))
                if precio == -1:
                    automatizar()
                cursor.execute('''
                INSERT into producto(precio, nombre_producto, marca, categoria_producto)
                VALUES(?, ?, ?, ?)
                            ''', (precio, nombre, marca, categoria,))
                cursor.execute('''
                SELECT id_producto from producto
                WHERE nombre_producto = ? AND marca = ?
                ''', (nombre, marca,))
                id = cursor.fetchone()
                if id == 'None':
                    print('No se ha encontrado el producto ingresado.')
                    automatizar()
                for i in id:
                    idd = i
                    ingresar_stock(idd)
        except Exception as e:
            print(f'Ha ocurrido un error durante el ingreso de datos del producto. Por favor intente nuevamente: Error: {e}')
            automatizar()
        automatizar()    
    elif opcion == 3:
        try:    
            nom = input('Ingrese el nombre del producto que desea modificar su stock. Ingrese -1 en cualquier momento para cualquiera de las siguientes opciones si desea salir: ')
            if nom == '-1':
                automatizar()
            mar = input(f'Ingrese la marca de {nom}: ')
            if mar == '-1':
                automatizar()
            cursor.execute('''
            SELECT id_producto from producto
            WHERE nombre_producto = ? AND marca = ?
                        ''', (nom, mar))
            aidi = cursor.fetchone()
            if aidi == 'None':
                    print('No se ha encontrado el producto ingresado.')
                    automatizar()
            for i in aidi:
                ide = i
                cursor.execute('''
            SELECT minimo, maximo, total
            FROM stock
            WHERE id_producto = ?
            ''', (ide,))
            stocks = cursor.fetchall()
            for i in stocks:
                minn, maxx, tota = i
                print(f'''
                    ------------------------
                    Stock mínimo: {minn}
                    ------------------------
                   
                    ------------------------
                    Stock máximo: {maxx}
                    ------------------------  
                   
                    ------------------------
                    Stock actual: {tota}
                    ------------------------
                   
                Ingrese -2 en cualquier momento, si desea mantener dicho número tal como esta.
                    ''')
               
                numin = int(input('Ingrese el stock mínimo: '))
                if numin == -1:
                    automatizar()
                elif numin == -2:
                    numin = minn
                numax = int(input('Ingrese el stock máximo: '))
                if numax == -1:
                    automatizar()
                elif numax == -2:
                    numax = maxx
                if numin > numax:
                    print('Se han ingresado valores erroneos. Los límites establecidos no tienen sentido.')
                    automatizar()
                nutota = int(input('Ingrese el stock: '))
                if nutota == -1:
                    automatizar()
                elif nutota == -2:
                    nutota = tota
                if nutota > numax or nutota < numin:
                    print('Se han ingresado valores erroneos. El stock no cumple con los límites establecidos.')
                    automatizar()
                cursor.execute('''
                UPDATE stock
                SET minimo = ?,maximo = ?,total = ?
                WHERE id_producto = ?
                            ''', (numin, numax, nutota, ide,))
                conn.commit()
                print('Datos guardados con éxito.')
                automatizar()
       
        except Exception as e:
            print(f'Ha ocurrido un error durante la modificación del stock. Por favor intente nuevamente: Error: {e}')
            automatizar()
    elif opcion == 4:
        try:
            no = input('Ingrese el nombre del producto que desea eliminar su stock. Ingrese -1 en cualquier momento para cualquiera de las siguientes opciones si desea salir: ')
            if no == '-1':
                automatizar()
            ma = input(f'Ingrese la marca de {no}: ')
            if ma == '-1':
                automatizar()
            cursor.execute('''
            SELECT id_producto from producto
            WHERE nombre_producto = ? AND marca = ?
                        ''', (no, ma))
            aid = cursor.fetchone()
            if aid == 'None':
                print('No se ha encontrado el producto ingresado.')
                automatizar()
            for i in aid:
                idi = i
                cursor.execute('''
                DELETE FROM producto
                WHERE id_producto = ?
                            ''', (idi,))
                cursor.execute('''
                DELETE FROM stock
                WHERE id_producto = ?
                            ''', (idi,))
                conn.commit()
                print('Producto eliminado con éxito.')
                automatizar()
        except Exception as e:
            print(f'Ha ocurrido un error durante la eliminación del producto. Por favor intente nuevamente: Error: {e}')
            automatizar()
    elif opcion == 5:
        print('Gracias por usar nuestro sistema.')
    else:
        print('Esa opción no existe.')
        automatizar()
automatizar()
