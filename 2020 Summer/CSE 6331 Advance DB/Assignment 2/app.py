import ibm_db
import os
from flask import Flask, render_template, url_for, request, redirect
from math import radians, cos, sin, asin, sqrt, atan2

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

@app.route('/eq-above-mag6',methods=['POST','GET'])
def eq_above_mag6():
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


@app.route('/eq-within-parameters', methods=['POST','GET'])
def eq_within_parameters():
    if request.method == 'POST':
        list_of_data = []
        latitude = request.form.get('lattitude')
        longitude = request.form.get('longitude')
        min_mag = request.form.get('mag_min')
        max_mag = request.form.get('mag_max')
        from_date = str(request.form.get('from_date'))
        to_date = str(request.form.get('to_date'))
        dist = request.form.get('distance')
        params = {'latitude' : latitude, 'longitude' : longitude, 'min_mag': min_mag, 'max_mag': max_mag, 'from_date': from_date, 'to_date': to_date, 'distance': dist }

        query = f"SELECT * FROM (SELECT *,\
            (\
                (\
                    (\
                        acos(\
                            sin(( {latitude} * 0.01745329251 ))\
                            *\
                            sin(( latitude * 0.01745329251 )) + cos(( {latitude} *0.01745329251 ))\
                            *\
                            cos(( latitude * 0.01745329251)) * cos((( {longitude} - longitude) * 0.01745329251)))\
                    ) * 57.2957795131\
                ) * 60 * 1.1515 * 1.609344\
            )\
        as distance FROM EARTHQUAKE WHERE time BETWEEN '{from_date}' and '{to_date}' AND mag BETWEEN {min_mag} and {max_mag}) WHERE distance <= {dist} ORDER BY distance DESC"

        stmt = ibm_db.exec_immediate(conn, query)
        result = ibm_db.fetch_tuple(stmt)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        
        return render_template('eq-parameters.html',data=list_of_data, params=params)

        
# status = ibm_db.close(conn)
# print(status)

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)