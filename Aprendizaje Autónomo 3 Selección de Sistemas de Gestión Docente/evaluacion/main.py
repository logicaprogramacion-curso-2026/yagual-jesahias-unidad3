# main.py
from data.preguntas import obtener_preguntas
from logic.evaluador_ia import evaluar_respuesta
from cli.interfaz import mostrar_menu, mostrar_resultado

def ejecutar():
    preguntas = obtener_preguntas()
    
    while True:
        id_sel = mostrar_menu(preguntas)
        
        # Buscar la pregunta seleccionada
        pregunta_obj = next((p for p in preguntas if p['id'] == id_sel), None)
        
        if pregunta_obj:
            respuesta = input("\nEscriba la respuesta del estudiante:\n> ")
            print("\nProcesando evaluación con IA...")
            
            resultado = evaluar_respuesta(
                pregunta_obj['pregunta'], 
                respuesta, 
                pregunta_obj['criterios']
            )
            
            mostrar_resultado(resultado)
        else:
            print("Opción no válida.")

        continuar = input("¿Desea evaluar otra? (s/n): ")
        if continuar.lower() != 's':
            print("Cerrando sistema...")
            break

if __name__ == "__main__":
    ejecutar()