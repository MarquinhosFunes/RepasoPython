productos = ["Manzana", "Banana", "Pera"]

def mostrar_menu():
    print("\nMenú:")
    print("1. Mostrar productos")
    print("2. Agregar producto")
    print("3. Salir")

def mostrar_productos():
    print("\nLista de productos:")
    if not productos:
        print("No hay productos en la lista.")
    else:
        for i, producto in enumerate(productos, 1):
            print(f"{i}. {producto}")

def agregar_producto():
    nuevo_producto = input("\nIngrese el nombre del nuevo producto: ")
    if nuevo_producto.strip():
        productos.append(nuevo_producto)
        print(f"Producto '{nuevo_producto}' agregado exitosamente.")
    else:
        print("Error: El nombre del producto no puede estar vacío.")

def main():
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("\nSelecciona una opción: "))
            
            if opcion == 1:
                mostrar_productos()
            elif opcion == 2:
                agregar_producto()
            elif opcion == 3:
                print("\n¡Gracias por usar el programa!")
                break
            else:
                print("\nOpción no válida. Por favor, seleccione 1, 2 o 3.")
        
        except ValueError:
            print("\nError: Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()