import os
from dao import PreguntaDAO
from gestor import GestorPreguntas
from simulador import Simulador

def menu():
    # Obtener la ruta absoluta de la carpeta donde está este proyecto
    # Esto evita el error de "FileNotFoundError"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    dao = PreguntaDAO()
    gestor = GestorPreguntas()
    
    while True:
        print("\n=== SISTEMA DE BANCO DE PREGUNTAS ===")
        print("1. Cargar preguntas desde JSON")
        print("2. Cargar preguntas desde CSV")
        print("3. Cargar preguntas desde TXT")
        print("4. Ver todas las preguntas (BD)")
        print("5. Iniciar Simulacro de Examen")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ruta = os.path.join(BASE_DIR, "preguntas.json")
            if os.path.exists(ruta):
                preguntas = gestor.cargar_desde_json(ruta)
                dao.insertar_muchas(preguntas)
                print(f"Cargadas {len(preguntas)} preguntas desde JSON.")
            else:
                print(f"Error: No se encuentra el archivo en {ruta}")

        elif opcion == "2":
            ruta = os.path.join(BASE_DIR, "preguntas.csv")
            if os.path.exists(ruta):
                preguntas = gestor.cargar_desde_csv(ruta)
                dao.insertar_muchas(preguntas)
                print(f"Cargadas {len(preguntas)} preguntas desde CSV.")
            else:
                print(f"Error: No se encuentra el archivo en {ruta}")

        elif opcion == "3":
            ruta = os.path.join(BASE_DIR, "preguntas.txt")
            if os.path.exists(ruta):
                preguntas = gestor.cargar_desde_txt(ruta)
                dao.insertar_muchas(preguntas)
                print(f"Cargadas {len(preguntas)} preguntas desde TXT.")
            else:
                print(f"Error: No se encuentra el archivo en {ruta}")

        elif opcion == "4":
            preguntas_db = dao.obtener_todas()
            if preguntas_db:
                for p in preguntas_db: 
                    print(p)
            else:
                print("La base de datos está vacía.")

        elif opcion == "5":
            todas = dao.obtener_todas()
            if todas:
                sim = Simulador(todas)
                sim.iniciar()
            else:
                print("No hay preguntas en la base de datos. Cargue un archivo primero.")

        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
