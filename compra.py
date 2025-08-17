import sqlite3

from tomar_pedido import validar_longitud

conn = sqlite3.connect('blackiron.db')

cursor = conn.cursor()


def compra():
    try:
        r = True
        rd = True
        p1 = 0
        p2 = 0
        c = int(input('Ingrese la id de su factura. Si no la recuerda ingrese -1 para la ayuda de búsqueda: '))
        if c == -1:
            dni = int(input('Ingrese el DNI del cliente a nombre de la factura. Si no lo sabe o no quiere ingresarlo ingrese -1: '))
            if dni == -1:
                rd = False
                print('''Se le va a pedir que ingrese un rango de precio en el que recuerde que el total de la factura oscile.''')
                p1 = int(input('Ingrese el precio menor: '))
                p2 = int(input('Ingrese el precio mayor: '))
                if p1 > p2:
                    print('El rango de precio ingresado es erroneo (precio mínimo mayor a precio máximo).')
                    compra()
                busca_fac(dni,r, rd, p1,p2)
            else:
                if validar_longitud(dni):
                    print('''Se le va a pedir que ingrese un rango de precio en el que recuerde que el total de la factura oscile. Si no recuerda o no quiere ingresar dicho rango ingrese -1 en cualquier momento. ''')
                    p1 = int(input('Ingrese el precio menor: '))
                    if p1 == -1:
                        r = False
                        busca_fac(dni, r, rd, p1, p2)
                    p2 = int(input('Ingrese el precio mayor: '))
                    if p2 == -1:    
                        r = False
                        busca_fac(dni, r, rd, p1, p2)
                    if p1 > p2:
                        print('El rango de precio ingresado es erroneo (precio mínimo mayor a precio máximo).')
                        compra()
                    busca_fac(dni,r, rd, p1,p2)
                else:
                    compra()
        else:
            cursor.execute('''
            SELECT * FROM factura 
            WHERE id_factura = ?
            ''', (c,))
            dF = cursor.fetchall()
            for i in dF:
                idF,total, dn = i    
            print(f'''
            ---------------------------------
                ID de la factura: {idF}
                
                Monto total: {total}

                DNI: {dn} 
            ---------------------------------
            ''')
            vD = input('''¿Son estos datos correctos?
                    
                                S/N - ''')
            if vD.lower() == 's':
                cursor.execute('''
                UPDATE pedido
                set estado = 'Vendido'
                WHERE id_factura = ?
                ''', (c,))
                try:
                    cursor.execute('''SELECT id_producto, cantidad FROM llevar
                                    WHERE id_pedido IN(SELECT id_pedido FROM pedido
                                                    WHERE id_factura = ?)
                                   ''', (c,))
                    
                    ic = cursor.fetchall()
                    for i in ic:
                        idP, cant = i
                        cursor.execute('''UPDATE stock
                                        SET total = total - ?
                                        WHERE id_producto = ?
                                        ''', (cant, idP))

                    cursor.execute('''SELECT id_kit, cantidad FROM pedido_kit
                                WHERE id_pedido IN(SELECT id_pedido FROM pedido
                                                WHERE id_factura = ?)
                                   ''', (c,))
                    kic = cursor.fetchall()
                    for i in kic:
                        idK, cant = i
                        cursor.execute('''
                        SELECT id_producto FROM conjuntar
                        WHERE id_kit = ?
                        ''', (idK,))
                        p = cursor.fetchall()
                        for i in p:
                            pro = i[0]
                            cursor.execute('''
                            SELECT COUNT(id_producto) FROM conjuntar
                            WHERE id_kit = ?
                            GROUP BY id_producto
                            HAVING id_producto = ?
                            ''', (idK, pro))
                            ca = cursor.fetchone()
                            ca = ca[0]
                            canti = cant * ca
                            cursor.execute('''
                            UPDATE stock
                            SET total = total - ?
                            WHERE id_producto = ?
                            ''', (canti, pro))
                except Exception:
                    try:
                        cursor.execute('''SELECT id_kit, cantidad FROM pedido_kit
                                    WHERE id_pedido IN(SELECT id_pedido FROM pedido
                                                    WHERE id_factura = ?)
                                       ''', (c,))
                        
                        kic = cursor.fetchall()
                        for i in kic:
                            idK, cant = i
                            print(cant)
                            cursor.execute('''
                            SELECT id_producto FROM conjuntar
                            WHERE id_kit = ?
                            ''', (idK,))
                            p = cursor.fetchall()
                            for i in p:
                                pro = i[0]
                                cursor.execute('''
                                SELECT COUNT(id_producto) FROM conjuntar
                                WHERE id_kit = ?
                                GROUP BY id_producto
                                HAVING id_producto = ?
                                ''', (idK, pro))
                                ca = cursor.fetchone()
                                ca = ca[0]
                                canti = cant * ca

                                cursor.execute('''
                                UPDATE stock
                                SET total = total - ?
                                WHERE id_producto = ?
                                ''', (canti, pro))
                    except Exception:
                        cursor.execute('''SELECT id_producto, cantidad FROM llevar
                                    WHERE id_pedido IN(SELECT id_pedido FROM pedido
                                                    WHERE id_factura = ?)
                                       ''', (c,))
                        ic = cursor.fetchall()
                        for i in ic:
                            idP, cant = i
                            cursor.execute('''UPDATE stock
                                            SET total = total - ?
                                            WHERE id_producto = ?
                                            ''', (cant, idP))
                conn.commit()  
                print('La compra se realizó con éxito.')
                compra()
            elif vD.lower() == 'n':
                print('Entendido. Volviendo atrás...')
                compra()
            else:
                print('La opción ingresada es inexistente. Volviendo atrás...')
                compra()
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')
        compra()

def busca_fac(dni, r, rd, p1, p2):
    try:
        if rd == True:
            if r == True:
                cursor.execute('''
                SELECT id_factura, total from factura 
                WHERE DNI = ? AND total BETWEEN ? AND ? AND estado = 'En armado'
                ''', (dni, p1, p2))
                dF = cursor.fetchall()
                print('Mostrando facturas encontradas con los datos suministrados: ')
                for i in dF:
                    idF, total = i
                    print(f'''
                    --------------------------      
                    ID de la factura: {idF}
                    Precio total: {total}
                    --------------------------
                    ''')
            if r == False:
                cursor.execute('''
                SELECT id_factura, total from factura 
                WHERE DNI = ? AND estado = 'En armado'
                ''', (dni,))
                dF = cursor.fetchall()
                print('Mostrando facturas encontradas con los datos suministrados: ')
                for i in dF:
                    idF, total = i
                    print(f'''
                    --------------------------      
                    ID de la factura: {idF}
                    Precio total: {total}
                    --------------------------
                    ''')
        else:
            cursor.execute('''
            SELECT id_factura, total from factura 
            WHERE total BETWEEN ? AND ? AND estado = 'En armado'
            ''', (p1, p2))
            dF = cursor.fetchall()
            print(dF)
            print('Mostrando facturas encontradas con los datos suministrados: ')
            for i in dF:
                idF, total = i
                print(f'''
                --------------------------      
                ID de la factura: {idF}
                Precio total: {total}
                --------------------------
                ''') 
        compra()
    except Exception:
        print('No se han encontrado facturas con los datos suministrados.')
        compra()

compra()