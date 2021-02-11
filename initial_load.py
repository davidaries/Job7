# import random
import db_tools
# used_tokens = []
vocab_en = ['Name','diagnosis','treat','Hello! Please treat:','flu','Pause','Un Pause','Return','Event','Time',
            'Job','Timer','Log','Sex','Age','Phone','Chief Complaint','Test','Weight','Submit','Male','Female',
            'Role','Receptionist','Assistant','Provider','Lab Technician','Headache','Fever','COVID','Flu Test',
            'Coronavirus Test','Task','Receive','Room','Diagnose','Pneumonia','Appendicitis','Cholelithiasis','Years',
            'Kgs','User ID','Password','HgA1c','Height','Meters','BMI','Status','Priority','Forward','Reassign','Skip',
            'Drop','Close','Assigned','Staffers','User','Action','Comments','Language Preference','English','Spanish']

vocab_sp = ['Nombre','diagnostico','curar','Hola! Por favor curar:','gripe','Pausa','Reanudar','Regresa','Evento','Hora',
            'Trabajo','Temporizador','Sesion','Sexo','Edad','Teléfono','Problema','Prueba','Peso','Enviar','Hombre',
            'Mujer','Cargo','Recepcionista','Asistente','Doctor','Técnico de Laboratorio','dolor de cabeza','fiebre',
            'COVID','Prueba de gripe','Prueba de COVID','Tarea','Receive','Dar una habitacion','Diagnosticar','Neumonía',
            'Apendicitis','Colelitiasis','Años','Kgs','el nombre de usuario','la contraseña','HgA1c','la estatura',
            'Meters','BMI','Estado','Prioridad','Reenviar','Reasignar','Saltarse','Soltar','Cerrar','Asignado','Empleados',
            'Usuario','Accion','Comentarios','Preferencia de idioma','ingles','espanol']

def initial_load(conn):
    for (ve, vs) in zip(vocab_en, vocab_sp):
        # ran = random.randint(0000000,9999999)
        # if "~%07d"%ran not in used_tokens:
        #     token = "~%07d"%ran
        # else:
        #     while "~%07d"%ran in used_tokens:
        #         ran = random.randint(0000000, 9999999)
        #     token = "~%07d"%ran
        token = db_tools.generate_token(conn)
        other = 'NA'
        vals_en ='''('%s','%s','%s')'''%(token,ve,other)
        vals_sp ='''('%s','%s','%s')'''%(token,vs,other)
        dict_en = 'English_words'
        dict_sp = 'Spanish_words'
        addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' %(dict_en,vals_en)
        addition_sp = '''INSERT INTO %s (vocab, term, other)VALUES %s''' %(dict_sp,vals_sp)

        print(addition_en)
        print(addition_sp)

        conn.execute(addition_en)
        conn.execute(addition_sp)
    conn.commit()