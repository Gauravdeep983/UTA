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

#Find the nearest earthquake with mag>6
@app.route('/magnitude',methods=['POST'])
def magnitude():
    value=[]
    lat = request.form.get("lat")
    long  = request.form.get("long")
    query = f"SELECT *,\
            (\
                (\
                    (\
                        acos(\
                            sin(( {lat} * 0.01745329251 ))\
                            *\
                            sin(( latitude * 0.01745329251 )) + cos(( {lat} *0.01745329251 ))\
                            *\
                            cos(( latitude * 0.01745329251)) * cos((( {long} - longitude) * 0.01745329251)))\
                    ) * 57.2957795131\
                ) * 60 * 1.1515\
            )\
        as distance FROM earthquake where mag>6 order by distance asc limit 1"
    stmt1 = ibm_db.exec_immediate(conn, query)
    result = ibm_db.fetch_both(stmt1)
    while result:
        value.append(result)
        result = ibm_db.fetch_both(stmt1)
    return render_template('magnitude.html', search=value, lat=lat, long=long)

#Earthquakes within a user-inputted distance
@app.route('/within-distance',methods=['POST'])
def within_distance():
    value=[]
    lat = request.form.get("lat")
    long  = request.form.get("long")
    dist = request.form.get("dist")
    query = f"SELECT * FROM(\
        SELECT *,\
            (\
                (\
                    (\
                        acos(\
                            sin(( {lat} * 0.01745329251 ))\
                            *\
                            sin(( latitude * 0.01745329251 )) + cos(( {lat} *0.01745329251 ))\
                            *\
                            cos(( latitude * 0.01745329251)) * cos((( {long} - longitude) * 0.01745329251)))\
                    ) * 57.2957795131\
                ) * 60 * 1.1515 * 1.609344\
            )\
        as distance FROM earthquake)\
        where distance <= {dist} order by distance asc"

    stmt1 = ibm_db.exec_immediate(conn, query)
    result = ibm_db.fetch_both(stmt1)
    while result:
        value.append(result)
        result = ibm_db.fetch_both(stmt1)
    return render_template('within-distance.html', search=value, lat=lat, long=long, dist=dist)


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

@app.route('/latlong',methods=['POST'])
def latlong():
    value=[]
    lat1 = float(request.form.get("lat1"))
    long1  = float(request.form.get("long1"))
    lat2 = float(request.form.get("lat2"))
    long2  = float(request.form.get("long2"))

    #Set min. latitude
    if lat1 < lat2:
        min_lat = lat1
        max_lat = lat2
    else:
        min_lat = lat2
        max_lat = lat1

    #Set min. longitude
    if long1 < long2:
        min_long = long1
        max_long = long2
    else:
        min_long = long2
        max_long = long1
    
    query = f"SELECT * FROM LATLONG WHERE LATITUDE BETWEEN {min_lat} and {max_lat} AND LONGITUDE BETWEEN {min_long} and {max_long}"

    stmt1 = ibm_db.exec_immediate(conn, query)
    result = ibm_db.fetch_both(stmt1)
    while result:
        value.append(result)
        result = ibm_db.fetch_both(stmt1)
    return render_template('latlong-results.html', search=value)
# status = ibm_db.close(conn)
# print(status)

cf_port = os.getenv("PORT")
if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)