import sqlite3
from sqlite3 import Error
import os

def crear_conexion():
    try:
        conn = sqlite3.connect('escuela.db')
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tabla(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                promedio REAL NOT NULL,
                origen TEXT DEFAULT 'archivo'
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def validar_datos(linea):
    try:
        partes = linea.strip().split(',')
        if len(partes) != 2:
            return False, None, None
        
        nombre = partes[0].strip()
        promedio = float(partes[1].strip())
        
        if not nombre or not (0 <= promedio <= 10):
            return False, None, None
            
        return True, nombre, promedio
    except ValueError:
        return False, None, None

def leer_archivo(nombre_archivo):
    datos_validos = []
    lineas_invalidas = []
    
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                valido, nombre, promedio = validar_datos(linea)
                if valido:
                    datos_validos.append((nombre, promedio))
                else:
                    lineas_invalidas.append(numero_linea)
                    
        if lineas_invalidas:
            print("\nAdvertencia: Se encontraron líneas con formato inválido:")
            print(f"Líneas: {', '.join(map(str, lineas_invalidas))}")
            
        return datos_validos
                    
    except FileNotFoundError:
        print(f"\nError: El archivo {nombre_archivo} no existe.")
        return []
    except IOError as e:
        print(f"\nError al leer el archivo: {e}")
        return []

def insertar_estudiantes(conn, estudiantes):
    cursor = conn.cursor()
    insertados = []
    existentes = []
    errores = []
    
    for nombre, promedio in estudiantes:
        try:
            cursor.execute('''
                INSERT INTO estudiantes (nombre, promedio)
                VALUES (?, ?)
            ''', (nombre, promedio))
            insertados.append((nombre, promedio))
        except sqlite3.IntegrityError:
            existentes.append(nombre)
        except Error as e:
            errores.append((nombre, str(e)))
    
    conn.commit()
    return insertados, existentes, errores

def mostrar_estudiantes(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, promedio, origen FROM estudiantes ORDER BY nombre')
        estudiantes = cursor.fetchall()
        
        if estudiantes:
            print("\nEstudiantes en la base de datos:")
            print("=" * 60)
            print(f"{'ID':<5} {'Nombre':<30} {'Promedio':<10} {'Origen':<15}")
            print("-" * 60)
            
            for estudiante in estudiantes:
                print(f"{estudiante[0]:<5} {estudiante[1]:<30} {estudiante[2]:<10.2f} {estudiante[3]:<15}")
            
            print("=" * 60)
        else:
            print("\nNo hay estudiantes registrados en la base de datos.")
            
    except Error as e:
        print(f"Error al mostrar estudiantes: {e}")

def crear_archivo_ejemplo():
    nombre_archivo = 'datos_estudiantes.txt'
    if not os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("Juan Pérez,8.5\n")
                archivo.write("María García,9.2\n")
                archivo.write("Carlos López,7.8\n")
            print(f"\nArchivo {nombre_archivo} creado con datos de ejemplo.")
        except IOError as e:
            print(f"Error al crear el archivo de ejemplo: {e}")

def main():
    crear_archivo_ejemplo()
    
    conn = crear_conexion()
    if conn is None:
        return
    
    crear_tabla(conn)
    
    while True:
        print("\nSistema Integrado de Gestión de Estudiantes")
        print("1. Cargar datos desde archivo")
        print("2. Ver todos los estudiantes")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            nombre_archivo = input("\nIngrese el nombre del archivo (default: datos_estudiantes.txt): ").strip()
            if not nombre_archivo:
                nombre_archivo = 'datos_estudiantes.txt'
                
            datos = leer_archivo(nombre_archivo)
            
            if datos:
                insertados, existentes, errores = insertar_estudiantes(conn, datos)
                
                if insertados:
                    print("\nEstudiantes insertados exitosamente:")
                    for nombre, promedio in insertados:
                        print(f"- {nombre}: {promedio}")
                        
                if existentes:
                    print("\nEstudiantes que ya existían en la base de datos:")
                    for nombre in existentes:
                        print(f"- {nombre}")
                        
                if errores:
                    print("\nErrores al insertar estudiantes:")
                    for nombre, error in errores:
                        print(f"- {nombre}: {error}")
                        
        elif opcion == "2":
            mostrar_estudiantes(conn)
            
        elif opcion == "3":
            print("\n¡Gracias por usar el programa!")
            break
            
        else:
            print("\nOpción no válida. Por favor, seleccione 1, 2 o 3.")
    
    conn.close()

if __name__ == "__main__":
    main()