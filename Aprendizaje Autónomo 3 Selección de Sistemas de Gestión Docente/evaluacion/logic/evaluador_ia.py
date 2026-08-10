# logic/evaluador_ia.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def evaluar_respuesta(pregunta, respuesta_estudiante, criterios):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Actúa como un evaluador académico.
    Pregunta: {pregunta}
    Criterios de evaluación: {criterios}
    Respuesta del alumno: {respuesta_estudiante}

    Entrega tu evaluación estrictamente en formato JSON con estas llaves:
    "puntuacion" (0-10), "retroalimentacion" (breve), "sugerencias" (para mejorar).
    """

    try:
        response = model.generate_content(prompt)
        # Limpiar posibles caracteres extra del LLM
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": f"Error en la IA: {str(e)}"}