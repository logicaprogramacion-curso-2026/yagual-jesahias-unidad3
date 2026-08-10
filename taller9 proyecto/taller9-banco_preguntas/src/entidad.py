class Pregunta:
    def __init__(self, id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema):
        self.id = id
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta
        self.dificultad = dificultad
        self.tema = tema

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"[{self.id}] {self.tema} - {self.pregunta}"