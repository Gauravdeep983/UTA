from flask import Flask, render_template, url_for, request, redirect
import ibm_db

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

app = Flask(__name__)

# TODO: 1) Basic bootstrap and flask template
# TODO: 2) Read csv via flask or upload csv to DB2
# TODO: 2.1) Display all records from DB2 in Web UI
# TODO: 5) CRUD
# TODO: 6) Cloud deployment

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

if __name__ == "__main__":
    app.run(debug=True)