import ibm_db
import os
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

conn = ibm_db.connect("hidden")

app.config['SECRET_KEY'] = 'blah blah blah blah'

@app.route('/')
def index():
    return render_template('main.html')
    
@app.route('/id')
def id_page():
    return render_template('id.html')

@app.route('/search-picture')
def pic_page():
    return render_template('search-picture.html')

@app.route('/id-fetch', methods=['POST', 'GET'])
def search_user():
    if request.method == 'POST':
        id = request.form.get("id")
        if id is not None:
            query = "SELECT * FROM NAMES WHERE ID = " +id
            stmt = ibm_db.exec_immediate(conn, query)
            data = ibm_db.fetch_tuple(stmt)
            return render_template('search-user.html', user=data)
    else:
        return "Doesnt work"

@app.route('/search-results', methods=['POST', 'GET'])
def search_results():
    if request.method == 'POST':
        pic = request.form.get("pic")
        if pic is not None:
            query = "SELECT * FROM NAMES WHERE PICTURE = '" +pic + "'"
            stmt = ibm_db.exec_immediate(conn, query)
            data = ibm_db.fetch_tuple(stmt)
            return render_template('results-q7.html', user=data)
    else:
        return "Doesnt work"


cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)