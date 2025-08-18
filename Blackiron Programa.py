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
            id_producto INTEGER PRIMARY KEY,
            precio REAL,
            nombre_producto TEXT,
            marca TEXT,
            categoria_producto TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            minimo INT,
            maximo INT,
            total INT,
            id_producto INTEGER,
            FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            DNI INTEGER PRIMARY KEY,
            gmail TEXT,
            direccion TEXT,
            apellido TEXT,
            nombre TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factura (
            id_factura INTEGER PRIMARY KEY,
            total INTEGER,
            DNI INTEGER,
            FOREIGN KEY(DNI) REFERENCES cliente(DNI)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido INTEGER PRIMARY KEY,
            estado TEXT,
            id_factura INTEGER,
            FOREIGN KEY(id_factura) REFERENCES factura(id_factura)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            contrasenia TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kits (
            nombre TEXT PRIMARY KEY,
            precio REAL
        )
    """)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conjuntar(
            id INTEGER PRIMARY KEY,
            id_kit TEXT,
            id_producto INT,
            FOREIGN KEY (id_kit) REFERENCES kits(nombre),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS llevar(
            id INTEGER PRIMARY KEY,
            id_pedido INT,
            cantidad INT,
            id_producto INT,
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedido_kit(
            id INTEGER PRIMARY KEY,
            id_pedido INT,
            cantidad INT,
            id_kit TEXT,
            FOREIGN KEY (id_kit) REFERENCES kits(nombre),
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        )
    ''')
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
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (25000, 'Proteína de suero', 'Optimum Nutrition', 'Suplemento')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (12000, 'Creatina monohidratada', 'Universal Nutrition', 'Suplemento')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (1500, 'Guantes de entrenamiento', 'Nike', 'Accesorio')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (30000, 'BCAA en polvo', 'MuscleTech', 'Suplemento')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (78000, 'Banco Plano de Pesas', 'Cap Barbell', 'Equipo')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (19500, 'Glutamina en Polvo', 'nowSports', 'Suplemento')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (5000, 'Mancuerna 10kg', 'Everlast', 'Pesas')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (8000, 'Barra olímpica', 'Rogue', 'Pesas')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (2000, 'Colchoneta antideslizante', 'Reebok', 'Yoga')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (3500, 'Soga para saltar', 'Adidas', 'Cardio')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (15000, 'Bicicleta fija', 'SpinningPro', 'Cardio')")
        cursor.execute("INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (7000, 'Kettlebell 16kg', 'Kong', 'Pesas')")
        
    cursor.execute("SELECT COUNT(*) FROM stock")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 50, 30, 1)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (5, 20, 15, 2)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (20, 100, 50, 3)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (8, 40, 25, 4)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (0, 50, 30, 5)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (0, 100, 80, 6)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (5, 30, 12, 7)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (2, 20, 8, 8)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 50, 25, 9)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (10, 40, 18, 10)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (1, 10, 4, 11)")
        cursor.execute("INSERT INTO stock (minimo, maximo, total, id_producto) VALUES (3, 25, 10, 12)")

    cursor.execute("SELECT COUNT(*) FROM cliente")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO cliente (DNI, gmail, direccion, apellido, nombre) VALUES (12345678, 'cliente1@mail.com', 'Calle Falsa 123', 'Diaz', 'Carlos')")
        
    cursor.execute("SELECT COUNT(*) FROM factura")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO factura (DNI, total) VALUES (12345678, 15050)")
        
    cursor.execute("SELECT COUNT(*) FROM pedido")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pedido (estado, id_factura) VALUES ('entregado', 1)")

    cursor.execute("SELECT COUNT(*) FROM kits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Cardio', 9500)")
        cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Yoga', 13500)")
        cursor.execute("INSERT INTO kits (nombre, precio) VALUES ('Fuerza', 22000)")

    cursor.execute("SELECT COUNT(*) FROM conjuntar")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Cardio', 10)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Cardio', 11)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Yoga', 9)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Yoga', 10)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 7)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 8)")
        cursor.execute("INSERT INTO conjuntar (id_kit, id_producto) VALUES ('Fuerza', 12)")
    
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

        boton_tomar_pedido = tk.Button(self.raiz, text="Tomar Pedido (Ventas)", width=25, command=self.toma_pedido)
        boton_tomar_pedido.pack(pady=5)
        
        boton_procesar_compra = tk.Button(self.raiz, text="Procesar Compra", width=25, command=self.compra)
        boton_procesar_compra.pack(pady=5)
        
        boton_cancelar_compra = tk.Button(self.raiz, text="Cancelar Compra", width=25, command=self.c_compra)
        boton_cancelar_compra.pack(pady=5)
        
        boton_pedidos = tk.Button(self.raiz, text="Visualizar Pedidos", width=25, command=self.mostrar_pedidos)
        boton_pedidos.pack(pady=5)
        
        boton_kits = tk.Button(self.raiz, text="Ver Kits", width=25, command=self.mostrar_kits)
        boton_kits.pack(pady=5)
        boton_gestion_kits = tk.Button(self.raiz, text="Gestión de Kits (Nuevo)", width=25, command=self.menu_kits_nuevo)
        boton_gestion_kits.pack(pady=5)

        separador = tk.Frame(self.raiz, height=2, bd=1, relief=tk.SUNKEN)
        separador.pack(fill=tk.X, padx=20, pady=10)
        
        etiqueta_gestion_stock = tk.Label(self.raiz, text="Gestión de Stock", font=("Arial", 12))
        etiqueta_gestion_stock.pack(pady=5)

        boton_gestionar_stock = tk.Button(self.raiz, text="Gestión de Stock", width=25, command=self.mostrar_menu_stock)
        boton_gestionar_stock.pack(pady=5)
        
        boton_cal_stock = tk.Button(self.raiz, text="Calcular Stock General", width=25, command=self.mostrar_menu_calcular_stock)
        boton_cal_stock.pack(pady=5)

        separador2 = tk.Frame(self.raiz, height=2, bd=1, relief=tk.SUNKEN)
        separador2.pack(fill=tk.X, padx=20, pady=10)

        boton_cerrar = tk.Button(self.raiz, text="Cerrar Sesión", width=25, command=self.mostrar_pantalla_inicio_sesion)
        boton_cerrar.pack(pady=10)

    def mostrar_menu_stock(self):
        ventana_stock_menu = tk.Toplevel(self.raiz)
        ventana_stock_menu.title("Menú de Stock")
        ventana_stock_menu.geometry("300x250")
        
        tk.Label(ventana_stock_menu, text="Opciones de Stock", font=("Arial", 14)).pack(pady=10)
        
        boton_ver_stock = tk.Button(ventana_stock_menu, text="Ver Productos y Stock", width=25, command=self.interfaz_filtro_productos)
        boton_ver_stock.pack(pady=5)

        boton_agregar = tk.Button(ventana_stock_menu, text="Ingresar Nuevo Producto", width=25, command=self.interfaz_agregar_producto)
        boton_agregar.pack(pady=5)
        
        boton_modificar = tk.Button(ventana_stock_menu, text="Modificar Stock de Producto", width=25, command=self.interfaz_modificar_stock)
        boton_modificar.pack(pady=5)

        boton_eliminar = tk.Button(ventana_stock_menu, text="Eliminar Producto", width=25, command=self.interfaz_eliminar_producto)
        boton_eliminar.pack(pady=5)

    def mostrar_pedidos(self):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT p.id_pedido, p.estado, c.cantidad, pr.nombre_producto, f.id_factura FROM pedido p INNER JOIN llevar c ON p.id_pedido = c.id_pedido INNER JOIN producto pr ON c.id_producto = pr.id_producto INNER JOIN factura f ON p.id_factura = f.id_factura")
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
            
            cursor.execute("""
                SELECT k.nombre, p.nombre_producto
                FROM kits k
                JOIN conjuntar c ON k.nombre = c.id_kit
                JOIN producto p ON c.id_producto = p.id_producto
                ORDER BY k.nombre
            """)
            datos_kits = cursor.fetchall()

            ventana_kits = tk.Toplevel(self.raiz)
            ventana_kits.title("Ver Kits")

            widget_texto = tk.Text(ventana_kits, wrap="word", width=50, height=15)
            widget_texto.pack(pady=10, padx=10)

            widget_texto.insert(tk.END, "Nombre del Kit | Producto\n")
            widget_texto.insert(tk.END, "--------------------------------------------------\n")

            if datos_kits:
                kits_agrupados = {}
                for kit, producto in datos_kits:
                    if kit not in kits_agrupados:
                        kits_agrupados[kit] = []
                    kits_agrupados[kit].append(producto)

                for kit, productos in kits_agrupados.items():
                    widget_texto.insert(tk.END, f"Kit: {kit}\n")
                    for producto in productos:
                        widget_texto.insert(tk.END, f"  - {producto}\n")
                    widget_texto.insert(tk.END, "--------------------------------------------------\n")
            else:
                widget_texto.insert(tk.END, "No se encontraron kits en la base de datos.")
            
            widget_texto.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al obtener kits: {e}")
        finally:
            if conn:
                conn.close()

    def toma_pedido(self):
        dni = simpledialog.askinteger("Datos del Cliente", "Ingrese el DNI o documento de identidad:", minvalue=100000, maxvalue=999999999)
        if not dni: return
        
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()

        cursor.execute("SELECT DNI FROM cliente WHERE DNI = ?", (dni,))
        existe_cliente = cursor.fetchone()

        if not existe_cliente:
            nombre = simpledialog.askstring("Datos del Cliente", "Ingrese el nombre:")
            apellido = simpledialog.askstring("Datos del Cliente", "Ingrese el apellido:")
            direccion = simpledialog.askstring("Datos del Cliente", "Ingrese la dirección:")
            gmail = simpledialog.askstring("Datos del Cliente", "Ingrese el gmail:")
            
            if not all([nombre, apellido, direccion, gmail]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                conn.close()
                return

            if '@' not in gmail:
                messagebox.showerror("Error", "El gmail debe contener '@'.")
                conn.close()
                return

            try:
                cursor.execute("INSERT INTO cliente VALUES(?, ?, ?, ?, ?)", (dni, gmail, direccion, apellido, nombre))
                conn.commit()
                messagebox.showinfo("Cliente", "Cliente nuevo registrado con éxito.")
            except sqlite3.Error as e:
                messagebox.showerror("Error de BD", f"Error al registrar cliente: {e}")
                conn.close()
                return
        
        try:
            fac = messagebox.askyesno("Factura", "¿Ya tiene una factura en curso?")
            if fac:
                id_factura = simpledialog.askinteger("Factura Existente", "Ingrese la ID de su factura:")
                cursor.execute("SELECT id_factura FROM factura WHERE id_factura = ? AND DNI = ?", (id_factura, dni))
                test = cursor.fetchone()
                if test:
                    self.seguir_pedido(id_factura, dni)
                else:
                    messagebox.showerror("Error", "ID de factura no encontrada o no coincide con el DNI.")
            else:
                self.crear_nuevo_pedido(dni, conn, cursor)
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
        finally:
            conn.close()

    def crear_nuevo_pedido(self, dni, conn, cursor):
        total = 0
        opcion = simpledialog.askinteger("Tipo de Pedido", "1-Producto(s)\n2-Kit(s)\n3-Producto(s)+Kit(s)", minvalue=1, maxvalue=3)
        if not opcion: return

        if opcion == 1:
            try:
                cant = simpledialog.askinteger("Cantidad de Productos", "¿De cuántos productos diferentes es el pedido?:")
                if not cant: return
                
                listPro = {}
                listCant = []
                for i in range(cant):
                    nombre = simpledialog.askstring("Producto", f"Ingrese el nombre del producto {i+1}:")
                    marca = simpledialog.askstring("Producto", f"Ingrese la marca del producto {i+1}:")
                    canti = simpledialog.askinteger("Producto", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT minimo, total FROM stock WHERE id_producto IN (SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?)", (nombre, marca))
                    estok = cursor.fetchone()
                    actual = estok[1]
                    minimo = estok[0]
                    if actual - canti < minimo:
                        messagebox.showerror("Error.", f"No hay suficiente stock de {nombre}, {marca}")
                        return
                    if not all([nombre, marca, canti]): return
                    

                    nombre_limpio = nombre.strip().lower()
                    marca_limpia = marca.strip().lower()

                    listPro[nombre_limpio] = marca_limpia
                    listCant.append(canti)
                    

                    cursor.execute("SELECT precio FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre_limpio, marca_limpia))
                    p = cursor.fetchone()
                    if p:
                        total += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Producto {nombre} no encontrado.")
                        return
                self.guardar_pedido(dni, total, listPro, listCant, "producto", conn, cursor)
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar el pedido de productos: {e}")

        elif opcion == 2:
            try:
                cant = simpledialog.askinteger("Cantidad de Kits", "¿De cuántos kits diferentes es el pedido?:")
                if not cant: return
                
                listKit = []
                listCant = []
                for i in range(cant):
                    nombre = simpledialog.askstring("Kit", f"Ingrese el nombre del kit {i+1}:")
                    canti = simpledialog.askinteger("Kit", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT id_producto FROM producto WHERE id_producto IN(SELECT id_producto FROM conjuntar WHERE id_kit = ?)", (nombre,))
                    nombres = cursor.fetchall()
                    for a in nombres:
                        ida = a[0]
                        cursor.execute("SELECT id_producto, COUNT(*) FROM conjuntar WHERE id_producto = ? AND id_kit = ?", (ida, nombre))
                        dat = cursor.fetchall()
                        for i in dat:
                            id, xkit = i
                            cursor.execute("SELECT minimo, total FROM stock WHERE id_producto = ?", (id,))
                            estok = cursor.fetchone()
                            actual = estok[1]
                            minimo = estok[0]
                            if actual - (canti * xkit) < minimo:
                                cursor.execute("SELECT nombre_producto, marca FROM producto WHERE id_producto = ?", (id,))
                                dP = cursor.fetchone()
                                noo = dP[0]
                                maa = dP[1]
                                messagebox.showerror("Error.", f"No hay suficiente stock de {noo}, {maa}.")
                                return
                    if not all([nombre, canti]): return
                    

                    nombre_limpio = nombre.strip().lower()

                    listKit.append(nombre_limpio)
                    listCant.append(canti)
                    

                    cursor.execute("SELECT precio FROM kits WHERE LOWER(nombre) = ?", (nombre_limpio,))
                    p = cursor.fetchone()
                    if p:
                        total += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Kit {nombre} no encontrado.")
                        return

                self.guardar_pedido(dni, total, listKit, listCant, "kit", conn, cursor)
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar el pedido de kits: {e}")

        elif opcion == 3:
            try:
                totalK = 0
                totalP = 0
                listPro = {}
                listKit = []
                listCantP = []
                listCantK = []

                kits = simpledialog.askinteger("Pedido Combinado", "¿Cuántos kits va a encargar?:")
                if not kits: return
                for i in range(kits):
                    nombre = simpledialog.askstring("Kit", "Ingrese el nombre del kit:")
                    cantid = simpledialog.askinteger("Kit", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT id_producto FROM producto WHERE id_producto IN(SELECT id_producto FROM conjuntar WHERE id_kit = ?)", (nombre,))
                    nombres = cursor.fetchall()
                    for a in nombres:
                        ida = a[0]
                        cursor.execute("SELECT id_producto, COUNT(*) FROM conjuntar WHERE id_producto = ? AND id_kit = ?", (ida, nombre))
                        dat = cursor.fetchall()
                        for i in dat:
                            id, xkit = i
                            cursor.execute("SELECT minimo, total FROM stock WHERE id_producto = ?", (id,))
                            estok = cursor.fetchone()
                            actual = estok[1]
                            minimo = estok[0]
                            if actual - (cantid * xkit) < minimo:
                                cursor.execute("SELECT nombre_producto, marca FROM producto WHERE id_producto = ?", (id,))
                                dP = cursor.fetchone()
                                noo = dP[0]
                                maa = dP[1]
                                messagebox.showerror("Error.", f"No hay suficiente stock de {noo}, {maa}.")
                                return
                    if not all([nombre, cantid]): return
                    

                    nombre_limpio = nombre.strip().lower()

                    listKit.append(nombre_limpio)
                    listCantK.append(cantid)
                    
                 
                    cursor.execute("SELECT precio FROM kits WHERE LOWER(nombre) = ?", (nombre_limpio,))
                    pK = cursor.fetchone()
                    if pK:
                        totalK += pK[0] * cantid
                    else:
                        messagebox.showerror("Error", f"Kit {nombre} no encontrado.")
                        return

                productos = simpledialog.askinteger("Pedido Combinado", "¿Cuántos productos va a encargar?:")
                if not productos: return
                for i in range(productos):
                    nombre = simpledialog.askstring("Producto", f"Ingrese el nombre del producto {i+1}:")
                    marca = simpledialog.askstring("Producto", f"Ingrese la marca del producto {i+1}:")
                    canti = simpledialog.askinteger("Producto", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT minimo, total FROM stock WHERE id_producto IN (SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?)", (nombre, marca))
                    estok = cursor.fetchone()
                    actual = estok[1]
                    minimo = estok[0]
                    if actual - canti < minimo:
                        messagebox.showerror("Error.", f"No hay suficiente stock de {nombre}, {marca}")
                        return
                    if not all([nombre, marca, canti]): return

                    nombre_limpio = nombre.strip().lower()
                    marca_limpia = marca.strip().lower()

                    listPro[nombre_limpio] = marca_limpia
                    listCantP.append(canti)
                    

                    cursor.execute("SELECT precio FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre_limpio, marca_limpia))
                    p = cursor.fetchone()
                    if p:
                        totalP += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Producto {nombre} no encontrado.")
                        return

                total = totalK + totalP
                self.guardar_pedido_combinado(dni, total, listPro, listCantP, listKit, listCantK, conn, cursor)
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar el pedido combinado: {e}")
    
    def guardar_pedido(self, dni, total, list_items, list_cant, tipo, conn, cursor):
        try:
            cursor.execute("INSERT INTO factura(total, DNI) VALUES(?, ?)", (total, dni))
            id_factura = cursor.lastrowid
            cursor.execute("INSERT INTO pedido(estado, id_factura) VALUES('En armado', ?)", (id_factura,))
            id_pedido = cursor.lastrowid

            
            if tipo == "producto":
                productos_items = list(list_items.items())
                for i in range(len(productos_items)):
                    nombre, marca = productos_items[i]
                    cantidad = list_cant[i]
                    cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre, marca))
                    id_producto = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO llevar(id_pedido, cantidad, id_producto) VALUES(?, ?, ?)", (id_pedido, cantidad, id_producto))
            elif tipo == "kit":
                for i in range(len(list_items)):
                    nombre = list_items[i]
                    cantidad = list_cant[i]
                    cursor.execute("SELECT nombre FROM kits WHERE LOWER(nombre) = ?", (nombre,))
                    id_kit = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO pedido_kit(id_pedido, cantidad, id_kit) VALUES(?, ?, ?)", (id_pedido, cantidad, id_kit))
            conn.commit()
            self.mostrar_factura(id_factura, conn, cursor)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al guardar el pedido: {e}")

    def guardar_pedido_combinado(self, dni, total, listPro, listCantP, listKit, listCantK, conn, cursor):
        try:
            cursor.execute("INSERT INTO factura(total, DNI) VALUES(?, ?)", (total, dni))
            id_factura = cursor.lastrowid
            cursor.execute("INSERT INTO pedido(estado, id_factura) VALUES('En armado', ?)", (id_factura,))
            id_pedido = cursor.lastrowid

            for n, c in zip(listKit, listCantK):
                cursor.execute("SELECT nombre FROM kits WHERE LOWER(nombre) = ?", (n,))
                id_kit = cursor.fetchone()[0]
                cursor.execute("INSERT INTO pedido_kit(id_pedido, cantidad, id_kit) VALUES(?, ?, ?)", (id_pedido, c, id_kit))

            productos_items = list(listPro.items())
            for n, (nombre, marca) in zip(listCantP, productos_items):
                cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre, marca))
                idPr = cursor.fetchone()[0]
                cursor.execute("INSERT INTO llevar(id_pedido, cantidad, id_producto) VALUES(?, ?, ?)", (id_pedido, n, idPr))
                
            conn.commit()
            self.mostrar_factura(id_factura, conn, cursor)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al guardar el pedido combinado: {e}")

    def mostrar_factura(self, id_factura, conn, cursor):
        cursor.execute("SELECT * FROM factura WHERE id_factura = ?", (id_factura,))
        datosFa = cursor.fetchone()
        id, tot, dn= datosFa
        
        info = f"DATOS DE SU FACTURA:\nID: {id}\nMONTO TOTAL: {tot}\nDNI del comprador: {dn}"
        messagebox.showinfo("Factura Generada", info)

        deseo = messagebox.askyesno("Continuar", "¿Desea agregar más pedidos a su factura?")
        if deseo:
            self.seguir_pedido(id_factura, dn)

    def seguir_pedido(self, id_factura, dni):
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        
        opcion = simpledialog.askinteger("Agregar a Factura", "1-Producto(s)\n2-Kit(s)\n3-Producto(s)+Kit(s)", minvalue=1, maxvalue=3)
        if not opcion:
            conn.close()
            return
            
        total = 0
        try:
            if opcion == 1:
                cant = simpledialog.askinteger("Cantidad de Productos", "¿De cuántos productos diferentes es el pedido?:")
                if not cant: return
                
                listPro = {}
                listCant = []
                for i in range(cant):
                    nombre = simpledialog.askstring("Producto", f"Ingrese el nombre del producto {i+1}:")
                    marca = simpledialog.askstring("Producto", f"Ingrese la marca del producto {i+1}:")
                    canti = simpledialog.askinteger("Producto", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT minimo, total FROM stock WHERE id_producto IN (SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?)", (nombre, marca))
                    estok = cursor.fetchone()
                    actual = estok[1]
                    minimo = estok[0]
                    if actual - canti < minimo:
                        messagebox.showerror("Error.", f"No hay suficiente stock de {nombre}, {marca}")
                        return
                    if not all([nombre, marca, canti]): return
                    
     
                    nombre_limpio = nombre.strip().lower()
                    marca_limpia = marca.strip().lower()

                    listPro[nombre_limpio] = marca_limpia
                    listCant.append(canti)
                    
            
                    cursor.execute("SELECT precio FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre_limpio, marca_limpia))
                    p = cursor.fetchone()
                    if p:
                        total += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Producto {nombre} no encontrado.")
                        return

                self.agregar_a_factura(id_factura, total, listPro, listCant, "producto", conn, cursor)

            elif opcion == 2:
                cant = simpledialog.askinteger("Cantidad de Kits", "¿De cuántos kits diferentes es el pedido?:")
                if not cant: return
                
                listKit = []
                listCant = []
                for i in range(cant):
                    nombre = simpledialog.askstring("Kit", f"Ingrese el nombre del kit {i+1}:")
                    canti = simpledialog.askinteger("Kit", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT id_producto FROM producto WHERE id_producto IN(SELECT id_producto FROM conjuntar WHERE id_kit = ?)", (nombre,))
                    nombres = cursor.fetchall()
                    for a in nombres:
                        ida = a[0]
                        cursor.execute("SELECT id_producto, COUNT(*) FROM conjuntar WHERE id_producto = ? AND id_kit = ?", (ida, nombre))
                        dat = cursor.fetchall()
                        for i in dat:
                            id, xkit = i
                            cursor.execute("SELECT minimo, total FROM stock WHERE id_producto = ?", (id,))
                            estok = cursor.fetchone()
                            actual = estok[1]
                            minimo = estok[0]
                            if actual - (canti * xkit) < minimo:
                                cursor.execute("SELECT nombre_producto, marca FROM producto WHERE id_producto = ?", (id,))
                                dP = cursor.fetchone()
                                noo = dP[0]
                                maa = dP[1]
                                messagebox.showerror("Error.", f"No hay suficiente stock de {noo}, {maa}.")
                                return
                    if not all([nombre, canti]): return
                    
             
                    nombre_limpio = nombre.strip().lower()

                    listKit.append(nombre_limpio)
                    listCant.append(canti)
           
                    cursor.execute("SELECT precio FROM kits WHERE LOWER(nombre) = ?", (nombre_limpio,))
                    p = cursor.fetchone()
                    if p:
                        total += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Kit {nombre} no encontrado.")
                        return

                self.agregar_a_factura(id_factura, total, listKit, listCant, "kit", conn, cursor)
            
            elif opcion == 3:
                totalK = 0
                totalP = 0
                listPro = {}
                listKit = []
                listCantP = []
                listCantK = []

                kits = simpledialog.askinteger("Pedido Combinado", "¿Cuántos kits va a encargar?:")
                if not kits: return
                for i in range(kits):
                    nombre = simpledialog.askstring("Kit", "Ingrese el nombre del kit:")
                    cantid = simpledialog.askinteger("Kit", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT id_producto FROM producto WHERE id_producto IN(SELECT id_producto FROM conjuntar WHERE id_kit = ?)", (nombre,))
                    nombres = cursor.fetchall()
                    for a in nombres:
                        ida = a[0]
                        cursor.execute("SELECT id_producto, COUNT(*) FROM conjuntar WHERE id_producto = ? AND id_kit = ?", (ida, nombre))
                        dat = cursor.fetchall()
                        for i in dat:
                            id, xkit = i
                            cursor.execute("SELECT minimo, total FROM stock WHERE id_producto = ?", (id,))
                            estok = cursor.fetchone()
                            actual = estok[1]
                            minimo = estok[0]
                            if actual - (cantid * xkit) < minimo:
                                cursor.execute("SELECT nombre_producto, marca FROM producto WHERE id_producto = ?", (id,))
                                dP = cursor.fetchone()
                                noo = dP[0]
                                maa = dP[1]
                                messagebox.showerror("Error.", f"No hay suficiente stock de {noo}, {maa}.")
                                return
                    if not all([nombre, cantid]): return
                    
   
                    nombre_limpio = nombre.strip().lower()

                    listKit.append(nombre_limpio)
                    listCantK.append(cantid)
                    
 
                    cursor.execute("SELECT precio FROM kits WHERE LOWER(nombre) = ?", (nombre_limpio,))
                    pK = cursor.fetchone()
                    if pK:
                        totalK += pK[0] * cantid
                    else:
                        messagebox.showerror("Error", f"Kit {nombre} no encontrado.")
                        return

                productos = simpledialog.askinteger("Pedido Combinado", "¿Cuántos productos va a encargar?:")
                if not productos: return
                for i in range(productos):
                    nombre = simpledialog.askstring("Producto", f"Ingrese el nombre del producto {i+1}:")
                    marca = simpledialog.askstring("Producto", f"Ingrese la marca del producto {i+1}:")
                    canti = simpledialog.askinteger("Producto", "¿Cuánta cantidad?:")
                    cursor.execute("SELECT minimo, total FROM stock WHERE id_producto IN (SELECT id_producto FROM producto WHERE nombre_producto = ? AND marca = ?)", (nombre, marca))
                    estok = cursor.fetchone()
                    actual = estok[1]
                    minimo = estok[0]
                    if actual - canti < minimo:
                        messagebox.showerror("Error.", f"No hay suficiente stock de {nombre}, {marca}")
                        return
                    if not all([nombre, marca, canti]): return
                    

                    nombre_limpio = nombre.strip().lower()
                    marca_limpia = marca.strip().lower()

                    listPro[nombre_limpio] = marca_limpia
                    listCantP.append(canti)
                    
              
                    cursor.execute("SELECT precio FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre_limpio, marca_limpia))
                    p = cursor.fetchone()
                    if p:
                        totalP += p[0] * canti
                    else:
                        messagebox.showerror("Error", f"Producto {nombre} no encontrado.")
                        return

                total = totalK + totalP
                self.agregar_combinado_a_factura(id_factura, total, listPro, listCantP, listKit, listCantK, conn, cursor)
        
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
        finally:
            conn.close()

    def agregar_a_factura(self, id_factura, total_adicional, list_items, list_cant, tipo, conn, cursor):
        try:
            cursor.execute("UPDATE factura SET total = total + ? WHERE id_factura = ?", (total_adicional, id_factura))
            cursor.execute("INSERT INTO pedido(estado, id_factura) VALUES('En armado', ?)", (id_factura,))
            id_pedido = cursor.lastrowid
            
            if tipo == "producto":
                productos_items = list(list_items.items())
                for i in range(len(productos_items)):
                    nombre, marca = productos_items[i]
                    cantidad = list_cant[i]
                    cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre, marca))
                    id_producto = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO llevar(id_pedido, cantidad, id_producto) VALUES(?, ?, ?)", (id_pedido, cantidad, id_producto))
            elif tipo == "kit":
                for i in range(len(list_items)):
                    nombre = list_items[i]
                    cantidad = list_cant[i]
                    cursor.execute("SELECT nombre FROM kits WHERE LOWER(nombre) = ?", (nombre,))
                    id_kit = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO pedido_kit(id_pedido, cantidad, id_kit) VALUES(?, ?, ?)", (id_pedido, cantidad, id_kit))
            
            conn.commit()
            self.mostrar_factura(id_factura, conn, cursor)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al agregar al pedido: {e}")

    def agregar_combinado_a_factura(self, id_factura, total, listPro, listCantP, listKit, listCantK, conn, cursor):
        try:
            cursor.execute("UPDATE factura SET total = total + ? WHERE id_factura = ?", (total, id_factura))
            cursor.execute("INSERT INTO pedido(estado, id_factura) VALUES('En armado', ?)", (id_factura,))
            id_pedido = cursor.lastrowid

            for n, c in zip(listKit, listCantK):
                cursor.execute("SELECT nombre FROM kits WHERE LOWER(nombre) = ?", (n,))
                id_kit = cursor.fetchone()[0]
                cursor.execute("INSERT INTO pedido_kit(id_pedido, cantidad, id_kit) VALUES(?, ?, ?)", (id_pedido, c, id_kit))

            productos_items = list(listPro.items())
            for n, (nombre, marca) in zip(listCantP, productos_items):
                cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre, marca))
                idPr = cursor.fetchone()[0]
                cursor.execute("INSERT INTO llevar(id_pedido, cantidad, id_producto) VALUES(?, ?, ?)", (id_pedido, n, idPr))
                
            conn.commit()
            self.mostrar_factura(id_factura, conn, cursor)
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al agregar el pedido combinado: {e}")

    def compra(self):
        id_factura = simpledialog.askinteger("Procesar Compra", "Ingrese la ID de la factura a procesar:", minvalue=1)
        if not id_factura: return

        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM factura WHERE id_factura = ?", (id_factura,))
            dF = cursor.fetchone()
            if not dF:
                messagebox.showerror("Error", "Factura no encontrada.")
                return

            idF, total, dn= dF
            cursor.execute("SELECT estado FROM pedido WHERE id_factura = ?", (id_factura,))
            estado = cursor.fetchone()
            estado = estado[0]
            if estado == 'Vendido':
                messagebox.showerror("Error", "Esta factura ya ha sido vendida.")
                return

            info = f"ID de la factura: {idF}\nMonto total: {total}\nDNI: {dn}"
            vD = messagebox.askyesno("Confirmación", f"¿Son estos datos correctos?\n\n{info}")
            
            if vD:

                cursor.execute("UPDATE pedido SET estado = 'Vendido' WHERE id_factura = ?", (id_factura,))


                cursor.execute("""
                    SELECT id_producto, SUM(cantidad) FROM llevar
                    WHERE id_pedido IN(SELECT id_pedido FROM pedido WHERE id_factura = ?)
                    GROUP BY id_producto
                """, (id_factura,))
                ic = cursor.fetchall()
                for idP, cant in ic:
                    cursor.execute("SELECT minimo, total FROM stock WHERE id_producto = ?", (idP,))
                    estok = cursor.fetchone()
                    actual = estok[1]
                    minimo = estok[0]
                    if actual - cant < minimo:
                        cursor.execute("SELECT nombre_producto, marca FROM producto WHERE id_producto = ?", (idP,))
                        dP = cursor.fetchone()
                        noo = dP[0]
                        maa = dP[1]
                        messagebox.showerror("Error.", f"No hay suficiente stock de {noo}, {maa}.")
                        return
                    cursor.execute("UPDATE stock SET total = total - ? WHERE id_producto = ?", (cant, idP))


                cursor.execute("""
                    SELECT id_kit, cantidad FROM pedido_kit
                    WHERE id_pedido IN(SELECT id_pedido FROM pedido WHERE id_factura = ?)
                """, (id_factura,))
                kic = cursor.fetchall()
                for idK, cant_kit in kic:
                    cursor.execute("SELECT id_producto FROM conjuntar WHERE LOWER(id_kit) = ?", (idK.lower(),))
                    productos_kit = cursor.fetchall()
                    for prod in productos_kit:
                        id_producto_en_kit = prod[0]
                        cursor.execute("""
                            SELECT COUNT(id_producto) FROM conjuntar
                            WHERE LOWER(id_kit) = ? AND id_producto = ?
                        """, (idK.lower(), id_producto_en_kit))
                        cantidad_en_kit = cursor.fetchone()[0]
                        cantidad_total_a_descontar = cant_kit * cantidad_en_kit
                        cursor.execute("UPDATE stock SET total = total - ? WHERE id_producto = ?", (cantidad_total_a_descontar, id_producto_en_kit))
                
                conn.commit()
                messagebox.showinfo("Éxito", "La compra se procesó correctamente.")
            else:
                messagebox.showinfo("Cancelado", "Compra cancelada.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al procesar la compra: {e}")
        finally:
            if conn:
                conn.close()

    def c_compra(self):
        id_factura = simpledialog.askinteger("Cancelar Compra", "Ingrese la ID de la factura a cancelar:", minvalue=1)
        if not id_factura: return

        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM factura WHERE id_factura = ?", (id_factura,))
            dF = cursor.fetchone()
            if not dF:
                messagebox.showerror("Error", "Factura no encontrada.")
                return

            idF, total, dn = dF
            cursor.execute("SELECT estado FROM pedido WHERE id_factura = ?", (id_factura,))
            estado = cursor.fetchone()
            estado = estado[0]
            if estado == 'Cancelado':
                messagebox.showerror("Error", "Esta factura ya ha sido cancelada.")
                return
            if estado != 'Vendido':
                messagebox.showerror("Error", "Solo se pueden cancelar compras que han sido vendidas previamente.")
                return

            info = f"ID de la factura: {idF}\nMonto total: {total}\nDNI: {dn}"
            vD = messagebox.askyesno("Confirmación", f"¿Son estos datos correctos?\n\n{info}")
            
            if vD:
                cursor.execute("UPDATE factura SET estado = 'Cancelado' WHERE id_factura = ?", (id_factura,))
                cursor.execute("UPDATE pedido SET estado = 'Cancelado' WHERE id_factura = ?", (id_factura,))


                cursor.execute("""
                    SELECT id_producto, cantidad FROM llevar
                    WHERE id_pedido IN(SELECT id_pedido FROM pedido WHERE id_factura = ?)
                """, (id_factura,))
                ic = cursor.fetchall()
                for idP, cant in ic:
                    cursor.execute("UPDATE stock SET total = total + ? WHERE id_producto = ?", (cant, idP))

                cursor.execute("""
                    SELECT id_kit, cantidad FROM pedido_kit
                    WHERE id_pedido IN(SELECT id_pedido FROM pedido WHERE id_factura = ?)
                """, (id_factura,))
                kic = cursor.fetchall()
                for idK, cant_kit in kic:
                    cursor.execute("SELECT id_producto FROM conjuntar WHERE LOWER(id_kit) = ?", (idK.lower(),))
                    productos_kit = cursor.fetchall()
                    for prod in productos_kit:
                        id_producto_en_kit = prod[0]
                        cursor.execute("""
                            SELECT COUNT(id_producto) FROM conjuntar
                            WHERE LOWER(id_kit) = ? AND id_producto = ?
                        """, (idK.lower(), id_producto_en_kit))
                        cantidad_en_kit = cursor.fetchone()[0]
                        cantidad_total_a_devolver = cant_kit * cantidad_en_kit
                        cursor.execute("UPDATE stock SET total = total + ? WHERE id_producto = ?", (cantidad_total_a_devolver, id_producto_en_kit))
                
                conn.commit()
                messagebox.showinfo("Éxito", "La compra se canceló correctamente y el stock fue actualizado.")
            else:
                messagebox.showinfo("Cancelado", "Cancelación anulada.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al cancelar la compra: {e}")
        finally:
            if conn:
                conn.close()

    def interfaz_filtro_productos(self):
        ventana_filtro = tk.Toplevel(self.raiz)
        ventana_filtro.title("Filtro de Productos y Stock")
        ventana_filtro.geometry("450x450")

        tk.Label(ventana_filtro, text="Filtros de Búsqueda", font=("Arial", 14)).pack(pady=10)

        tk.Label(ventana_filtro, text="Nombre del Producto:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_filtro, width=30)
        entrada_nombre.pack()
        
        tk.Label(ventana_filtro, text="Marca:").pack(pady=5)
        entrada_marca = tk.Entry(ventana_filtro, width=30)
        entrada_marca.pack()

        tk.Label(ventana_filtro, text="Categoría:").pack(pady=5)
        entrada_categoria = tk.Entry(ventana_filtro, width=30)
        entrada_categoria.pack()

        tk.Label(ventana_filtro, text="Estado de Stock:").pack(pady=5)
        estado_opciones = ["Cualquiera", "Óptimo", "Bajo", "Sin Stock"]
        estado_var = tk.StringVar(ventana_filtro)
        estado_var.set(estado_opciones[0])
        opcion_estado = tk.OptionMenu(ventana_filtro, estado_var, *estado_opciones)
        opcion_estado.pack()
        
        widget_texto = tk.Text(ventana_filtro, wrap="word", width=60, height=15)
        widget_texto.pack(pady=10, padx=10)
        
        def aplicar_filtro():
            nombre = entrada_nombre.get()
            marca = entrada_marca.get()
            categoria = entrada_categoria.get()
            estado = estado_var.get()
            self.mostrar_lista_productos_stock(widget_texto, nombre, marca, categoria, estado)

        boton_filtrar = tk.Button(ventana_filtro, text="Aplicar Filtros", command=aplicar_filtro)
        boton_filtrar.pack(pady=10)

        self.mostrar_lista_productos_stock(widget_texto)


    def mostrar_lista_productos_stock(self, widget_texto, nombre="", marca="", categoria="", estado="Cualquiera"):
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()
            
            sql_query = """
                SELECT p.nombre_producto, p.marca, p.categoria_producto, s.minimo, s.maximo, s.total
                FROM producto p JOIN stock s ON p.id_producto = s.id_producto
            """
            
            conditions = []
            params = []
            
            if nombre:
                conditions.append("LOWER(p.nombre_producto) LIKE ?")
                params.append(f"%{nombre.lower()}%")
            if marca:
                conditions.append("LOWER(p.marca) LIKE ?")
                params.append(f"%{marca.lower()}%")
            if categoria:
                conditions.append("LOWER(p.categoria_producto) LIKE ?")
                params.append(f"%{categoria.lower()}%")
                
            if conditions:
                sql_query += " WHERE " + " AND ".join(conditions)

            cursor.execute(sql_query, params)
            datos_filtrados = cursor.fetchall()
            
            widget_texto.config(state=tk.NORMAL)
            widget_texto.delete(1.0, tk.END)
            widget_texto.insert(tk.END, "--- Resultados de la Búsqueda ---\n\n")

            has_results = False
            for nombre_prod, marca_prod, cat_prod, minimo, maximo, total in datos_filtrados:
                
                umbral_30_porciento = maximo * 0.30 if maximo is not None else 0
                
                current_status = ""
                if total == 0:
                    current_status = "Sin Stock"
                elif total <= umbral_30_porciento:
                    current_status = "Bajo"
                else:
                    current_status = "Óptimo"

                if estado != "Cualquiera" and estado.replace(" ", "") != current_status.replace(" ", ""):
                    continue
                
                has_results = True
                linea = f"Nombre: {nombre_prod}\n"
                linea += f"Marca: {marca_prod}, Categoría: {cat_prod}\n"
                linea += f"Stock Mínimo: {minimo}, Stock Máximo: {maximo}, Stock Actual: {total}\n"
                if total <= umbral_30_porciento:
                    linea += f"Estado: ⚠️ Queda poco stock\n"
                else:
                    linea += f"Estado: ✅ El stock está óptimo\n"
                linea += "-" * 70 + "\n"
                widget_texto.insert(tk.END, linea)
            
            if not has_results:
                widget_texto.insert(tk.END, "No se encontraron productos que coincidan con los filtros. 😔\n")
            
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
                nombre = entrada_nombre.get().strip() 
                marca = entrada_marca.get().strip() 
                cat = entrada_categoria.get().strip() 
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
                nombre = entrada_nombre.get().strip() 
                marca = entrada_marca.get().strip()  
                nuevo_stock = int(entrada_nuevo_stock.get())

                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre.lower(), marca.lower()))
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
                nombre = entrada_nombre.get().strip() 
                marca = entrada_marca.get().strip() 
                
                conn = sqlite3.connect('blackiron.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = ? AND LOWER(marca) = ?", (nombre.lower(), marca.lower()))
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
                        WHERE LOWER(p.categoria_producto) = ?
                    """, (categoria.lower(),))
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



    def menu_kits_nuevo(self):
        top = tk.Toplevel(self.raiz)
        top.title("Gestión de Kits")
        top.geometry("360x260")
        tk.Label(top, text="Gestión de Kits", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(top, text="Ingresar Kit", width=28, command=lambda: [top.destroy(), self.ingresar_kit_gui()]).pack(pady=5)
        tk.Button(top, text="Modificar Kit", width=28, command=lambda: [top.destroy(), self.modificar_kit_gui()]).pack(pady=5)
        tk.Button(top, text="Borrar Kit", width=28, command=lambda: [top.destroy(), self.borrar_kit_gui()]).pack(pady=5)
        tk.Button(top, text="Cerrar", width=28, command=top.destroy).pack(pady=10)

    def kit_existe(self, nombre: str) -> bool:
        try:
            conn = sqlite3.connect('blackiron.db')
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM kits WHERE nombre = ?", (nombre,))
            return cur.fetchone() is not None
        finally:
            try:
                conn.close()
            except:
                pass

    def producto_buscar(self, nombre_prod: str, marca: str):
        try:
            conn = sqlite3.connect('blackiron.db')
            cur = conn.cursor()
            cur.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = LOWER(?) AND LOWER(marca) = LOWER(?)", (nombre_prod, marca))
            return cur.fetchall()
        finally:
            try:
                conn.close()
            except:
                pass

    def conjuntar_count(self, id_kit: str, id_producto: int) -> int:
        try:
            conn = sqlite3.connect('blackiron.db')
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM conjuntar WHERE id_kit = ? AND id_producto = ?", (id_kit, id_producto))
            return cur.fetchone()[0]
        finally:
            try:
                conn.close()
            except:
                pass

    def conjuntar_set_count(self, id_kit: str, id_producto: int, nuevo: int):
        actual = self.conjuntar_count(id_kit, id_producto)
        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        try:
            if nuevo == 0:
                cur.execute("DELETE FROM conjuntar WHERE id_kit = ? AND id_producto = ?", (id_kit, id_producto))
            elif nuevo < actual:
                quitar = actual - nuevo
                cur.execute("DELETE FROM conjuntar WHERE id IN(SELECT id FROM conjuntar WHERE id_kit = ? AND id_producto = ? LIMIT ?)", (id_kit, id_producto, quitar))
            elif nuevo > actual:
                agregar = nuevo - actual
                for _ in range(agregar):
                    cur.execute("INSERT INTO conjuntar(id_kit, id_producto) VALUES(?, ?)", (id_kit, id_producto))
            conn.commit()
        finally:
            conn.close()

    def ingresar_kit_gui(self):
        nombre = simpledialog.askstring("Ingresar Kit", "Nombre del kit:", parent=self.raiz)
        if not nombre:
            return
        if self.kit_existe(nombre):
            messagebox.showerror("Error", "El kit ingresado ya existe.")
            return

        while True:
            precio_str = simpledialog.askstring("Ingresar Kit", "Precio del kit:", parent=self.raiz)
            if precio_str is None:
                return
            try:
                precio = float(precio_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Ingrese un precio válido.")

        while True:
            total_str = simpledialog.askstring("Ingresar Kit", f"¿De cuántos productos estará compuesto {nombre}?", parent=self.raiz)
            if total_str is None:
                return
            try:
                total = int(total_str)
                if total < 0:
                    raise ValueError
                break
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número entero válido.")

        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO kits(nombre, precio) VALUES(?, ?)", (nombre, precio))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            messagebox.showerror("Error", "No se pudo crear el kit (nombre duplicado).")
            return
        conn.close()

        for i in range(total):
            producto = simpledialog.askstring("Ingresar Kit", f"Nombre del producto {i+1}:", parent=self.raiz)
            if producto is None:
                self._rollback_kit(nombre)
                return
            marca = simpledialog.askstring("Ingresar Kit", f"Marca de '{producto}':", parent=self.raiz)
            if marca is None:
                self._rollback_kit(nombre)
                return

            encontrados = self.producto_buscar(producto, marca)
            if not encontrados:
                messagebox.showerror("No encontrado", f"No se encontró el producto '{producto}' con marca '{marca}'. Se cancela el alta del kit.")
                self._rollback_kit(nombre)
                return

            while True:
                cant_str = simpledialog.askstring("Ingresar Kit", f"¿Cuántas unidades de '{producto}' (marca {marca})?", parent=self.raiz)
                if cant_str is None:
                    self._rollback_kit(nombre)
                    return
                try:
                    cant = int(cant_str)
                    if cant < 0:
                        raise ValueError
                    break
                except ValueError:
                    messagebox.showerror("Error", "Ingrese una cantidad entera válida.")

            conn = sqlite3.connect('blackiron.db')
            cur = conn.cursor()
            for row in encontrados:
                pr = row[0]
                for _ in range(cant):
                    cur.execute("INSERT INTO conjuntar(id_kit, id_producto) VALUES(?, ?)", (nombre, pr))
            conn.commit()
            conn.close()

        messagebox.showinfo("Éxito", "Kit ingresado con éxito.")

    def _rollback_kit(self, nombre):
        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM kits WHERE nombre = ?", (nombre,))
        cur.execute("DELETE FROM conjuntar WHERE id_kit = ?", (nombre,))
        conn.commit()
        conn.close()

    def borrar_kit_gui(self):
        nombre = simpledialog.askstring("Eliminar Kit", "Nombre del kit a eliminar:", parent=self.raiz)
        if not nombre:
            return
        if not self.kit_existe(nombre):
            messagebox.showerror("Error", "Ese kit no existe.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el kit '{nombre}'?"):
            return

        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM conjuntar WHERE id_kit = ?", (nombre,))
        cur.execute("DELETE FROM kits WHERE nombre = ?", (nombre,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Kit eliminado con éxito.")

    def _mostrar_productos_kit(self, nombre):
        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        cur.execute(
            "SELECT p.nombre_producto, p.marca, COUNT(c.id_producto) "
            "FROM conjuntar AS c JOIN producto AS p ON c.id_producto = p.id_producto "
            "WHERE c.id_kit = ? GROUP BY c.id_producto, p.nombre_producto, p.marca",
            (nombre,)
        )
        productos = cur.fetchall()
        conn.close()

        if not productos:
            messagebox.showinfo("Productos del kit", "No se encontraron productos para ese kit.")
            return []

        msg = ["--- Productos en el kit ---"]
        for nom, marca, cant in productos:
            msg.append(f"- {nom} ({marca}): {cant}")
        messagebox.showinfo("Productos del kit", "\n".join(msg))
        return productos

    def _modificar_productos_kit(self, nombre):
        productos = self._mostrar_productos_kit(nombre)
        if not productos:
            return

        while True:
            n_str = simpledialog.askstring("Modificar productos", f"Hay {len(productos)} productos distintos.\n¿Cuántos desea modificar?", parent=self.raiz)
            if n_str is None:
                return
            try:
                nuMo = int(n_str)
                if nuMo < 0 or nuMo > len(productos):
                    raise ValueError
                break
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido (entre 0 y la cantidad mostrada).")

        for i in range(nuMo):
            nombr = simpledialog.askstring("Modificar producto", f"Nombre del producto {i+1}:", parent=self.raiz)
            if nombr is None:
                return
            ma = simpledialog.askstring("Modificar producto", f"Marca de '{nombr}':", parent=self.raiz)
            if ma is None:
                return

            conn = sqlite3.connect('blackiron.db')
            cur = conn.cursor()
            cur.execute("SELECT id_producto FROM producto WHERE LOWER(nombre_producto) = LOWER(?) AND LOWER(marca) = LOWER(?)", (nombr, ma))
            row = cur.fetchone()
            conn.close()
            if not row:
                messagebox.showerror("Error", f"No existe el producto '{nombr}' ({ma}).")
                return
            idP = row[0]

            canP = self.conjuntar_count(nombre, idP)
            messagebox.showinfo("Cantidad actual", f"Cantidad actual de {nombr} ({ma}): {canP}", parent=self.raiz)

            while True:
                nuCant_str = simpledialog.askstring("Nueva cantidad", "Ingrese la nueva cantidad:", parent=self.raiz)
                if nuCant_str is None:
                    return
                try:
                    nuCant = int(nuCant_str)
                    if nuCant < 0:
                        raise ValueError
                    break
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un entero mayor o igual a 0.")

            self.conjuntar_set_count(nombre, idP, nuCant)

        messagebox.showinfo("Éxito", "Kit modificado con éxito.")

    def _modificar_datos_kit(self, nombre):
        conn = sqlite3.connect('blackiron.db')
        cur = conn.cursor()
        cur.execute("SELECT nombre, precio FROM kits WHERE nombre = ?", (nombre,))
        row = cur.fetchone()
        if not row:
            conn.close()
            messagebox.showerror("Error", "El kit no existe.")
            return
        nombre_actual, precio_actual = row

        nNuevo = simpledialog.askstring("Modificar datos", f"Nuevo nombre (Enter para mantener '{nombre_actual}'):", parent=self.raiz)
        if nNuevo in (None, ""):
            nNuevo = nombre_actual

        while True:
            pNuevo_str = simpledialog.askstring("Modificar datos", f"Nuevo precio (Enter para mantener {precio_actual}):", parent=self.raiz)
            if pNuevo_str is None or pNuevo_str == "":
                pNuevo = precio_actual
                break
            try:
                pNuevo = float(pNuevo_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Ingrese un precio válido.")

        try:
            cur.execute("UPDATE kits SET nombre = ?, precio = ? WHERE nombre = ?", (nNuevo, pNuevo, nombre_actual))
            if nNuevo != nombre_actual:
                cur.execute("UPDATE conjuntar SET id_kit = ? WHERE id_kit = ?", (nNuevo, nombre_actual))
            conn.commit()
            messagebox.showinfo("Éxito", "Datos del kit modificados con éxito.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un kit con ese nombre.")
        finally:
            conn.close()

    def _modificar_datos_y_productos(self, nombre):
        self._modificar_datos_kit(nombre)
        self._modificar_productos_kit(nombre)

    def modificar_kit_gui(self):
        nombre = simpledialog.askstring("Modificar Kit", "Nombre del kit a modificar:", parent=self.raiz)
        if not nombre:
            return
        if not self.kit_existe(nombre):
            messagebox.showerror("Error", "Ese kit no existe.")
            return

        top = tk.Toplevel(self.raiz)
        top.title(f"Modificar Kit: {nombre}")
        top.geometry("420x260")
        tk.Label(top, text=f"Modificar Kit: {nombre}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(top, text="1) Modificar productos del kit", command=lambda: [top.destroy(), self._modificar_productos_kit(nombre)]).pack(fill="x", padx=20, pady=6)
        tk.Button(top, text="2) Modificar nombre / precio", command=lambda: [top.destroy(), self._modificar_datos_kit(nombre)]).pack(fill="x", padx=20, pady=6)
        tk.Button(top, text="3) Modificar productos + nombre / precio", command=lambda: [top.destroy(), self._modificar_datos_y_productos(nombre)]).pack(fill="x", padx=20, pady=6)
        tk.Button(top, text="Cerrar", command=top.destroy).pack(pady=10)
if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionBlackIron(raiz)
    raiz.mainloop()


def ingresar_kit():
    try:
        app.ingresar_kit_gui()
    except NameError:
        messagebox.showerror("Error", "La aplicación no está inicializada.")

def borrar_kit():
    try:
        app.borrar_kit_gui()
    except NameError:
        messagebox.showerror("Error", "La aplicación no está inicializada.")

def modificar_kit():
    try:
        app.modificar_kit_gui()
    except NameError:
        messagebox.showerror("Error", "La aplicación no está inicializada.")
