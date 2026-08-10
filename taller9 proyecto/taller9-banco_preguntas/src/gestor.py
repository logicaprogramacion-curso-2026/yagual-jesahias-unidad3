import json
import csv
from entidad import Pregunta

class GestorPreguntas:
    @staticmethod
    def cargar_desde_json(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return [Pregunta(**d) for d in json.load(f)]

    @staticmethod
    def cargar_desde_csv(ruta):
        preguntas = []
        with open(ruta, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for r in lector:
                r['id'] = int(r['id'])
                preguntas.append(Pregunta(**r))
        return preguntas

    @staticmethod
    def cargar_desde_txt(ruta):
        preguntas = []
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                d = linea.strip().split('|')
                if len(d) == 9:
                    preguntas.append(Pregunta(int(d[0]), d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8]))
        return preguntas