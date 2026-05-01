import requests

URL_BASE = "http://127.0.0.1:5000"

def menu():
    print("\n--- SISTEMA DE GESTIÓN DE TAREAS ---")
    print("1. Registrarse")
    print("2. Iniciar Sesión")
    print("3. Salir")
    return input("Seleccione una opción: ")

def registrar_usuario():
    usuario = input("Nombre de usuario: ")
    clave = input("Contraseña: ")
    respuesta = requests.post(f"{URL_BASE}/registro", json={"usuario": usuario, "contrasena": clave})
    print(respuesta.json().get("mensaje") or respuesta.json().get("error"))

# Función para mostrar las tareas de cada usuario.
def mostrar_tareas(user_id):
    # El cliente solicita sus recursos específicos al servidor
    respuesta = requests.get(f"{URL_BASE}/mis_tareas/{user_id}")
    
    if respuesta.status_code == 200:
        tareas = respuesta.json()
        print(f"\n--- LISTA DE TAREAS (ID Usuario: {user_id}) ---")
        if not tareas:
            print("No hay tareas registradas para este usuario.")
        else:
            for t in tareas:
                # Mostramos el estado según el valor booleano de la DB ( si la tarea esta hecha o no)
                estado = "[X]" if t['completada'] else "[ ]"
                print(f"ID: {t['id']} | {estado} {t['titulo']}")
    else:
        print("Error al obtener las tareas del servidor.")

def iniciar_sesion():
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")
    respuesta = requests.post(f"{URL_BASE}/login", json={"usuario": usuario, "contrasena": clave})
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        user_id = datos.get("user_id")
        print(f"\n¡Login exitoso! Bienvenido, {usuario}.")
        
        mostrar_tareas(user_id) 
        
        input("\nPresione Enter para volver al menú...")
    else:
        try:
            print("Error:", respuesta.json().get("error"))
        except:
            print("Error: Credenciales inválidas o fallo en el servidor.")

# Bucle del menú principal
while True:
    opcion = menu()
    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        print("Cerrando cliente...")
        break
    else:
        print("Opción no válida.")