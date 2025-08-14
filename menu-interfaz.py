import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import time


intentos_fallidos = 0
tiempo_de_bloqueo = 0
MAX_INTENTOS = 3
TIEMPO_DE_ESPERA = 30  




def setup_database():
    """
    Conecta a la base de datos y crea las tablas si no existen.
    Luego, puebla las tablas con datos de ejemplo si están vacías.
    """
    try:
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()

    
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id_producto INTEGER PRIMARY KEY,
            precio REAL,
            nombre_producto TEXT,
            marca TEXT,
            categoria_producto TEXT
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            minimo REAL,
            maximo REAL,
            real REAL,
            id_producto INTEGER,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            DNI INTEGER PRIMARY KEY,
            gmail TEXT,
            direccion TEXT,
            apellido TEXT,
            nombre TEXT
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS factura (
            id_factura INTEGER PRIMARY KEY,
            total REAL,
            nombre_producto TEXT,
            DNI INTEGER,
            FOREIGN KEY (DNI) REFERENCES cliente(DNI)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturar (
            id_facturar INTEGER PRIMARY KEY,
            DNI INTEGER,
            id_factura INTEGER,
            FOREIGN KEY (DNI) REFERENCES cliente(DNI),
            FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido INTEGER PRIMARY KEY,
            estado TEXT,
            cantidad INTEGER,
            id_producto INTEGER,
            id_factura INTEGER,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
            FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            contrasenia TEXT
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS kits (
            id_kits INTEGER PRIMARY KEY,
            id_producto INTEGER,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        );''')

        conn.commit()

 
        poblar_datos_ejemplo(conn, cursor)

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al configurar la base de datos: {e}")
    finally:
        if conn:
            conn.close()


def poblar_datos_ejemplo(conn, cursor):
    """Inserta datos de ejemplo en las tablas si estas están vacías."""
    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO empleados (nombre, apellido, contrasenia) VALUES ('admin', 'Gomez', '12345')")
        cursor.execute("INSERT INTO empleados (nombre, apellido, contrasenia) VALUES ('juan', 'Perez', 'abcde')")

    cursor.execute("SELECT COUNT(*) FROM producto")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (150.50, 'Proteina en Polvo', 'WheyPro', 'Suplementos')")
        cursor.execute(
            "INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (25.00, 'Guantes de Gimnasio', 'FitGear', 'Accesorios')")
        cursor.execute(
            "INSERT INTO producto (precio, nombre_producto, marca, categoria_producto) VALUES (300.00, 'Mancuerna de 10kg', 'IronGym', 'Equipo')")

    cursor.execute("SELECT COUNT(*) FROM stock")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO stock (minimo, maximo, real, id_producto) VALUES (10, 50, 25, 1)")
        cursor.execute("INSERT INTO stock (minimo, maximo, real, id_producto) VALUES (5, 20, 12, 2)")
        cursor.execute("INSERT INTO stock (minimo, maximo, real, id_producto) VALUES (2, 10, 5, 3)")

    cursor.execute("SELECT COUNT(*) FROM cliente")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO cliente (DNI, gmail, direccion, apellido, nombre) VALUES (12345678, 'cliente1@mail.com', 'Calle Falsa 123', 'Diaz', 'Carlos')")

    cursor.execute("SELECT COUNT(*) FROM factura")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO factura (total, nombre_producto, DNI) VALUES (150.50, 'Proteina en Polvo', 12345678)")

    cursor.execute("SELECT COUNT(*) FROM pedido")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pedido (estado, cantidad, id_producto, id_factura) VALUES ('entregado', 1, 1, 1)")

    cursor.execute("SELECT COUNT(*) FROM kits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO kits (id_producto) VALUES (1)")
        cursor.execute("INSERT INTO kits (id_producto) VALUES (2)")

    conn.commit()




def mostrar_stock():
    """Muestra los datos de la tabla 'stock' en una nueva ventana."""
    try:
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT s.id, s.minimo, s.maximo, s.real, p.nombre_producto FROM stock s INNER JOIN producto p ON s.id_producto = p.id_producto")
        stock_data = cursor.fetchall()

        stock_window = tk.Toplevel()
        stock_window.title("Visualizar Stock")

        text_widget = tk.Text(stock_window, wrap="word", width=60, height=15)
        text_widget.pack(pady=10, padx=10)


        text_widget.insert(tk.END, "ID | Mínimo | Máximo | Real | Nombre del Producto\n")
        text_widget.insert(tk.END, "--------------------------------------------------------\n")

        for row in stock_data:
            text_widget.insert(tk.END, f"{row[0]:<3} | {row[1]:<6} | {row[2]:<6} | {row[3]:<4} | {row[4]}\n")

        text_widget.config(state=tk.DISABLED)  
    except sqlite3.Error as e:
        messagebox.showerror("Error de BD", f"Error al obtener stock: {e}")
    finally:
        if conn:
            conn.close()


def mostrar_pedidos():
    """Muestra los datos de la tabla 'pedido' en una nueva ventana."""
    try:
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.id_pedido, p.estado, p.cantidad, pr.nombre_producto, f.id_factura FROM pedido p INNER JOIN producto pr ON p.id_producto = pr.id_producto INNER JOIN factura f ON p.id_factura = f.id_factura")
        pedidos_data = cursor.fetchall()

        pedidos_window = tk.Toplevel()
        pedidos_window.title("Visualizar Pedidos")

        text_widget = tk.Text(pedidos_window, wrap="word", width=60, height=15)
        text_widget.pack(pady=10, padx=10)

        text_widget.insert(tk.END, "ID Pedido | Estado | Cantidad | Producto | ID Factura\n")
        text_widget.insert(tk.END, "-----------------------------------------------------\n")

        for row in pedidos_data:
            text_widget.insert(tk.END, f"{row[0]:<10} | {row[1]:<7} | {row[2]:<8} | {row[3]:<10} | {row[4]}\n")

        text_widget.config(state=tk.DISABLED)
    except sqlite3.Error as e:
        messagebox.showerror("Error de BD", f"Error al obtener pedidos: {e}")
    finally:
        if conn:
            conn.close()


def mostrar_kits():
    """Muestra los datos de la tabla 'kits' en una nueva ventana."""
    try:
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT k.id_kits, p.nombre_producto FROM kits k INNER JOIN producto p ON k.id_producto = p.id_producto")
        kits_data = cursor.fetchall()

        kits_window = tk.Toplevel()
        kits_window.title("Ver Kits")

        text_widget = tk.Text(kits_window, wrap="word", width=40, height=10)
        text_widget.pack(pady=10, padx=10)

        text_widget.insert(tk.END, "ID Kit | Producto\n")
        text_widget.insert(tk.END, "------------------------\n")

        for row in kits_data:
            text_widget.insert(tk.END, f"{row[0]:<7} | {row[1]}\n")

        text_widget.config(state=tk.DISABLED)
    except sqlite3.Error as e:
        messagebox.showerror("Error de BD", f"Error al obtener kits: {e}")
    finally:
        if conn:
            conn.close()


def tomar_pedido():
    """Crea una ventana para registrar un nuevo pedido y factura."""
    pedido_ventana = tk.Toplevel()
    pedido_ventana.title("Tomar Pedido")
    pedido_ventana.geometry("300x250")

    def guardar_pedido():
        """Función interna para guardar el pedido en la base de datos."""
        try:
            conn = sqlite3.connect('blackiron.db')
            cursor = conn.cursor()

            dni = entry_dni.get()
            nombre_producto = entry_producto.get()
            cantidad = entry_cantidad.get()

            if not dni or not nombre_producto or not cantidad:
                messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
                return

            cantidad = int(cantidad)

            cursor.execute("SELECT id_producto, precio FROM producto WHERE nombre_producto = ?", (nombre_producto,))
            producto_info = cursor.fetchone()

            if not producto_info:
                messagebox.showerror("Producto Inexistente", "El producto no se encuentra en la base de datos.")
                return

            id_producto, precio = producto_info
            total_factura = precio * cantidad

            cursor.execute("INSERT INTO factura (total, nombre_producto, DNI) VALUES (?, ?, ?)",
                           (total_factura, nombre_producto, dni))
            id_factura = cursor.lastrowid

            cursor.execute(
                "INSERT INTO pedido (estado, cantidad, id_producto, id_factura) VALUES ('pendiente', ?, ?, ?)",
                (cantidad, id_producto, id_factura))

            cursor.execute("INSERT INTO facturar (DNI, id_factura) VALUES (?, ?)", (dni, id_factura))

            conn.commit()
            messagebox.showinfo("Pedido Guardado",
                                f"El pedido para '{nombre_producto}' ha sido registrado con éxito. Total: ${total_factura}")
            pedido_ventana.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error de BD", f"Error al guardar el pedido: {e}")
        except ValueError:
            messagebox.showerror("Error de entrada", "La cantidad debe ser un número.")
        finally:
            if conn:
                conn.close()

    tk.Label(pedido_ventana, text="DNI del Cliente:").pack(pady=5)
    entry_dni = tk.Entry(pedido_ventana)
    entry_dni.pack()

    tk.Label(pedido_ventana, text="Nombre del Producto:").pack(pady=5)
    entry_producto = tk.Entry(pedido_ventana)
    entry_producto.pack()

    tk.Label(pedido_ventana, text="Cantidad:").pack(pady=5)
    entry_cantidad = tk.Entry(pedido_ventana)
    entry_cantidad.pack()

    btn_guardar = tk.Button(pedido_ventana, text="Guardar Pedido", command=guardar_pedido)
    btn_guardar.pack(pady=10)


def mostrar_menu_empleado():
    """Crea y muestra la ventana con el menú de opciones del empleado."""
    menu_ventana = tk.Toplevel()
    menu_ventana.title("Menú de Empleado")
    menu_ventana.geometry("350x350")

    label_bienvenida = tk.Label(menu_ventana, text="Bienvenido al sistema.", font=("Arial", 14))
    label_bienvenida.pack(pady=10)

    btn_stock = tk.Button(menu_ventana, text="Visualizar Stock", width=25, command=mostrar_stock)
    btn_stock.pack(pady=5)

    btn_pedidos = tk.Button(menu_ventana, text="Visualizar Pedidos", width=25, command=mostrar_pedidos)
    btn_pedidos.pack(pady=5)

    btn_kits = tk.Button(menu_ventana, text="Ver Kits", width=25, command=mostrar_kits)
    btn_kits.pack(pady=5)

    btn_tomar_pedido = tk.Button(menu_ventana, text="Tomar Pedido (Ventas)", width=25, command=tomar_pedido)
    btn_tomar_pedido.pack(pady=5)

    separador = tk.Frame(menu_ventana, height=2, bd=1, relief=tk.SUNKEN)
    separador.pack(fill=tk.X, padx=20, pady=10)

    btn_cerrar = tk.Button(menu_ventana, text="Cerrar Sesión", width=25, command=menu_ventana.destroy)
    btn_cerrar.pack(pady=10)



def verificar_login(ventana_login):
    """Verifica las credenciales en la base de datos y maneja el acceso, con bloqueo por intentos fallidos."""
    global intentos_fallidos, tiempo_de_bloqueo

    if tiempo_de_bloqueo > time.time():
        tiempo_restante = int(tiempo_de_bloqueo - time.time())
        messagebox.showwarning("Cuenta Bloqueada",
                               f"Demasiados intentos fallidos. Inténtalo de nuevo en {tiempo_restante} segundos.")
        return

    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    try:
        conn = sqlite3.connect('blackiron.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleados WHERE nombre = ? AND contrasenia = ?", (usuario, contrasena))
        empleado = cursor.fetchone()

        if empleado:
            intentos_fallidos = 0
            messagebox.showinfo("Acceso Correcto", f"¡Inicio de sesión exitoso! Bienvenido, {empleado[1]}.")
            ventana_login.destroy()
            mostrar_menu_empleado()
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


ventana = tk.Tk()
ventana.title("Iniciar Sesión")
ventana.geometry("300x200")

label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

label_contrasena = tk.Label(ventana, text="Contraseña:")
label_contrasena.pack(pady=5)
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.pack(pady=5)

btn_login = tk.Button(ventana, text="Iniciar Sesión", command=lambda: verificar_login(ventana))
btn_login.pack(pady=10)

setup_database()
ventana.mainloop()