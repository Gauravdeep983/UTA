import random
import os
import string
from flask import Flask, render_template, url_for, request
import psycopg2

application = Flask(__name__)

# PostgreSQL conn string
engine = psycopg2.connect(
    database="awsadb",
    user="postgres",
    password="Jeevesh123",
    host="postgres-adb.cfjuah6u50my.us-east-2.rds.amazonaws.com",
    port='5432'
)

# Home redirect
@application.route('/')
def index():
    return render_template('main1.html')

@application.route('/q6', methods=["POST", "GET"])
def q6(): 
    cur = engine.cursor();
    name = request.form.get("name")
    isTeacher = request.form.get("isTeacher")

    if(isTeacher == 'yes'):
        role = "teacher"
        id = random.randint(1,10000)
        cur.execute("INSERT INTO public.user(id, username, role) VALUES(%s, %s, %s)", (id, name, role))
        engine.commit()
        return render_template("teacher.html", name=name)
    else:
        role = "student"
        id = random.randint(1,10000)
        cur.execute("INSERT INTO public.user(id, username, role) VALUES(%s, %s, %s)", (id, name, role))
        engine.commit()
        return render_template("student.html", name=name)

@application.route('/teacher', methods=["POST", "GET"])
def teacher():
    cur = engine.cursor();
    id = random.randint(1,10000)
    name = request.form.get("name")
    question = request.form.get("question")
    sql = f"SELECT id, username, role FROM public.user WHERE username = '{name}'"
    cur.execute(sql)
    teacher = cur.fetchone()
    answer = "no"
    cur.execute("INSERT INTO public.questions(id, question, teacher, answer) VALUES (%s, %s, %s, %s)", (id, question, name, answer))
    engine.commit()

    return render_template('teacher.html', name=name)

# engine.close()  
cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        application.run(debug=True)
    else:
        application.run(host='0.0.0.0', port=int(cf_port), debug=True)