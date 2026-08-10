import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dao import PreguntaDAO

def test_conexion():
    dao = PreguntaDAO()
    try:
        conn = dao.conectar()
        print("Conexión a BD exitosa.")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_conexion()