import ibm_db
import os
from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

app = Flask(__name__)
img_path = 'static/images/'
app.config['UPLOAD_FOLDER'] = img_path
app.config['SECRET_KEY'] = 'blah blah blah blah'

@app.route('/')
def index():
    arr=[]
    query = "SELECT * FROM PEOPLE"
    stmt = ibm_db.exec_immediate(conn, query)
    data = ibm_db.fetch_tuple(stmt)

    while data:
        arr.append(data)
        data = ibm_db.fetch_tuple(stmt)
    return render_template('main.html', table=arr)

@app.route('/search', methods=['POST', 'GET'])
def search_user():
    if request.method == 'POST':
        first_name = request.form.get("name")
        if first_name is not None:
            query = "SELECT * FROM PEOPLE WHERE NAME = '" + first_name + "'"
        else:
            print("Empty value")

        stmt = ibm_db.exec_immediate(conn, query)
        data = ibm_db.fetch_tuple(stmt)
        return render_template('search-user.html', user=data)


@app.route('/show-images',methods=['POST','GET'])
def show_images_in_range():
    if request.method == 'POST':
        salary = request.form.get('salary')
        list_of_data = []
        sql = "SELECT * FROM PEOPLE where salary between 0 and "+salary
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        return render_template('show_images_range.html',data=list_of_data)

@app.route('/change-caption',methods=['POST','GET'])
def change_keyword():
    if request.method == 'POST':
        name = request.form.get('name')
        caption = request.form.get('caption')
        query = "UPDATE PEOPLE SET KEYWORDS='" + str(caption) + "' WHERE NAME='" + str(name) + "'"
        print(query)
        stmt = ibm_db.exec_immediate(conn, query)
        while stmt:
            return redirect('/')

# Change salary
@app.route('/change-salary',methods=['POST','GET'])
def change_salary():
    if request.method == 'POST':
        name = request.form.get('name')
        salary = request.form.get('salary')
        sql = "UPDATE PEOPLE SET SALARY = "+salary+" WHERE NAME ='"+name+"'"
        stmt = ibm_db.exec_immediate(conn, sql)
        if stmt:            
            return redirect('/')

# Delete person
@app.route('/delete-person',methods=['POST','GET'])
def delete_person():
    if request.method == 'POST':
        name = request.form.get('name')
        sql = "DELETE FROM PEOPLE WHERE NAME ='"+name+"'"
        stmt = ibm_db.exec_immediate(conn, sql)
        if stmt:
            return redirect('/')

# Change picture for a name
@app.route('/update-picture',methods=['POST','GET'])
def update_picture():
    if request.method == 'POST':
        name = request.form.get('name')
        picture = request.form.get('picture')
        list_of_data = []
        sql = "UPDATE PEOPLE SET PICTURE ='"+picture+"' WHERE NAME='"+name+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        if stmt:
            sql = "select * from people where name ='"+name+"'"
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_tuple(stmt)
            # print(result)
            while result:
                list_of_data.append(result)
                result = ibm_db.fetch_tuple(stmt)
            return render_template('update-image.html',data=list_of_data)
        return render_template('update-image.html',data=list_of_data)
            

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)