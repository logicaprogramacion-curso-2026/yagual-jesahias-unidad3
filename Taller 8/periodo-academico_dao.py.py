class periodo_academico_dao:
    def __init__(self,db):
        self.db = db

    def crear_tabla(self):
        self.db.cursor.execute('''CREATE TABLE IF NOT EXISTS periodo_academico (id INTEGER PRIMARY KEY AUTOINCREMENT nombre TEXT NOT NULL, direccion TEXT, telefono TEXT, correo TEXT)''')
        
    def insertar(self, periodo_academico):
        self.db.cursor.execute('''INSERT INTO periodo_academico (inscripciones, matricula,nombre,asignaturas,tiempo_limite,fecha_inicio,fecha_fin,examenes,
    actividades, VALUES(?,?,?,?)''', (periodo_academico.inscripciones
                                      ,periodo_academico.matricula
                                      ,periodo_academico.asignaturas
                                      ,periodo_academico.tiempo_limite
                                      ,periodo_academico.fecha_inicio 
                                      ,periodo_academico.fecha_fin
                                      ,periodo_academico.examenes 
                                      ,periodo_academico.actividades))