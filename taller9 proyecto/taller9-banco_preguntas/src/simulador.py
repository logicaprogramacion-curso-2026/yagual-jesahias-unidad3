import random
import json
import csv
import os
from datetime import datetime

class Simulador:
    def __init__(self, preguntas):
        self.preguntas = preguntas
        self.respuestas_usuario = []
        self.puntaje = 0

    def iniciar(self, cantidad=5):
        seleccionadas = random.sample(self.preguntas, min(len(self.preguntas), cantidad))
        print("\n--- INICIO DE EVALUACIÓN ---")
        
        for i, p in enumerate(seleccionadas, 1):
            print(f"\n{i}. {p.pregunta}")
            print(f"A) {p.opcion_a}\nB) {p.opcion_b}\nC) {p.opcion_c}\nD) {p.opcion_d}")
            res = input("Tu respuesta: ").upper()
            
            es_correcta = (res == p.respuesta_correcta)
            if es_correcta: self.puntaje += 1
            
            self.respuestas_usuario.append({
                "pregunta": p.pregunta,
                "tu_respuesta": res,
                "correcta": p.respuesta_correcta,
                "resultado": "Correcto" if es_correcta else "Incorrecto"
            })
        
        self.guardar_resultados()

    def guardar_resultados(self):
        # Guardar en resultados/reporte.json
        ruta_json = os.path.join('resultados', 'reporte.json')
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(self.respuestas_usuario, f, indent=4)
            
        print(f"\nEvaluación finalizada. Puntaje: {self.puntaje}")
        print("Resultados guardados en la carpeta 'resultados/'")