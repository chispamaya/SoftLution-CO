import sqlite3


conn = sqlite3.connect('blackiron.db')


cursor = conn.cursor()


def calStock():
    try:
        opcion = int(input('''
        Se le pide que seleccione una de las siguientes opciones:
                       
                        1 - Calcular stock total.
                       
                        2 - Calcular stock por categoría.
                       
                        3 - Salir.
                       
                        - '''))
    except Exception as e:
        print(f'Ha ocurrido un error durante la selección de opciones. Por favor intente nuevamente: Error: {e}')
        calStock()


    if opcion == 1:
        cursor.execute('''
        SELECT SUM(total) FROM stock
                    ''')
        total = cursor.fetchone()
        for i in total:
            totall = i
        print(f'Stock total: {totall}.')
        calStock()
       
    elif opcion == 2:
        try:
            opt = int(input('''
        Por favor seleccione la opción que considere más conveniente
                           
                        1 - Mostrar un listado de todas las categorías con su stock total correspondiente.
                           
                        2 - Mostrar el stock de una única categoría.
                           
                        3 - Volver atrás.
                           
                        - '''))
        except Exception as e:
            print(f'Ha ocurrido un error durante la selección de opciones. Por favor intente nuevamente: Error: {e}')
            calStock()
        if opt == 1:
            cursor.execute('''
        SELECT sum(total), categoria_producto
        from stock s inner join producto p on p.id_producto = s.id_producto
        GROUP by categoria_producto
        ''')
            xcat = cursor.fetchall()
            print('''
                ------------------------------------------------------------
                |Categoría                   |Stock                        |
                ------------------------------------------------------------
            ''')
            for i in xcat:
                stockxcat, cat = i
                print(f'{cat} -|- {stockxcat}')
            calStock()    
        elif opt == 2:
            try:
                categoria = input('Ingrese la categoría cuyo stock desea consultar: ')
                cursor.execute('''
                SELECT SUM(total)
                from stock s inner join producto p on s.id_producto = p.id_producto
                GROUP BY categoria_producto
                HAVING categoria_producto = ?
                ''', (categoria,))


                tot = cursor.fetchone()
                for i in tot:
                    tota = i
                    print(f'El stock total en la categoría de {categoria} es de {tota}.')
                calStock()
            except Exception as e:
                print(f'Ha ocurrido un error, no encontramos la categoría ingresada. Por favor intente nuevamente: Error: {e}')
                calStock()
        elif opt == 3:
            print('Volviendo atrás.')
            calStock()
        else:
            print('No se ha encontrado esa opción. Por favor, ingrese una válida.')
            calStock()
    elif opcion == 3:
        print('Gracias por usar nuestro sistema.')
    else:
        print('Por favor, ingrese una opción válida.')
        calStock()








calStock()
