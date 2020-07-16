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
    return render_template('main.html', table)

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

@app.route('/image-upload', methods=['POST', 'GET'])
def image_upload():
    if request.method == 'POST':
        first_name = 'Dave'
        f = request.files['image']
        filename = secure_filename(f.filename)
        
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        query = "UPDATE PEOPLE SET PICTURE = '"+ filename +"'"" WHERE NAME = '" + first_name + "'"
        if f is not None:
            try:
                stmt = ibm_db.exec_immediate(conn, query)
                if stmt: 
                    return "Upload successful"
                else:
                    return "Didn't work homie"
            except:
                print("Failed to upload")
        else:
            return "Empty value"
    else:
        return "No post"

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)