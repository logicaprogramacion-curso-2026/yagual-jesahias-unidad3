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