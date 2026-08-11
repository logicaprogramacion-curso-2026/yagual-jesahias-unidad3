# Evaluación Formativa de Competencias Docentes

App web de **autoevaluación docente** construida con **Flask** (Python) y **Bootstrap 5**.
Los datos se manejan en memoria/sesión: no requiere base de datos ni login.

## ¿Qué hace?

1. El docente completa un formulario con escalas Likert (1 a 5) organizado en
   6 competencias: Planificación, Dominio disciplinar, Metodología,
   Evaluación de aprendizajes, Clima de aula y Uso de TIC.
2. Al enviar el formulario, la app calcula el promedio y porcentaje por
   competencia y el resultado general.
3. Muestra un panel de resultados con:
   - Puntaje general y nivel de logro (Inicial / En desarrollo / Satisfactorio / Destacado)
   - Gráfico radar y de barras (Chart.js)
   - Fortalezas y áreas de mejora
   - Tabla detallada por competencia

## Instalación

```bash
pip install flask
```

## Ejecución

```bash
python app.py
```

Luego abre tu navegador en: **http://localhost:5000**

## Estructura del proyecto

```
evaluacion_docente/
├── app.py                     # Backend Flask (rutas, cálculo de resultados)
├── templates/
│   ├── base.html              # Plantilla base (navbar, Bootstrap, Chart.js)
│   ├── index.html             # Formulario de autoevaluación
│   └── resultados.html        # Panel de resultados y gráficos
└── static/
    └── style.css               # Estilos adicionales
```

## Personalización

- **Competencias e indicadores**: edita la lista `COMPETENCIAS` en `app.py`.
- **Umbrales de nivel de logro**: edita la lista `NIVELES` en `app.py`.
- **Persistencia**: si en el futuro quieres guardar el historial de
  autoevaluaciones, se puede añadir SQLite/SQLAlchemy fácilmente
  reemplazando el uso de `session` por inserciones en base de datos.
