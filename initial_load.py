# import random
import db_tools
from icecream import ic

# vocab_en = ['Name','diagnosis','treat','Hello! Please treat:','flu','Pause','Un Pause','Return','Event','Time',
#             'Job','Timer','Log','Sex','Age','Phone','Chief Complaint','Test','Weight','Submit','Male','Female',
#             'Role','Receptionist','Assistant','Provider','Lab Technician','Headache','Fever','COVID','Flu Test',
#             'Coronavirus Test','Task','Receive','Room','Diagnose','Pneumonia','Appendicitis','Cholelithiasis','Years',
#             'Kgs','User ID','Password','HgA1c','Height','Meters','BMI','Status','Priority','Forward','Reassign','Skip',
#             'Drop','Close','Assigned','Staffers','User','Action','Comments','Language Preference','English','Spanish']
#
# vocab_sp = ['Nombre','diagnostico','curar','Hola! Por favor curar:','gripe','Pausa','Reanudar','Regresa','Evento','Hora',
#             'Trabajo','Temporizador','Sesion','Sexo','Edad','Teléfono','Problema','Prueba','Peso','Enviar','Hombre',
#             'Mujer','Cargo','Recepcionista','Asistente','Doctor','Técnico de Laboratorio','dolor de cabeza','fiebre',
#             'COVID','Prueba de gripe','Prueba de COVID','Tarea','Receive','Dar una habitacion','Diagnosticar','Neumonía',
#             'Apendicitis','Colelitiasis','Años','Kgs','el nombre de usuario','la contraseña','HgA1c','la estatura',
#             'Meters','BMI','Estado','Prioridad','Reenviar','Reasignar','Saltarse','Soltar','Cerrar','Asignado','Empleados',
#             'Usuario','Accion','Comentarios','Preferencia de idioma','ingles','espanol']
# vocab_en = ['Pneumonia', 'Appendicitis', 'Cholelithiasis', 'Influenza', 'Hip Fracture - femoral neck',
#             'Upper Respiratory Infection', 'Frostbite', 'HIV']
# icd10_words = ['Pneumonia, unspecified', 'Unspecified appendicitis', 'Cholelithiasis',
#                'Influenza due to unidentified influenza virus',
#                'Fracture of neck of femur NOS', 'Acute upper respiratory infection, unspecified',
#                'Superficial frostbite',
#                'Unspecified human immunodeficiency virus [HIV] disease]']
# icd10_codes = ['J18.9', 'K37', 'K10', 'J11', 'S72.00', 'J06.9', 'T33', 'B24']
# umls_words = ['Pneumonia', 'Appendicitis', 'Cholelithiasis', 'Influenza, virus not identified',
#               'Femoral Neck Fractures',
#               'Upper Respiratory Infections', 'Frostbite', 'HIV Infections', ]
# umls_cui = ['C0032285', 'C0003615', 'C0008350', 'C0494639', 'C0015806', 'C0041912', 'C0016736', 'C0019693']
#
#
# def initial_load(conn):
#     for (ve, icdw, icdc, umlw, umlc) in zip(vocab_en, icd10_words, icd10_codes, umls_words, umls_cui):
#         vocab = db_tools.generate_vocab(conn)
#         other = 'NA'
#         vals_en = '''('%s','%s','%s')''' % (vocab, ve, other)
#         vals_icdw = '''('%s','%s','%s')''' % (vocab, icdw, other)
#         vals_icdc = '''('%s','%s','%s')''' % (vocab, icdc, other)
#         vals_umlsw = '''('%s','%s','%s')''' % (vocab, umlw, other)
#         vals_umlsc = '''('%s','%s','%s')''' % (vocab, umlc, other)
#         dict_en = 'English_words'
#         dict_icdw = 'ICD10_words'
#         dict_icdc = 'ICD10_codes'
#         dict_umlsw = 'UMLS_words'
#         dict_umlsc = 'UMLS_CUI'
#         addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dict_en, vals_en)
#         addition_icdw = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dict_icdw, vals_icdw)
#         addition_icdc = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dict_icdc, vals_icdc)
#         addition_umlsw = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dict_umlsw, vals_umlsw)
#         addition_umlsc = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dict_umlsc, vals_umlsc)
#
#         conn.execute(addition_en)
#         conn.execute(addition_icdw)
#         conn.execute(addition_icdc)
#         conn.execute(addition_umlsw)
#         conn.execute(addition_umlsc)
#
#         # conn.execute(addition_en)
#         # conn.execute(addition_sp)
#     conn.commit()
