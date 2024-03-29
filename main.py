from flask import Flask, make_response
from flask_restful import Resource, Api
import sqlite3, pymysql, random

import pymysql.cursors

#Flask
app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

connection = pymysql.connect(host='remotemysql.com',
                                    user='riPOnUyCuK',
                                    password='m6YJ0faBdk',
                                    database='riPOnUyCuK',
                                    cursorclass=pymysql.cursors.DictCursor)

def get_connection(connection):
    connection.ping()
    cur = connection.cursor()
    return cur
#Connection sqlite3
# conn = sqlite3.connect('hsl_db.sqlite')
# cur = conn.cursor()

def get_datasets(data, coluna, linha, valor):
    labels =[]
    data_set = []
    for info in data:
        if info[coluna] not in labels:
            labels.append(info[coluna])
    for info in data:
        if not any(d['label'] == info[linha] for d in data_set):
            dict_ ={}
            dict_['label'] = info[linha]
            dict_['data'] = [0 for _ in range(len(labels))]
            dict_['data'][labels.index(info[coluna])]=info[valor]
            color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
            dict_['backgroundColor']=[color for _ in labels]
            data_set.append(dict_)
        else:
            for d in data_set:
                if d['label'] == info[linha]:
                    d['data'][labels.index(info[coluna])]=info[valor]
    return {"labels": labels,"datasets":data_set}

def get_datasets_limit(data, coluna, linha, valor):
    labels =[]
    data_set = []
    for info in data:
        if info[coluna] not in labels and len(labels) < 4:
            labels.append(info[coluna])
    for info in data:
        if not any(d['label'] == info[linha] for d in data_set):
            if len(data_set) < 12:
                dict_ ={}
                dict_['label'] = info[linha]
                dict_['data'] = [0 for _ in range(len(labels))]
                dict_['data'][labels.index(info[coluna])]=info[valor]
                color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                dict_['backgroundColor']=[color for _ in labels]
                data_set.append(dict_)
        else:
            for d in data_set:
                if d['label'] == info[linha]:
                    d['data'][labels.index(info[coluna])]=info[valor]
    return {"labels": labels, "datasets":data_set}

def get_dataset(data_info, coluna, valor):
    labels =[]
    data = []
    background_colors = []
    print(data)
    for info in data_info:
        if info[coluna] not in labels:
            labels.append(info[coluna])
            data.append(info[valor])
            background_colors.append("#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)]))
    data_sets = [{"data":data, "backgroundColor":background_colors}]
    return {"labels": labels, "datasets":data_sets}    
class MessageHealth(Resource):

    def get(self):
        cur = get_connection(connection)
        return {'message': 'health'}
#EXAMES
class Exames(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_EXAME as exame, COUNT(DE_EXAME) AS quantidade FROM EXAME EXAME GROUP  BY DE_EXAME ORDER  BY Count(*) DESC")
        exames = cur.fetchall()
        return make_response({'exames':exames})
 
class ExamesPorClinica(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT atndmt.DE_CLINICA as clinica, count(DE_EXAME) as quantidade, DE_EXAME AS nome_exame FROM EXAME INNER JOIN EXAME_ATENDIMENTO as exmAtndmt on  EXAME.ID_EXAME = exmAtndmt.ID_EXAME INNER JOIN ATENDIMENTO as atndmt on atndmt.ID_ATENDIMENTO = exmAtndmt.ATENDIMENTO_ID GROUP BY DE_EXAME, atndmt.DE_CLINICA ORDER BY count(DE_EXAME) desc;")
        clinicas = cur.fetchall()
        info = get_datasets(clinicas[:10], 'clinica', 'nome_exame', 'quantidade')
        return make_response({'graphics':info, 'clinicas':clinicas}) 
class ExamesPorPaciente(Resource):
    def get(self, id_paciente):
        cur = get_connection(connection)
        cur.execute("SELECT pcnt.ID AS idPaciente, exm.DE_EXAME AS exame FROM EXAME AS exm INNER JOIN EXAME_ATENDIMENTO AS exmAtndm on exmAtndm.ID_EXAME = exm.ID_EXAME LEFT JOIN ATENDIMENTO AS atndm on atndm.ID_ATENDIMENTO = exmAtndm.ATENDIMENTO_ID RIGHT JOIN PACIENTE AS pcnt on pcnt.ID = atndm.ID_PACIENTE WHERE pcnt.ID = {}".format(id_paciente))
        exames = cur.fetchall()
        return make_response({'exames':exames})

class ExamesPorPacientesIdosos(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT exm.DE_EXAME as exame, COUNT(pcnt.ID_PACIENTE) as quantidade, dsfch.DT_DESFECHO as dia_atendimento FROM ATENDIMENTO INNER JOIN EXAME_ATENDIMENTO AS exmAtnd on ATENDIMENTO.ID_ATENDIMENTO = exmAtnd.ATENDIMENTO_ID INNER JOIN EXAME AS exm on exmAtnd.ID_EXAME = exm.ID_EXAME INNER JOIN PACIENTE AS pcnt on pcnt.ID_PACIENTE = ATENDIMENTO.ID_PACIENTE INNER JOIN DESFECHO AS dsfch on dsfch.ID_DESFECHO = ATENDIMENTO.ID_DESFECHO WHERE pcnt.AA_NASCIMENTO < 1961 GROUP BY exm.DE_EXAME, dsfch.DT_DESFECHO ORDER BY COUNT(exm.DE_EXAME) desc;")
        exames = cur.fetchall()
        info = get_datasets(exames[:10], 'exame', 'dia_atendimento', 'quantidade')
        return make_response({'graphics':info, 'exames':exames}) 
class ExamesPorMunicipio(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT exm.DE_EXAME as exame, COUNT(exm.DE_EXAME) as quantidade, pcnt.CD_MUNICIPIO as municipio FROM ATENDIMENTO INNER JOIN EXAME_ATENDIMENTO AS exmAtnd on ATENDIMENTO.ID_ATENDIMENTO = exmAtnd.ATENDIMENTO_ID INNER JOIN EXAME AS exm on exmAtnd.ID_EXAME = exm.ID_EXAME INNER JOIN PACIENTE AS pcnt on pcnt.ID_PACIENTE = ATENDIMENTO.ID_PACIENTE GROUP BY exm.DE_EXAME, pcnt.CD_MUNICIPIO ORDER BY COUNT(exm.DE_EXAME) desc;")
        exams = cur.fetchall()
        info = get_datasets(exams[:10], 'exame', 'municipio', 'quantidade')
        return make_response({'graphics':info, 'exames':exams}) 

class ExamesPorAVGAnoNasc(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_EXAME AS exame, cast(ROUND(cast(AVG(pcnt.AA_NASCIMENTO) as decimal)) as CHAR(4)) AS media_idade FROM EXAME AS exm INNER JOIN EXAME_ATENDIMENTO AS exmAtndmt on exmAtndmt.ID_EXAME = exm.ID_EXAME INNER JOIN ATENDIMENTO AS atdnmt on atdnmt.ID_ATENDIMENTO = exmAtndmt.ATENDIMENTO_ID INNER JOIN PACIENTE as pcnt on pcnt.ID_PACIENTE = atdnmt.ID_PACIENTE GROUP BY DE_EXAME")
        exams = cur.fetchall()
        return make_response({'exams':exams})
#CLINICAS
class ClinicaPorDesistencia(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT ATENDIMENTO.DE_CLINICA AS clinica, COUNT(DESFECHO.DE_DESFECHO) AS desistencias FROM DESFECHO, ATENDIMENTO WHERE DESFECHO.DE_DESFECHO like 'Desistência do atendimento' AND ATENDIMENTO.ID_DESFECHO = DESFECHO.ID_DESFECHO GROUP BY DE_CLINICA ORDER BY COUNT(DESFECHO.DE_DESFECHO) DESC")
        clinicas = cur.fetchall()
        return make_response({'clinicas':clinicas})
        
class ClinicaPorAtendimentos(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_CLINICA AS clinica, COUNT(DE_CLINICA) AS atendimentos FROM ATENDIMENTO GROUP BY DE_CLINICA ORDER BY ATENDIMENTOS DESC")
        clinicas = cur.fetchall()
        return make_response({'clinicas':clinicas})
class ClinicaPorAltasObitos(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_CLINICA as clinica, desf.DE_DESFECHO AS desfecho, COUNT(desf.DE_DESFECHO) AS quantidade FROM ATENDIMENTO INNER JOIN DESFECHO AS desf on ATENDIMENTO.ID_DESFECHO = desf.ID_DESFECHO WHERE desf.DE_DESFECHO like 'Alta Administrativa' GROUP BY DE_CLINICA, desf.DE_DESFECHO UNION SELECT DE_CLINICA as clinica,  desf.DE_DESFECHO AS desfecho, COUNT(desf.DE_DESFECHO) AS quantidade FROM ATENDIMENTO INNER JOIN DESFECHO AS desf on ATENDIMENTO.ID_DESFECHO = desf.ID_DESFECHO WHERE desf.DE_DESFECHO like 'Obito%' GROUP BY DE_CLINICA, desf.DE_DESFECHO ORDER BY quantidade DESC;")
        clinicas = cur.fetchall()
        info = get_datasets_limit(clinicas, 'desfecho', 'clinica', 'quantidade')
        return make_response({'graphics':info, 'clinicas':clinicas}) 
# DESFECHOS
class Desfechos(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_DESFECHO as desfecho ,count(DE_DESFECHO) as quantidade FROM DESFECHO GROUP BY DE_DESFECHO ORDER BY count(DE_DESFECHO) DESC;")
        desfechos = cur.fetchall()
        graphics = get_dataset(desfechos, "desfecho", "quantidade")
        return make_response({'desfechos':desfechos, "graphics":graphics})

class DesfechosPorMunicipio(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT desf.DE_DESFECHO AS desfecho,  COUNT(desf.DE_DESFECHO) as quantidades, pcnt.CD_MUNICIPIO as municipio FROM ATENDIMENTO INNER JOIN DESFECHO AS desf on ATENDIMENTO.ID_DESFECHO = desf.ID_DESFECHO INNER JOIN PACIENTE AS pcnt on ATENDIMENTO.ID_PACIENTE = pcnt.ID_PACIENTE GROUP BY desf.DE_DESFECHO, pcnt.CD_MUNICIPIO ORDER BY COUNT(desf.DE_DESFECHO) desc;")
        desfechos = cur.fetchall()
        info = get_datasets(desfechos[:10], 'desfecho', 'municipio', 'quantidades')
        return make_response({'graphics':info, 'desfechos':desfechos}) 

class DesfechosPorIdade(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT S.DESFECHO as desfecho, 2021-S.AA_NASCIMENTO as idade, COUNT(S.DESFECHO) as quantidade FROM (SELECT ID_CLINICA, DT_ATENDIMENTO, desf.DE_DESFECHO AS DESFECHO, PACIENTE.ID_PACIENTE, PACIENTE.AA_NASCIMENTO FROM ATENDIMENTO INNER JOIN PACIENTE on ATENDIMENTO.ID_PACIENTE = PACIENTE.ID_PACIENTE and PACIENTE.AA_NASCIMENTO != 'YYYY' INNER JOIN DESFECHO AS desf on ATENDIMENTO.ID_DESFECHO = desf.ID_DESFECHO WHERE DE_DESFECHO like 'Alta Administrativa' or DE_DESFECHO like 'Obito%' ORDER BY ID_CLINICA ASC) AS S GROUP BY S.DESFECHO,S.AA_NASCIMENTO ORDER BY quantidade DESC")
        desfechos = cur.fetchall()
        info = get_datasets_limit(desfechos, 'desfecho', 'idade', 'quantidade')
        return make_response({'graphics':info, 'desfechos':desfechos}) 

# PACIENTES
class Pacientes(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT ID, ID_PACIENTE, CD_MUNICIPIO FROM PACIENTE")
        pacientes = cur.fetchall()
        return make_response({'pacientes':pacientes})



class HelloWorld(Resource):
    def get(self):
        return make_response({'hello': 'world'})
'''

    ROTAS

'''

api.add_resource(HelloWorld, '/')
api.add_resource(MessageHealth, '/health')
#Exames
api.add_resource(Exames, '/exames')
api.add_resource(ExamesPorClinica, '/exames/clinica')
api.add_resource(ExamesPorPacientesIdosos, '/exames/paciente_idoso')
api.add_resource(ExamesPorPaciente, '/exames/paciente/<int:id_paciente>')
api.add_resource(ExamesPorMunicipio, '/exames/municipio')
api.add_resource(ExamesPorAVGAnoNasc, '/exames/avg_nasc')

#Clinicas
api.add_resource(ClinicaPorAtendimentos, '/clinicas/atendimento')
api.add_resource(ClinicaPorDesistencia, '/clinicas/desistencia')
api.add_resource(ClinicaPorAltasObitos, '/clinicas/altas_obitos')

#Desfechos
api.add_resource(Desfechos, '/desfechos')
api.add_resource(DesfechosPorMunicipio, '/desfechos/municipio')
api.add_resource(DesfechosPorIdade, '/desfechos/idade')

#Paciente
api.add_resource(Pacientes, '/pacientes')


if __name__ == '__main__':
    app.run(debug=True)