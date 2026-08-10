import sqlite3
import os
from entidad import Pregunta

class PreguntaDAO:
    def __init__(self):
        # Asegurar que la ruta a la DB sea correcta desde la raíz
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'preguntas.db')
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def crear_tabla(self):
        with self.conectar() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS preguntas (
                            id INTEGER PRIMARY KEY,
                            pregunta TEXT NOT NULL,
                            opcion_a TEXT, opcion_b TEXT, opcion_c TEXT, opcion_d TEXT,
                            respuesta_correcta TEXT, dificultad TEXT, tema TEXT)''')

    def insertar_muchas(self, preguntas):
        with self.conectar() as conn:
            cursor = conn.cursor()
            datos = [(p.id, p.pregunta, p.opcion_a, p.opcion_b, p.opcion_c, p.opcion_d, 
                      p.respuesta_correcta, p.dificultad, p.tema) for p in preguntas]
            cursor.executemany("INSERT OR REPLACE INTO preguntas VALUES (?,?,?,?,?,?,?,?,?)", datos)

    def obtener_todas(self):
        with self.conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM preguntas")
            return [Pregunta(**dict(row)) for row in cursor.fetchall()]

    def obtener_estadisticas(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tema, COUNT(*) FROM preguntas GROUP BY tema")
            return cursor.fetchall()