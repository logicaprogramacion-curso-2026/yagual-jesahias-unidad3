
"""
Evaluación Formativa de Competencias Docentes
Autoevaluación con formulario Bootstrap + panel de resultados con gráficos.
Los datos se manejan en memoria/sesión (sin base de datos, sin login).
"""

from flask import Flask, render_template, request, session, redirect, url_for
import statistics

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"


# Definición del marco de competencias docentes
COMPETENCIAS = [
    {
        "id": "planificacion",
        "nombre": "Planificación curricular y didáctica",
        "icono": "bi-clipboard-check",
        "indicadores": [
            "Diseño planificaciones alineadas a los objetivos y estándares curriculares.",
            "Defino con claridad los aprendizajes esperados de cada clase.",
            "Selecciono actividades coherentes con los objetivos planteados.",
            "Ajusto mi planificación según los resultados obtenidos previamente.",
        ],
    },
    {
        "id": "dominio_disciplinar",
        "nombre": "Dominio disciplinar y actualización profesional",
        "icono": "bi-mortarboard",
        "indicadores": [
            "Domino los contenidos de mi área o asignatura.",
            "Actualizo mis conocimientos de forma continua.",
            "Relaciono los contenidos con situaciones de la vida real.",
            "Resuelvo con seguridad las dudas conceptuales de mis estudiantes.",
        ],
    },
    {
        "id": "metodologia",
        "nombre": "Estrategias metodológicas y didácticas",
        "icono": "bi-lightbulb",
        "indicadores": [
            "Utilizo variedad de estrategias de enseñanza según el tema y el grupo.",
            "Promuevo el pensamiento crítico y la resolución de problemas.",
            "Adapto mi metodología a los diferentes ritmos de aprendizaje.",
            "Genero espacios de participación activa del estudiantado.",
        ],
    },
    {
        "id": "evaluacion_aprendizajes",
        "nombre": "Evaluación de los aprendizajes",
        "icono": "bi-check2-square",
        "indicadores": [
            "Utilizo diversos instrumentos para evaluar el aprendizaje.",
            "Brindo retroalimentación oportuna y constructiva.",
            "Uso los resultados de la evaluación para mejorar mi práctica.",
            "Comunico con claridad los criterios de evaluación.",
        ],
    },
    {
        "id": "clima_aula",
        "nombre": "Gestión del clima de aula y convivencia",
        "icono": "bi-people",
        "indicadores": [
            "Promuevo un ambiente de respeto y confianza en el aula.",
            "Manejo de forma efectiva los conflictos que surgen en clase.",
            "Establezco normas claras de convivencia con mis estudiantes.",
            "Fomento la inclusión y el respeto a la diversidad.",
        ],
    },
    {
        "id": "tic",
        "nombre": "Uso de TIC y recursos educativos",
        "icono": "bi-laptop",
        "indicadores": [
            "Integro herramientas digitales para enriquecer mis clases.",
            "Selecciono recursos educativos pertinentes y de calidad.",
            "Oriento a mis estudiantes en el uso responsable de la tecnología.",
            "Exploro nuevas herramientas para innovar mi práctica docente.",
        ],
    },
]

NIVELES = [
    (90, "Destacado", "success"),
    (75, "Satisfactorio", "primary"),
    (60, "En desarrollo", "warning"),
    (0, "Inicial", "danger"),
]


def clasificar(porcentaje):
    for umbral, etiqueta, color in NIVELES:
        if porcentaje >= umbral:
            return etiqueta, color
    return "Inicial", "danger"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", competencias=COMPETENCIAS)


@app.route("/evaluar", methods=["POST"])
def evaluar():
    resultados_competencia = []
    todos_los_puntajes = []

    for comp in COMPETENCIAS:
        puntajes = []
        for i in range(len(comp["indicadores"])):
            campo = f"{comp['id']}_{i}"
            valor = int(request.form.get(campo, 3))
            puntajes.append(valor)
            todos_los_puntajes.append(valor)

        promedio = statistics.mean(puntajes)
        porcentaje = round((promedio / 5) * 100, 1)
        etiqueta, color = clasificar(porcentaje)

        resultados_competencia.append({
            "id": comp["id"],
            "nombre": comp["nombre"],
            "icono": comp["icono"],
            "promedio": round(promedio, 2),
            "porcentaje": porcentaje,
            "etiqueta": etiqueta,
            "color": color,
        })

    promedio_general = statistics.mean(todos_los_puntajes)
    porcentaje_general = round((promedio_general / 5) * 100, 1)
    etiqueta_general, color_general = clasificar(porcentaje_general)

    ordenado = sorted(resultados_competencia, key=lambda c: c["porcentaje"], reverse=True)
    fortalezas = ordenado[:2]
    areas_mejora = ordenado[-2:]

    docente = request.form.get("nombre_docente", "").strip() or "Docente"
    asignatura = request.form.get("asignatura", "").strip()

    session["resultado"] = {
        "docente": docente,
        "asignatura": asignatura,
        "competencias": resultados_competencia,
        "porcentaje_general": porcentaje_general,
        "etiqueta_general": etiqueta_general,
        "color_general": color_general,
        "fortalezas": fortalezas,
        "areas_mejora": areas_mejora,
    }

    return redirect(url_for("resultados"))


@app.route("/resultados", methods=["GET"])
def resultados():
    resultado = session.get("resultado")
    if not resultado:
        return redirect(url_for("index"))
    return render_template("resultados.html", r=resultado)


@app.route("/reiniciar", methods=["GET"])
def reiniciar():
    session.pop("resultado", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
