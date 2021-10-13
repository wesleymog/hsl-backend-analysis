from flask import Flask, make_response
from flask_restful import Resource, Api
import sqlite3, pymysql
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
    try:
        cur = connection.cursor()
    except:
        connection = pymysql.connect(host='remotemysql.com',
                                    user='riPOnUyCuK',
                                    password='m6YJ0faBdk',
                                    database='riPOnUyCuK',
                                    cursorclass=pymysql.cursors.DictCursor)
        cur = connection.cursor()
    return cur
#Connection sqlite3
# conn = sqlite3.connect('hsl_db.sqlite')
# cur = conn.cursor()


class MessageHealth(Resource):

    def get(self):
        cur = get_connection(connection)
        return {'message': 'health'}

class CovidExams(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT `DE_EXAME` as nome_exame, COUNT(`DE_EXAME`) AS quantidade FROM   EXAMES GROUP  BY DE_EXAME ORDER  BY Count(*) DESC")
        exames = cur.fetchall()
        return make_response({'exames':exames})
 
class ClinicaDesistencia(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT ATENDIMENTO.DE_CLINICA AS clinica, COUNT(DESFECHO.DE_DESFECHO) AS desistencias FROM DESFECHO, ATENDIMENTO WHERE DESFECHO.DE_DESFECHO like 'Desistência do atendimento' AND ATENDIMENTO.ID_DESFECHO = DESFECHO.ID_DESFECHO GROUP BY DE_CLINICA ORDER BY COUNT(DESFECHO.DE_DESFECHO) DESC")
        clinicas = cur.fetchall()
        return make_response({'clinicas':clinicas})
        
class ClinicaAtendimentos(Resource):
    def get(self):
        cur = get_connection(connection)
        cur.execute("SELECT DE_CLINICA AS clinica, COUNT(DE_CLINICA) AS atendimentos FROM ATENDIMENTO GROUP BY DE_CLINICA ORDER BY ATENDIMENTOS DESC")
        clinicas = cur.fetchall()
        return make_response({'clinicas':clinicas})

class HelloWorld(Resource):
    def get(self):
        return make_response({'hello': 'world'})

api.add_resource(HelloWorld, '/')
api.add_resource(MessageHealth, '/health')
api.add_resource(CovidExams, '/covid-exams')
api.add_resource(ClinicaAtendimentos, '/clinicas/atendimento')
api.add_resource(ClinicaDesistencia, '/clinicas/desistencia')

if __name__ == '__main__':
    app.run(debug=True)