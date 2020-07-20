import ibm_db
import os
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah blah blah blah'

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")

@app.route('/')
def index():
    arr=[]
    query = "SELECT * FROM EARTHQUAKE LIMIT 10"
    stmt = ibm_db.exec_immediate(conn, query)
    data = ibm_db.fetch_tuple(stmt)
    while data:
        arr.append(data)
        data = ibm_db.fetch_tuple(stmt)
    return render_template('main.html', table=arr)

@app.route('/eqabovemag6',methods=['POST','GET'])
def eqabovemag6():
    if request.method =='POST':
        latitude = request.form.get('latitudeValue')
        longitude = request.form.get('longitudeValue')
        list_of_data =[]
        sql ="SELECT *,\
        (\
            (\
                (\
                    acos(\
                        sin(("+latitude+" * 0.01745329251))\
                        *\
                        sin((latitude * 0.01745329251)) +\
                        cos(("+latitude+" * 0.01745329251))\
                        *\
                        cos((latitude * 0.01745329251)) \
                        * \
                        cos((("+longitude+" - longitude) * 0.01745329251))) \
                ) * 57.2957795131\
            ) * 60 * 1.1515 \
        )\
        as distance FROM earthquake where mag > 6  ORDER BY Distance asc LIMIT 1"
# print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
# print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        print(list_of_data)
        return render_template('eqmagabove6.html',data=list_of_data,lat=latitude,long=longitude)



# status = ibm_db.close(conn)
# print(status)

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)