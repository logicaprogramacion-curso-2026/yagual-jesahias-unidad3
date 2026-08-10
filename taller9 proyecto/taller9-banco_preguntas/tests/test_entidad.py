import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from entidad import Pregunta

def test_pregunta():
    p = Pregunta(1, "Test", "A", "B", "C", "D", "A", "Fácil", "Gral")
    assert p.id == 1
    assert p.respuesta_correcta == "A"
    print("Prueba de entidad exitosa.")

if __name__ == "__main__":
    test_pregunta()