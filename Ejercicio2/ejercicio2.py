def validar_nota(nota_str):
    try:
        nota = float(nota_str)
        if 0 <= nota <= 10:
            return True, nota
        else:
            return False, None
    except ValueError:
        return False, None

def ingresar_notas():
    notas = []
    for i in range(5):
        while True:
            nota_str = input(f"Ingrese la nota {i+1} (0-10): ")
            valida, nota = validar_nota(nota_str)
            
            if valida:
                notas.append(nota)
                break
            else:
                print("Error: Por favor ingrese una nota válida entre 0 y 10")
    
    return notas

def calcular_promedio(notas):
    return sum(notas) / len(notas)

def mostrar_reporte(estudiante, notas, promedio):
    print("\nReporte de notas:")
    print("=" * 30)
    print(f"Estudiante: {estudiante}")
    print("-" * 30)
    for i, nota in enumerate(notas, 1):
        print(f"Nota {i}: {nota:.2f}")
    print("-" * 30)
    print(f"Promedio: {promedio:.2f}")
    
    if promedio >= 7:
        print("¡Excelente desempeño!")
    elif promedio >= 4:
        print("Aprobado")
    else:
        print("Necesita mejorar")
    print("=" * 30)

def main():
    estudiantes = {}
    
    while True:
        print("\nGestión de Notas de Estudiantes")
        print("1. Ingresar notas de estudiante")
        print("2. Ver estudiantes registrados")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            nombre = input("\nIngrese el nombre del estudiante: ").strip()
            
            if nombre:
                if nombre in estudiantes:
                    print(f"\nEl estudiante '{nombre}' ya existe.")
                    ver_notas = input("¿Desea ver sus notas? (s/n): ").lower()
                    if ver_notas == 's':
                        notas = estudiantes[nombre]
                        promedio = calcular_promedio(notas)
                        mostrar_reporte(nombre, notas, promedio)
                else:
                    print(f"\nIngrese las notas para {nombre}")
                    notas = ingresar_notas()
                    estudiantes[nombre] = notas
                    promedio = calcular_promedio(notas)
                    mostrar_reporte(nombre, notas, promedio)
            else:
                print("Error: El nombre no puede estar vacío")
                
        elif opcion == "2":
            if estudiantes:
                print("\nEstudiantes registrados:")
                print("-" * 30)
                for nombre, notas in estudiantes.items():
                    promedio = calcular_promedio(notas)
                    print(f"{nombre}: Promedio = {promedio:.2f}")
            else:
                print("\nNo hay estudiantes registrados")
                
        elif opcion == "3":
            print("\n¡Gracias por usar el programa!")
            break
            
        else:
            print("\nOpción no válida. Por favor, seleccione 1, 2 o 3.")

if __name__ == "__main__":
    main()