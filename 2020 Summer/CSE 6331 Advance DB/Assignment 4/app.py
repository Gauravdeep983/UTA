import pyodbc
import ibm_db
import random
import os
import string
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

#IBM DB2 connection string
# conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

#Azure connection string
server = 'tcp:gaurav-az.database.windows.net'
database = 'gaurav-adb'
username = 'gaurav-master'
password = 'Jeevesh@123'   
driver= '{ODBC Driver 17 for SQL Server}'
conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


# Home redirect
@app.route('/')
def index():    
    return render_template('main1.html')


@app.route('/barchart', methods=["POST"])
def barchart():
    start_mag = magnitudefrom = float(request.form.get("mag_from"))
    magnitudeto = float(request.form.get("mag_to"))
    step = float(request.form.get("step"))
    list_of_data = [['Magnitude Range','Count', {'role':'style'}]]
    loop = int(0)
    while (start_mag < magnitudeto):
        end_mag = start_mag+step
        values=[]
        sql = f"(SELECT count(*) FROM earthquake where (mag between {str(round(start_mag,2))} and {str(round(end_mag,2))}) ) "

        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_tuple(stmt)
        if data:
            values.append(str(round(start_mag,2))+"-"+str(round(end_mag,2)))
            values.append(int(data[0]))
            values.append("%06x" % random.randint(0, 0xFFFFFF))
            list_of_data.append(values)
        start_mag = start_mag+step
        loop+=1    
    return render_template('barchart.html', table=list_of_data, increment=step)

@app.route('/scatterchart', methods=["POST", "GET"])
def scatter_chart():  
    pop_min = int(request.form.get("pop_min"))*1000;
    pop_max = int(request.form.get("pop_max"))*1000;
    arr = [['State', 'Registered Voters', {'role':'tooltip'}]]  
    sql = f"SELECT StateName, Totalpop, Registered FROM Voter WHERE TotalPop BETWEEN {pop_min} AND {pop_max}"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_tuple(stmt)
    while data:
        total_pop = float(data[1])/1000
        reg_voters = float(data[2])/1000
        tooltip = str(data[0])+'\nTotal pop: '+str(total_pop)+'\nReg. voters: '+ str(reg_voters)
        arr.append([total_pop, reg_voters, tooltip])
        data = ibm_db.fetch_tuple(stmt)
    return render_template('/scatterchart.html', table=arr, pop_max=pop_max)

@app.route('/linechart', methods=["POST", "GET"])
def linechart(): 
    pop_min = int(request.form.get("pop_min"))*1000;
    pop_max = int(request.form.get("pop_max"))*1000;
    arr = []
    sql = f"SELECT StateName, Totalpop, Registered FROM Voter WHERE TotalPop BETWEEN {pop_min} AND {pop_max}"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_tuple(stmt)
    while data:
        total_pop = float(data[1])/1000
        reg_voters = float(data[2])/1000
        # tooltip = str(data[0])+'\nTotal pop: '+str(total_pop)+'\nReg. voters: '+ str(reg_voters)
        arr.append([total_pop, reg_voters])
        data = ibm_db.fetch_tuple(stmt)
    return render_template('/linechart.html', data=arr)


@app.route('/q6', methods=["POST", "GET"])
def q6(): 
    arr = [['Volcano', 'Elevation']]  
    country = request.form.get("country")
    sql = f"SELECT Volcano_Name, Elev FROM volcano1 WHERE country = '{country}'"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            arr.append([row[0],row[1]])
    return render_template('/q6.html', table=arr)


@app.route('/q8', methods=["POST", "GET"])
def q8(): 
    volcano_min = request.form.get("volcano_min")
    volcano_max = request.form.get("volcano_max")
    arr = [['Volcano', 'Elevation']]  
    country = request.form.get("country")
    sql = f"SELECT Volcano_Name, Elev FROM volcano1 WHERE country = '{country}'"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            arr.append([row[0],row[1]])
    return render_template('/q6.html', table=arr)

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)