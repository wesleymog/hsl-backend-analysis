from flask import Flask
from flask_restful import Resource, Api
import sqlite3, pymysql
import pymysql.cursors

#Flask
app = Flask(__name__)
api = Api(app)

connection = pymysql.connect(host='remotemysql.com',
                             user='riPOnUyCuK',
                             password='m6YJ0faBdk',
                             database='riPOnUyCuK',
                             cursorclass=pymysql.cursors.DictCursor)
#Connection sqlite3
# conn = sqlite3.connect('hsl_db.sqlite')
# cur = conn.cursor()

cur = connection.cursor()

class MessageHealth(Resource):

    def get(self):
        return {'message': 'health'}

class CovidExams(Resource):
    def get(self):
        cur.execute("SELECT `DE_EXAME` as nome_exame, COUNT(`DE_EXAME`) AS quantidade FROM   EXAMES GROUP  BY DE_EXAME ORDER  BY Count(*) DESC")
        exames = cur.fetchall()
        return {'exames':exames}
        
api.add_resource(MessageHealth, '/health')
api.add_resource(CovidExams, '/covid-exams')

if __name__ == '__main__':
    app.run(debug=True)