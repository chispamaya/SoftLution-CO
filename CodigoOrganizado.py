import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import time

intentos_fallidos = 0
tiempo_de_bloqueo = 0
MAX_INTENTOS = 3
TIEMPO_DE_ESPERA = 30

def configurar_base_de_datos():
    conn = sqlite3.connect("blackiron.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            marca TEXT,
            categoria_producto TEXT,
            precio REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER,
            minimo INTEGER,
            maximo INTEGER,
            total INTEGER,
            FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            DNI INTEGER,
            nombre TEXT,
            apellido TEXT,
            gmail TEXT,
            direccion TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factura (
            id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
            DNI INTEGER,
            nombre_producto TEXT,
            total REAL,
            FOREIGN KEY(DNI) REFERENCES cliente(DNI)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT,
            cantidad INTEGER,
            id_producto INTEGER,
            id_factura INTEGER,
            FOREIGN KEY(id_producto) REFERENCES producto(id_producto),
            FOREIGN KEY(id_factura) REFERENCES factura(id_factura)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            contrasenia TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kits (
            id_kit INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER,
            nombre TEXT,
            precio REAL,
            FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
        )
    """)
    conn.commit()
    conn.close()

def poblar_datos_ejemplo():
    conn = sqlite3.connect("blackiron.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO empleados (nombre, apellido, contrasenia) VALUES ('admin', 'Gomez', '12345')")
        cursor.execute("INSERT INTO empleados (nombre, apellido, contrasenia) VALUES ('Juan', 'Perez', 'abcde')")
        
    cursor.execute("SELECT COUNT(*) FROM producto")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO producto (nombre_producto, marca, categoria_producto, precio) VALUES ('Proteina en Polvo', 'WheyPro', 'Suplementos', 150.50)")
        cursor.execute("INSERT INTO producto (nombre_producto, marca, categoria_producto, precio) VALUES ('Guantes de Gimnasio', 'FitGear', 'Accesorios', 25.00)")
        cursor.execute("INSERT INTO producto (nombre_producto, marca, categoria_producto, precio) VALUES ('Mancuerna de 10kg', 'IronGym', 'Equipo', 300.00)")
        cursor.execute("INSERT INTO producto (nombre_producto, marca, categoria_producto, precio) VALUES ('Banda Elastica', 'FitGear', 'Accesorios', 200.00)")
        
    cursor.execute("SELECT COUNT(*) FROM stock")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 50, 5, 1)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (5, 20, 12, 2)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (2, 10, 5, 3)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (5, 25, 0, 4)")
        
    cursor.execute("SELECT COUNT(*) FROM cliente")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO cliente (DNI, gmail, direccion, apellido, nombre) VALUES (12345678, 'cliente1@mail.com', 'Calle Falsa 123', 'Diaz', 'Carlos')")
        
    cursor.execute("SELECT COUNT(*) FROM factura")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO factura (DNI, total) VALUES (12345678, 150.50)")
        
    cursor.execute("SELECT COUNT(*) FROM pedido")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pedido (estado, id_factura) VALUES ('entregado', 1)")
        
    conn.commit()
    conn.close()

class AplicacionBlackIron:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Gestión Black Iron")
        self.raiz.geometry("350x250")
        self.raiz.resizable(False, False)
        
        configurar_base_de_datos()
        poblar_datos_ejemplo()
        self.mostrar_pantalla_inicio_sesion()

    def limpiar_marco(self):
        for widget in self.raiz.winfo_children():
            widget.destroy()

    def mostrar_pantalla_inicio_sesion(self):
        self.limpiar_marco()
        self.raiz.title("Iniciar Sesión")
        self.raiz.geometry("300x250")

        tk.Label(self.raiz, text="Nombre:").pack(pady=5)
        self.entrada_nombre = tk.Entry(self.raiz)
        self.entrada_nombre.pack(pady=5)
        
        tk.Label(self.raiz, text="Apellido:").pack(pady=5)
        self.entrada_apellido = tk.Entry(self.raiz)
        self.entrada_apellido.pack(pady=5)

        tk.Label(self.raiz, text="Contraseña:").pack(pady=5)
        self.entrada_contrasenia = tk.Entry(self.raiz, show="*")
        self.entrada_contrasenia.pack(pady=5)

        boton_iniciar_sesion = tk.Button(self.raiz, text="Iniciar Sesión", command=self.verificar_inicio_sesion)
        boton_iniciar_sesion.pack(pady=10)

    def verificar_inicio_sesion(self):
        global intentos_fallidos, tiempo_de_bloqueo

        if tiempo_de_bloqueo > time.time():
            tiempo_restante = int(tiempo_de_bloqueo - time.time())
            messagebox.showwarning("Cuenta Bloqueada",
                                   f"Demasiados intentos fallidos. Inténtalo de nuevo en {tiempo_restante} segundos.")
            return

        nombre = self.entrada_nombre.get()
        apellido = self.entrada_apellido.get()
        contrasenia = self.entrada_contrasenia.get()

        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleados WHERE nombre = ? AND apellido = ? AND contrasenia = ?", (nombre, apellido, contrasenia))
            empleado = cursor.fetchone()

            if empleado:
                intentos_fallidos = 0
                messagebox.showinfo("Acceso Correcto", f"¡Inicio de sesión exitoso! Bienvenido, {empleado[1]}.")
                self.mostrar_menu_empleado()
            else:
                intentos_fallidos += 1
                if intentos_fallidos >= MAX_INTENTOS:
                    tiempo_de_bloqueo = time.time() + TIEMPO_DE_ESPERA
                    messagebox.showerror("Error de Credenciales",
                                         f"Demasiados intentos fallidos. La cuenta ha sido bloqueada por {TIEMPO_DE_ESPERA} segundos.")
                    intentos_fallidos = 0
                else:
                    messagebox.showerror("Error de Credenciales",
                                         f"Usuario o contraseña incorrectos. Te quedan {MAX_INTENTOS - intentos_fallidos} intentos.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error de conexión o consulta a la base de datos: {e}")
        finally:
            if conn:
                conn.close()

    def mostrar_menu_empleado(self):
        self.limpiar_marco()
        self.raiz.title("Menú de Empleado")
        self.raiz.geometry("350x450")
        
        etiqueta_bienvenida = tk.Label(self.raiz, text="Bienvenido al sistema.", font=("Arial", 14))
        etiqueta_bienvenida.pack(pady=10)

        boton_tomar_pedido = tk.Button(self.raiz, text="Tomar Pedido (Ventas)", width=25, command=self.tomar_pedido)
        boton_tomar_pedido.pack(pady=5)
        boton_pedidos = tk.Button(self.raiz, text="Visualizar Pedidos", width=25, command=self.mostrar_pedidos)
        boton_pedidos.pack(pady=5)
        boton_kits = tk.Button(self.raiz, text="Ver Kits", width=25, command=self.mostrar_kits)
        boton_kits.pack(pady=5)

        separador = tk.Frame(self.raiz, height=2, bd=1, relief=tk.SUNKEN)
        separador.pack(fill=tk.X, padx=20, pady=10)
        
        etiqueta_gestion_stock = tk.Label(self.raiz, text="Gestión de Stock", font=("Arial", 12))
        etiqueta_gestion_stock.pack(pady=5)

        boton_ver_stock = tk.Button(self.raiz, text="Ver y Gestionar Stock", width=25, command=self.mostrar_menu_gestion_stock)
        boton_ver_stock.pack(pady=5)

        boton_cal_stock = tk.Button(self.raiz, text="Calcular Stock General", width=25, command=self.mostrar_menu_calcular_stock)
        boton_cal_stock.pack(pady=5)

        separador2 = tk.Frame(self.raiz, height=2, bd=1, relief=tk.SUNKEN)
        separador2.pack(fill=tk.X, padx=20, pady=10)

        boton_cerrar = tk.Button(self.raiz, text="Cerrar Sesión", width=25, command=self.mostrar_pantalla_inicio_sesion)
        boton_cerrar.pack(pady=10)

    def mostrar_pedidos(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT p.id_pedido, p.estado, p.cantidad, pr.nombre_producto, f.id_factura FROM pedido p INNER JOIN producto pr ON p.id_producto = pr.id_producto INNER JOIN factura f ON p.id_factura = f.id_factura")
            datos_pedidos = cursor.fetchall()

            ventana_pedidos = tk.Toplevel(self.raiz)
            ventana_pedidos.title("Visualizar Pedidos")

            widget_texto = tk.Text(ventana_pedidos, wrap="word", width=60, height=15)
            widget_texto.pack(pady=10, padx=10)

            widget_texto.insert(tk.END, "ID Pedido | Estado | Cantidad | Producto | ID Factura\n")
            widget_texto.insert(tk.END, "-----------------------------------------------------\n")

            for fila in datos_pedidos:
                widget_texto.insert(tk.END, f"{fila[0]:<10} | {fila[1]:<7} | {fila[2]:<8} | {fila[3]:<10} | {fila[4]}\n")

            widget_texto.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener pedidos: {e}")
        finally:
            if conn:
                conn.close()

    def mostrar_kits(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT k.nombre, p.nombre_producto FROM kits k INNER JOIN producto p ON k.id_producto = p.id_producto")
            datos_kits = cursor.fetchall()

            ventana_kits = tk.Toplevel(self.raiz)
            ventana_kits.title("Ver Kits")

            widget_texto = tk.Text(ventana_kits, wrap="word", width=40, height=10)
            widget_texto.pack(pady=10, padx=10)

            widget_texto.insert(tk.END, "ID Kit | Producto\n")
            widget_texto.insert(tk.END, "------------------------\n")

            for fila in datos_kits:
                widget_texto.insert(tk.END, f"{fila[0]:<7} | {fila[1]}\n")

            widget_texto.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener kits: {e}")
        finally:
            if conn:
                conn.close()

    def tomar_pedido(self):
        ventana_pedido = tk.Toplevel(self.raiz)
        ventana_pedido.title("Tomar Pedido")
        ventana_pedido.geometry("450x550")

        marco_formulario = tk.Frame(ventana_pedido)
        marco_formulario.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(marco_formulario, text="DNI del Cliente:").pack(pady=5)
        entrada_dni = tk.Entry(marco_formulario)
        entrada_dni.pack()

        tk.Label(marco_formulario, text="Nombre del Producto:").pack(pady=5)
        entrada_producto = tk.Entry(marco_formulario)
        entrada_producto.pack()

        tk.Label(marco_formulario, text="Cantidad:").pack(pady=5)
        entrada_cantidad = tk.Entry(marco_formulario)
        entrada_cantidad.pack()

        def guardar_pedido():
            try:
                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()

                dni = entrada_dni.get()
                nombre_producto = entrada_producto.get()
                cantidad = entrada_cantidad.get()

                if not dni or not nombre_producto or not cantidad:
                    messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
                    return

                cantidad = int(cantidad)

                cursor.execute("SELECT id_producto, precio FROM producto WHERE nombre_producto = ?", (nombre_producto,))
                info_producto = cursor.fetchone()

                if not info_producto:
                    messagebox.showerror("Producto Inexistente", "El producto no se encuentra en la base de datos.")
                    return

                id_producto, precio = info_producto

                cursor.execute("SELECT total FROM stock WHERE id_producto = ?", (id_producto,))
                stock_total = cursor.fetchone()

                if stock_total is None or stock_total[0] < cantidad:
                    messagebox.showerror("Error de Stock", "No hay suficiente stock disponible para este producto.")
                    return

                total_factura = precio * cantidad

                cursor.execute("INSERT INTO factura (total, nombre_producto, DNI) VALUES (?, ?, ?)",
                               (total_factura, nombre_producto, dni))
                id_factura = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO pedido (estado, cantidad, id_producto, id_factura) VALUES ('pendiente', ?, ?, ?)",
                    (cantidad, id_producto, id_factura))

                nuevo_stock = stock_total[0] - cantidad
                cursor.execute("UPDATE stock SET total = ? WHERE id_producto = ?", (nuevo_stock, id_producto))

                conn.commit()
                messagebox.showinfo("Pedido Guardado",
                                    f"El pedido para '{nombre_producto}' ha sido registrado con éxito. Total: ${total_factura}")
                
                self.mostrar_alertas_stock(widget_texto_stock)
                
            except sqlite3.Error as e:
                messagebox.showerror("Error de BD", f"Error al guardar el pedido: {e}")
            except ValueError:
                messagebox.showerror("Error de entrada", "La cantidad debe ser un número entero.")
            finally:
                if conn:
                    conn.close()

        boton_guardar = tk.Button(marco_formulario, text="Guardar Pedido", command=guardar_pedido)
        boton_guardar.pack(pady=10)

        separador = tk.Frame(ventana_pedido, height=2, bd=1, relief=tk.SUNKEN)
        separador.pack(fill=tk.X, padx=10, pady=5)

        marco_alerta = tk.Frame(ventana_pedido)
        marco_alerta.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(marco_alerta, text="⚠️ Alertas de Stock Bajo ⚠️", font=("Arial", 12)).pack(pady=5)

        widget_texto_stock = tk.Text(marco_alerta, wrap="word", width=45, height=15)
        widget_texto_stock.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        barra_desplazamiento = tk.Scrollbar(marco_alerta, command=widget_texto_stock.yview)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        widget_texto_stock.config(yscrollcommand=barra_desplazamiento.set)
        
        self.mostrar_alertas_stock(widget_texto_stock)

    def mostrar_alertas_stock(self, widget_texto):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.nombre_producto, s.minimo, s.maximo, s.total
                FROM producto p JOIN stock s ON p.id_producto = s.id_producto
            ''')
            datos = cursor.fetchall()
            
            widget_texto.config(state=tk.NORMAL)
            widget_texto.delete(1.0, tk.END)
            widget_texto.insert(tk.END, "--- Productos con Stock Bajo / Agotado ---\n\n")

            tiene_stock_bajo = False
            for nombre, minimo, maximo, total in datos:
                umbral_30_porciento = maximo * 0.30
                
                if total <= umbral_30_porciento:
                    tiene_stock_bajo = True
                    if total == 0:
                        estado = "❌ SIN STOCK"
                    else:
                        estado = "⚠️ BAJO STOCK"
                    
                    linea = f"Producto: {nombre}\n"
                    linea += f"Stock Actual: {int(total)} (Estado: {estado})\n"
                    linea += f"---" * 15 + "\n"
                    widget_texto.insert(tk.END, linea)
            
            if not tiene_stock_bajo:
                widget_texto.insert(tk.END, "Todos los productos tienen stock óptimo. ✅\n")
            
            widget_texto.config(state=tk.DISABLED)

        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener la lista de productos: {e}")
        finally:
            if conn:
                conn.close()

    def mostrar_menu_gestion_stock(self):
        ventana_gestion_stock = tk.Toplevel(self.raiz)
        ventana_gestion_stock.title("Gestión de Productos y Stock")
        ventana_gestion_stock.geometry("400x300")

        tk.Label(ventana_gestion_stock, text="Opciones de Gestión", font=("Arial", 14)).pack(pady=10)

        boton_ver = tk.Button(ventana_gestion_stock, text="Ver Productos y Stock", width=30, command=self.mostrar_lista_productos_stock)
        boton_ver.pack(pady=5)

        boton_agregar = tk.Button(ventana_gestion_stock, text="Ingresar Nuevo Producto", width=30, command=self.interfaz_agregar_producto)
        boton_agregar.pack(pady=5)

        boton_modificar = tk.Button(ventana_gestion_stock, text="Modificar Stock", width=30, command=self.interfaz_modificar_stock)
        boton_modificar.pack(pady=5)

        boton_eliminar = tk.Button(ventana_gestion_stock, text="Eliminar Producto", width=30, command=self.interfaz_eliminar_producto)
        boton_eliminar.pack(pady=5)

    def mostrar_lista_productos_stock(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.nombre_producto, p.marca, p.categoria_producto, s.minimo, s.maximo, s.total
                FROM producto p JOIN stock s ON p.id_producto = s.id_producto
            ''')
            datos = cursor.fetchall()
            
            ventana_lista_stock = tk.Toplevel(self.raiz)
            ventana_lista_stock.title("Productos y Stock")
            
            widget_texto = tk.Text(ventana_lista_stock, wrap="word", width=80, height=20)
            widget_texto.pack(pady=10, padx=10)
            widget_texto.insert(tk.END, "--- Lista de Productos y Stock ---\n\n")

            alerta_enviada = False

            for nombre, marca, cat, minimo, maximo, total in datos:
                umbral_30_porciento = maximo * 0.30
                
                linea = f"Nombre: {nombre}\n"
                linea += f"Marca: {marca}, Categoría: {cat}\n"
                linea += f"Stock Mínimo: {minimo}, Stock Máximo: {maximo}, Stock Actual: {total}\n"
                
                if total <= umbral_30_porciento:
                    linea += "Estado: ⚠️ REPONER STOCK\n"
                    if not alerta_enviada:
                        messagebox.showwarning("¡Alerta de Stock!", f"Hay que reponer stock del producto: {nombre}")
                        alerta_enviada = True
                else:
                    linea += "Estado: ✅ Stock óptimo\n"
                
                widget_texto.insert(tk.END, linea)
                widget_texto.insert(tk.END, "-" * 70 + "\n")
            
            widget_texto.config(state=tk.DISABLED)

        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener la lista de productos: {e}")
        finally:
            if conn:
                conn.close()

    def interfaz_agregar_producto(self):
        ventana_agregar = tk.Toplevel(self.raiz)
        ventana_agregar.title("Ingresar Nuevo Producto")
        ventana_agregar.geometry("350x350")
        
        tk.Label(ventana_agregar, text="Nombre del producto:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_agregar)
        entrada_nombre.pack()
        
        tk.Label(ventana_agregar, text="Marca:").pack(pady=5)
        entrada_marca = tk.Entry(ventana_agregar)
        entrada_marca.pack()
        
        tk.Label(ventana_agregar, text="Categoría:").pack(pady=5)
        entrada_categoria = tk.Entry(ventana_agregar)
        entrada_categoria.pack()
        
        tk.Label(ventana_agregar, text="Precio:").pack(pady=5)
        entrada_precio = tk.Entry(ventana_agregar)
        entrada_precio.pack()
        
        tk.Label(ventana_agregar, text="Stock Mínimo:").pack(pady=5)
        entrada_min = tk.Entry(ventana_agregar)
        entrada_min.pack()
        
        tk.Label(ventana_agregar, text="Stock Máximo:").pack(pady=5)
        entrada_max = tk.Entry(ventana_agregar)
        entrada_max.pack()
        
        tk.Label(ventana_agregar, text="Stock Actual:").pack(pady=5)
        entrada_total = tk.Entry(ventana_agregar)
        entrada_total.pack()

        def guardar_producto():
            try:
                nombre = entrada_nombre.get()
                marca = entrada_marca.get()
                cat = entrada_categoria.get()
                precio = float(entrada_precio.get())
                min_stock = int(entrada_min.get())
                max_stock = int(entrada_max.get())
                total_stock = int(entrada_total.get())
                
                if min_stock > max_stock or not (min_stock <= total_stock <= max_stock):
                    messagebox.showerror("Error de validación", "El stock no cumple con los límites establecidos.")
                    return

                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO producto (precio, nombre_producto, marca, categoria_producto)
                    VALUES(?, ?, ?, ?)
                ''', (precio, nombre, marca, cat))
                conn.commit()
                
                id_producto = cursor.lastrowid
                
                cursor.execute('''
                    INSERT INTO stock (minimo, maximo, total, id_producto)
                    VALUES(?, ?, ?, ?)
                ''', (min_stock, max_stock, total_stock, id_producto))
                conn.commit()

                messagebox.showinfo("Éxito", "Producto y stock guardados correctamente.")
                ventana_agregar.destroy()

            except (ValueError, sqlite3.Error) as e:
                messagebox.showerror("Error", f"Error al guardar el producto: {e}")
            finally:
                if conn:
                    conn.close()

        tk.Button(ventana_agregar, text="Guardar", command=guardar_producto).pack(pady=10)

    def interfaz_modificar_stock(self):
        ventana_modificar = tk.Toplevel(self.raiz)
        ventana_modificar.title("Modificar Stock")
        ventana_modificar.geometry("350x250")

        tk.Label(ventana_modificar, text="Nombre del producto a modificar:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_modificar)
        entrada_nombre.pack()
        
        tk.Label(ventana_modificar, text="Marca del producto:").pack(pady=5)
        entrada_marca = tk.Entry(ventana_modificar)
        entrada_marca.pack()
        
        tk.Label(ventana_modificar, text="Nuevo stock:").pack(pady=5)
        entrada_nuevo_stock = tk.Entry(ventana_modificar)
        entrada_nuevo_stock.pack()

        def actualizar_stock():
            try:
                nombre = entrada_nombre.get()
                marca = entrada_marca.get()
                nuevo_stock = int(entrada_nuevo_stock.get())

                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?", (nombre, marca))
                producto = cursor.fetchone()
                
                if not producto:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return

                id_prod = producto[0]
                
                cursor.execute("UPDATE stock SET total = ? WHERE id_producto = ?", (nuevo_stock, id_prod))
                conn.commit()
                messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
                ventana_modificar.destroy()
            except (ValueError, sqlite3.Error) as e:
                messagebox.showerror("Error", f"Error al actualizar el stock: {e}")
            finally:
                if conn:
                    conn.close()
        
        tk.Button(ventana_modificar, text="Actualizar Stock", command=actualizar_stock).pack(pady=10)

    def interfaz_eliminar_producto(self):
        ventana_eliminar = tk.Toplevel(self.raiz)
        ventana_eliminar.title("Eliminar Producto")
        ventana_eliminar.geometry("300x180")
        
        tk.Label(ventana_eliminar, text="Nombre del producto a eliminar:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_eliminar)
        entrada_nombre.pack()
        
        tk.Label(ventana_eliminar, text="Marca del producto:").pack(pady=5)
        entrada_marca = tk.Entry(ventana_eliminar)
        entrada_marca.pack()
        
        def eliminar_producto():
            try:
                nombre = entrada_nombre.get()
                marca = entrada_marca.get()
                
                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?", (nombre, marca))
                producto = cursor.fetchone()
                
                if not producto:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return
                
                id_prod = producto[0]

                cursor.execute("DELETE FROM stock WHERE id_producto = ?", (id_prod,))
                cursor.execute("DELETE FROM producto WHERE id_producto = ?", (id_prod,))
                conn.commit()
                
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                ventana_eliminar.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al eliminar el producto: {e}")
            finally:
                if conn:
                    conn.close()
        
        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar_producto).pack(pady=10)

    def mostrar_menu_calcular_stock(self):
        ventana_cal_stock = tk.Toplevel(self.raiz)
        ventana_cal_stock.title("Calcular Stock")
        ventana_cal_stock.geometry("350x200")

        tk.Label(ventana_cal_stock, text="Opciones de Cálculo de Stock", font=("Arial", 14)).pack(pady=10)
        
        boton_total = tk.Button(ventana_cal_stock, text="Calcular Stock Total", width=25, command=self.calcular_stock_total)
        boton_total.pack(pady=5)
        
        boton_categoria = tk.Button(ventana_cal_stock, text="Calcular Stock por Categoría", width=25, command=self.calcular_stock_por_categoria)
        boton_categoria.pack(pady=5)

    def calcular_stock_total(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total) FROM stock")
            total = cursor.fetchone()[0]

            messagebox.showinfo("Stock Total", f"El stock total de todos los productos es: {int(total) if total else 0}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al calcular el stock total: {e}")
        finally:
            if conn:
                conn.close()

    def calcular_stock_por_categoria(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT DISTINCT categoria_producto FROM producto")
            categorias = [cat[0] for cat in cursor.fetchall()]
            
            ventana_categoria = tk.Toplevel(self.raiz)
            ventana_categoria.title("Stock por Categoría")
            ventana_categoria.geometry("300x200")

            def mostrar_stock_para_categoria(categoria):
                try:
                    conn_interior = sqlite3.connect('blackiron.db')
                    cursor_interior = conn_interior.cursor()
                    cursor_interior.execute("""
                        SELECT SUM(s.total)
                        FROM stock s INNER JOIN producto p ON s.id_producto = p.id_producto
                        WHERE p.categoria_producto = ?
                    """, (categoria,))
                    total_cat = cursor_interior.fetchone()[0]
                    messagebox.showinfo("Stock por Categoría", f"El stock total para '{categoria}' es: {int(total_cat) if total_cat else 0}")
                except sqlite3.Error as e:
                    messagebox.showerror("Error de BD", f"Error al calcular el stock: {e}")
                finally:
                    if conn_interior:
                        conn_interior.close()
                    ventana_categoria.destroy()

            tk.Label(ventana_categoria, text="Selecciona una categoría:", font=("Arial", 12)).pack(pady=10)
            
            if not categorias:
                tk.Label(ventana_categoria, text="No hay categorías disponibles.").pack()
            else:
                for cat in categorias:
                    tk.Button(ventana_categoria, text=cat, command=lambda c=cat: mostrar_stock_para_categoria(c)).pack(pady=2)

        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener categorías: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionBlackIron(raiz)
    raiz.mainloop()
