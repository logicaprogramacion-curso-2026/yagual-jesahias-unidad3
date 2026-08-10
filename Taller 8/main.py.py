# GRUPO 3
class periodo_academico:
    inscripciones = ""
    matricula = ""
    nombre = ""
    asignaturas = []
    tiempo_limite = 0
    fecha_inicio = ""
    fecha_fin = ""
    examenes = ""
    actividades = ""
def __init__(self, inscripciones, matricula, nombre, asignaturas, tiempo_limite, fecha_inicio, fecha_fin, evaluaciones, examenes, actividades):
    self.inscripciones = inscripciones
    self.matricula = matricula
    self.nombre = nombre
    self.asignaturas = asignaturas
    self.tiempo_limite = tiempo_limite
    self.fecha_inicio = fecha_inicio
    self.fecha_fin = fecha_fin
    self.examenes = examenes
    self.actividades = actividades

class evaluación:
    id_evaluacion = ""
    fecha = ""
    estado_coherencia = ""
    nombre = ""
    docente_evaluador = ""
    preguntas_abiertas = []
def __init__(self, id_evaluacion, fecha, estado_coherencia, nombre, docente_evaluador, preguntas_abiertas):
    self.id_evaluacion = id_evaluacion
    self.fecha = fecha
    self.estado_coherencia = estado_coherencia
    self.nombre = nombre
    self.docente_evaluador = docente_evaluador
    self.preguntas_abiertas = preguntas_abiertas

class calificaciones:
  fecha_de_entrega = ""
  puntaje = 0
  comentario = ""
  promedio_total = 0
def __init__(self, fecha_de_entrega, puntaje, comentario, promedio_total):
    self.fecha_de_entrega = fecha_de_entrega
    self.puntaje = puntaje
    self.comentario = comentario
    self.promedio_total = promedio_total