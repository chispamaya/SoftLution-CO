import sqlite3

conn = sqlite3.connect('blackiron.db')

cursor = conn.cursor()

def automatizar():
    opcion = int(input('''
    Seleccione una opción: 
    
    -----------------------------------------------
    
        1 - Ver productos y su stock.
        
        2 - Ingresar un nuevo producto.
        
        3 - Ingresar stock de uno o más productos.
        
        4 - Cambiar stock máximo o/y mínimo de un producto.
        
        4 - Salir.    
    
    - 
    
    '''))

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
                print(f'Nombre: {nombre}, Marca: {marca}, Categoría: {cat}, Stock Mínimo: {minimo}, Stock Máximo: {maximo}, Stock actual: {total}.')


    if opcion == 2:


automatizar()