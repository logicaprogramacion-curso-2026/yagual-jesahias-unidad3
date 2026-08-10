# cli/interfaz.py

def mostrar_menu(preguntas):
    print("\n" + "="*40)
    print("  SISTEMA DE EVALUACIÓN AUTOMÁTICA")
    print("="*40)
    for p in preguntas:
        print(f"[{p['id']}] {p['pregunta']}")
    
    try:
        seleccion = int(input("\nSeleccione el ID de la pregunta: "))
        return seleccion
    except ValueError:
        return None

def mostrar_resultado(res):
    print("\n--- RESULTADO DE LA EVALUACIÓN ---")
    if "error" in res:
        print(f"ERROR: {res['error']}")
    else:
        print(f"NOTA: {res['puntuacion']}/10")
        print(f"RETROALIMENTACIÓN: {res['retroalimentacion']}")
        print(f"MEJORAS: {res['sugerencias']}")
    print("-" * 34)