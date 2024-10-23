def crear_archivo_si_no_existe():
    try:
        with open('notas.txt', 'a') as archivo:
            pass
    except IOError as e:
        print(f"Error al crear el archivo: {e}")
        return False
    return True

def validar_promedio(promedio_str):
    try:
        promedio = float(promedio_str)
        if 0 <= promedio <= 10:
            return True, promedio
        else:
            return False, None
    except ValueError:
        return False, None

def leer_archivo():
    try:
        with open('notas.txt', 'r') as archivo:
            contenido = archivo.read().strip()
            
            if contenido:
                print("\nContenido del archivo notas.txt:")
                print("=" * 40)
                print("Nombre\t\tPromedio")
                print("-" * 40)
                for linea in contenido.split('\n'):
                    if ',' in linea:
                        nombre, promedio = linea.split(',')
                        print(f"{nombre:<15}\t{promedio}")
                print("=" * 40)
            else:
                print("\nEl archivo está vacío.")
                
    except FileNotFoundError:
        print("\nEl archivo notas.txt aún no existe.")
    except IOError as e:
        print(f"\nError al leer el archivo: {e}")

def agregar_estudiante():
    nombre = input("\nIngrese el nombre del estudiante: ").strip()
    
    if not nombre:
        print("Error: El nombre no puede estar vacío")
        return False
        
    while True:
        promedio_str = input(f"Ingrese el promedio de {nombre} (0-10): ")
        valido, promedio = validar_promedio(promedio_str)
        
        if valido:
            try:
                with open('notas.txt', 'a') as archivo:
                    archivo.write(f"{nombre},{promedio:.2f}\n")
                print(f"\nEstudiante {nombre} agregado exitosamente.")
                return True
            except IOError as e:
                print(f"Error al escribir en el archivo: {e}")
                return False
        else:
            print("Error: Por favor ingrese un promedio válido entre 0 y 10")

def buscar_estudiante():
    nombre_buscar = input("\nIngrese el nombre del estudiante a buscar: ").strip().lower()
    
    try:
        with open('notas.txt', 'r') as archivo:
            encontrados = False
            print("\nResultados de la búsqueda:")
            print("-" * 40)
            
            for linea in archivo:
                if ',' in linea:
                    nombre, promedio = linea.strip().split(',')
                    if nombre_buscar in nombre.lower():
                        print(f"Nombre: {nombre}")
                        print(f"Promedio: {promedio}")
                        print("-" * 40)
                        encontrados = True
            
            if not encontrados:
                print(f"No se encontró ningún estudiante con el nombre '{nombre_buscar}'")
                
    except FileNotFoundError:
        print("\nEl archivo notas.txt aún no existe.")
    except IOError as e:
        print(f"\nError al leer el archivo: {e}")

def main():
    if not crear_archivo_si_no_existe():
        return
    
    while True:
        print("\nGestión de Notas - Archivo de Texto")
        print("1. Ver todos los estudiantes")
        print("2. Agregar nuevo estudiante")
        print("3. Buscar estudiante")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            leer_archivo()
        elif opcion == "2":
            agregar_estudiante()
        elif opcion == "3":
            buscar_estudiante()
        elif opcion == "4":
            print("\n¡Gracias por usar el programa!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()