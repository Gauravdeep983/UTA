import ibm_db
import os
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah blah blah blah'

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

@app.route('/')
def index():
    arr=[]
    query = "SELECT * FROM PERSONS"
    stmt = ibm_db.exec_immediate(conn, query)
    data = ibm_db.fetch_tuple(stmt)
    while data:
        arr.append(data)
        data = ibm_db.fetch_tuple(stmt)
    return render_template('index.html', table=arr)


@app.route('/search', methods=['POST', 'GET'])
def search_user():
    if request.method == 'POST':
        first_name = request.form.get("name")
        if first_name is not None:
            query = "SELECT * FROM PERSONS WHERE PERSON = '" + first_name + "'"
        else:
            print("Empty value")

        stmt = ibm_db.exec_immediate(conn, query)
        data = ibm_db.fetch_tuple(stmt)
        return render_template('search-user.html', user=data)

@app.route('/find-keyword',methods=['POST','GET'])
def find_keyword():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        query = "SELECT * from PERSONS WHERE DESCRIPTION='" + keyword + "'"
        print(query)
        stmt = ibm_db.exec_immediate(conn, query)
        data = ibm_db.fetch_tuple(stmt)
        return render_template('q7.html', user=data)

@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        name = request.form.get('name')
        sql = "DELETE FROM PERSONS WHERE PERSON='"+name+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        if stmt:
            return redirect('/')
        return redirect('/')

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        name = request.form.get('name')
        sql = "SELECT * FROM PERSONS WHERE PERSON='"+name+"'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_tuple(stmt)
        if stmt:
            return render_template('update-user.html', user=data)

@app.route('/update-person',methods=['POST','GET'])
def update_person():
    if request.method == 'POST':
        old = request.form.get('old')
        name = request.form.get('name')
        year = request.form.get('year')
        picture = request.form.get('picture')
        description = request.form.get('description')
        sql = "UPDATE PERSONS SET PERSON = '"+name+"', YEAR = "+year+", PICTURE = '"+picture+", DESCRIPTION = '"+description+" WHERE PERSON='"+old+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        if stmt:
            return redirect('/')
        return "didnt work"

# status = ibm_db.close(conn)
# print(status)

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)