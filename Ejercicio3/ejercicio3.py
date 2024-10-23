import sqlite3
from sqlite3 import Error

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
                nombre TEXT NOT NULL,
                promedio REAL NOT NULL
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_datos_iniciales(conn):
    estudiantes = [
        ('Rodrigo Gomez', 7.5),
        ('Juan Lopez', 9.8),
        ('Carlos Garcia', 8.3)
    ]
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.executemany('''
                INSERT INTO estudiantes (nombre, promedio)
                VALUES (?, ?)
            ''', estudiantes)
            conn.commit()
            print("Datos iniciales insertados correctamente.")
        else:
            print("La tabla ya contiene datos.")
    except Error as e:
        print(f"Error al insertar datos: {e}")

def buscar_estudiante(conn, nombre):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nombre, promedio 
            FROM estudiantes 
            WHERE LOWER(nombre) LIKE LOWER(?)
        ''', (f'%{nombre}%',))
        
        resultados = cursor.fetchall()
        
        if resultados:
            print("\nEstudiantes encontrados:")
            for estudiante in resultados:
                print(f"Nombre: {estudiante[0]}")
                print(f"Promedio: {estudiante[1]:.2f}")
        else:
            print(f"\nNo se encontró ningún estudiante con el nombre '{nombre}'")
            
    except Error as e:
        print(f"Error al buscar estudiante: {e}")

def mostrar_todos_estudiantes(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estudiantes')
        estudiantes = cursor.fetchall()
        
        if estudiantes:
            print("\nLista de todos los estudiantes:")
            for estudiante in estudiantes:
                print(f"ID: {estudiante[0]}, Nombre: {estudiante[1]}, Promedio: {estudiante[2]:.2f}")
        else:
            print("\nNo hay estudiantes registrados en la base de datos.")
            
    except Error as e:
        print(f"Error al mostrar estudiantes: {e}")

def main():
    conn = crear_conexion()
    if conn is None:
        return
    
    crear_tabla(conn)
    insertar_datos_iniciales(conn)
    
    while True:
        print("\nMenú:")
        print("1. Buscar estudiante")
        print("2. Mostrar todos los estudiantes")
        print("3. Salir")
        
        try:
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                nombre = input("Ingrese el nombre del estudiante a buscar: ")
                buscar_estudiante(conn, nombre)
            elif opcion == "2":
                mostrar_todos_estudiantes(conn)
            elif opcion == "3":
                print("¡Gracias por usar el programa!")
                break
            else:
                print("Opción no válida. Por favor, seleccione 1, 2 o 3.")
                
        except Exception as e:
            print(f"Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    main()