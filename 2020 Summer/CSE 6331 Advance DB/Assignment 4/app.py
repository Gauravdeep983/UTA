import pyodbc
import ibm_db
# import pypyodbc
import os
import string
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

#IBM DB2 connection string
conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

#Azure connection string
# server = 'tcp:gaurav-az.database.windows.net'
# database = 'gaurav-adb'
# username = 'gaurav-master'
# password = 'Jeevesh@123'   
# driver= '{ODBC Driver 17 for SQL Server}'
# conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


# Home redirect
@app.route('/')
def index():    
    return render_template('main.html')


@app.route('/barchart')
def barchart():
    start_mag = magnitudefrom = 1.0
    magnitudeto = 9.0
    N = 100
    step = 0.1
    list_of_data = [['Magnitude Range','Count']]
    loop = int(0)
    while (start_mag < magnitudeto) and (loop<N):
        end_mag = start_mag+step
        values=[]
        sql = f"(SELECT count(*)\
        FROM earthquake where (mag between {str(round(start_mag,2))} and {str(round(end_mag,2))}) ) "
        # print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_tuple(stmt)
        if data:
            values.append(str(round(start_mag,2))+"-"+str(round(end_mag,2)))
            #data = ibm_db.fetch_tuple(stmt)
            values.append(int(data[0]))
            list_of_data.append(values)
        start_mag = start_mag+step
        loop+=1    
    return render_template('barchart.html', table=list_of_data)

@app.route('/scatterchart')
def scatter_chart():    
    pop_min = int(1*1000);
    pop_max = int(6*1000);
    sql = f"SELECT * FROM Voter WHERE TotalPop BETWEEN {pop_min} AND {pop_max}"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_tuple(stmt)
    if data:
        

    return render_template('scatterchart.html')

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)