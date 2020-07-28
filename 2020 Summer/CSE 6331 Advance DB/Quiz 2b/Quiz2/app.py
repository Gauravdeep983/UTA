from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
import sys
import os

import ibm_db

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=zgx10325;PWD=nk^ttsk5lffq6v0h;", "", "")


app = Flask(__name__)

bootstrap = Bootstrap(app)

# configurations
app.config['SECRET_KEY'] = 'blah blah blah blah'
cf_port = os.getenv("PORT")

# Routes
# Index Page


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# --------------------------------------------------------

@app.route('/qtask1', methods=['POST', 'GET'])
def qtask1():
    print('test')
    if request.method == 'POST':
        id_value = request.form.get('idValue')
        list_of_data = []
        sql = " select * from Q where id='"+id_value+"' limit 1"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        print(result)
        mag_value = float(result[3])
        print(mag_value)
        sql = "select l.place, q.time, q.id, q.depth, q.mag, q.nst, q.error FROM Q q INNER JOIN L l on l.id = q.id  where q.mag between '"+str(mag_value-0.1)+"' and '"+str(mag_value+0.1)+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        print(list_of_data)
        return render_template('qtask1.html', data=list_of_data)


@app.route('/qtask6', methods=['POST', 'GET'])
def qtask6():
    if request.method == 'POST':
        latitude_one = float(request.form.get('latitudeValueOne'))
        longitude_one = float(request.form.get('longitudeValueOne'))
        latitude_two = float(request.form.get('latitudeValueTwo'))
        longitude_two = float(request.form.get('longitudeValueTwo'))
        depth_from = float(request.form.get('depthFrom'))
        depth_to = float(request.form.get('depthTo'))
        if latitude_one > latitude_two:
            latitude_one, latitude_two = latitude_two, latitude_one
            print('one')

        if longitude_one > longitude_two:
            longitude_one, longitude_two = longitude_two, longitude_one
            print('two')

        list_of_data = []
        sql = "select l.place, q.time, q.id, q.depth, q.mag, q.nst, q.error FROM Q q INNER JOIN L l on l.id = q.id  where (l.latitude between '"+str(latitude_one)+"' and '"+str(latitude_two)+"') and (l.longitude between '"+str(longitude_one)+"' and '"+str(longitude_two)+"' ) and q.depth between '"+str(depth_from)+"' and '"+str(depth_to)+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        print(list_of_data)
        return render_template('qtask1.html', data=list_of_data)



@app.route('/qtask7', methods=['POST', 'GET'])
def qtask7():
    if request.method == 'POST':
        location = request.form.get('locationValue')
        depth_from = float(request.form.get('depthFrom'))
        depth_to = float(request.form.get('depthTo'))
        distance = float(request.form.get('distanceValue'))
        distance_in_degrees = distance/111

        sql = "(select l.latitude, l.longitude from L l Inner Join Q q on l.id = q.id where l.place like '%"+location+"%' AND q.DEPTH BETWEEN '"+str(depth_from)+"' AND '"+str(depth_to)+"')"
        print(sql)
        list_of_data = []
        initial_result=[]
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        while result:
            initial_result.append(result)
            result = ibm_db.fetch_tuple(stmt)
        print(f"list of data={initial_result}")
        for i in initial_result:
            latitude_one = float(i[0])-distance_in_degrees
            latitude_two = float(i[0])+distance_in_degrees
            longitude_one = float(i[1])-distance_in_degrees
            longitude_two = float(i[1])+distance_in_degrees
            if latitude_one > latitude_two:
                latitude_one, latitude_two = latitude_two, latitude_one
                print('one')

            if longitude_one > longitude_two:
                longitude_one, longitude_two = longitude_two, longitude_one
                print('two')
            sql = " select l.place as place, q.time as time, q.id, q.depth as depth, q.mag as mag, q.nst as nst, q.error as error FROM Q q INNER JOIN L l on l.id = q.id  where (l.latitude between '"+str(latitude_one)+"' and '"+str(latitude_two)+"') and (l.longitude between '"+str(longitude_one)+"' and '"+str(longitude_two)+"'  )  ORDER BY MAG DESC LIMIT 1 "
            print(sql)
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_tuple(stmt)
            while result:
                list_of_data.append(result)
                result = ibm_db.fetch_tuple(stmt)

        print(list_of_data)
        return render_template('qtask1.html', data=list_of_data)



@app.route('/qtask8', methods=['POST', 'GET'])
def qtask8():
    if request.method == 'POST':
        latitude_one = float(request.form.get('latitudeValueOne'))
        longitude_one = float(request.form.get('longitudeValueOne'))
        latitude_two = float(request.form.get('latitudeValueTwo'))
        longitude_two = float(request.form.get('longitudeValueTwo'))
        N = request.form.get('NValue')
        if latitude_one > latitude_two:
            latitude_one, latitude_two = latitude_two, latitude_one
            print('one')

        if longitude_one > longitude_two:
            longitude_one, longitude_two = longitude_two, longitude_one
            print('two')

        list_of_data = []
        sql = " select * from (select l.place, q.time, q.id, q.depth, q.mag, q.nst, q.error FROM Q q INNER JOIN L l on l.id = q.id  where (l.latitude between '"+str(latitude_one)+"' and '"+str(latitude_two)+"') and (l.longitude between '"+str(longitude_one)+"' and '"+str(longitude_two)+"'  ))  limit '"+N+"'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        print(list_of_data)
        return render_template('qtask1.html', data=list_of_data)





# --------------------------------------------------------
@app.route('/task1', methods=['POST', 'GET'])
def task1():
    if request.method == 'POST':
        latitude = request.form.get('latitudeValue')
        longitude = request.form.get('longitudeValue')
        list_of_data = []
        sql = "SELECT *,\
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
        as distance FROM eqi where mag > 6  ORDER BY Distance asc LIMIT 1"
        # print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('eqmagabove6.html', data=list_of_data, lat=latitude, long=longitude)


@app.route('/task2', methods=['POST', 'GET'])
def task2():
    if request.method == 'POST':
        latitude = request.form.get('latitudeValue')
        longitude = request.form.get('longitudeValue')
        list_of_data = []
        current = datetime.now().date()
        week = datetime.now().date() - timedelta(days=7)
        sql = " SELECT * from (SELECT *,\
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
            ) * 60 * 1.1515 * 1.609344\
        )\
        as distance FROM eqi where time between '"+str(week)+"' and '"+str(current)+"') WHERE DISTANCE<=500 ORDER BY MAG DESC LIMIT 1 "
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('task2.html', data=list_of_data, lat=latitude, long=longitude)


@app.route('/task3', methods=['POST', 'GET'])
def task3():
    if request.method == 'POST':
        latitude = request.form.get('latitudeValue')
        longitude = request.form.get('longitudeValue')
        date_from = request.form.get('dateFromValue')
        date_to = request.form.get('dateToValue')
        magnitude_from = request.form.get('magnitudeFromValue')
        magnitude_to = request.form.get('magnitudeToValue')
        distance = request.form.get('distanceValue')
        list_of_data = []
        sql = " SELECT * from (SELECT *,\
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
            ) * 60 * 1.1515 * 1.609344\
        )\
        as distance FROM eqi where (time between '"+str(date_from)+"' and '"+str(date_to)+"') and (mag between "+str(magnitude_from)+" and "+str(magnitude_to)+" )) WHERE DISTANCE<= "+distance+" ORDER BY MAG DESC "
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('task3.html', data=list_of_data, lat=latitude, long=longitude, magfrom=magnitude_from, magto=magnitude_to, distance=distance, datefrom=date_from, dateto=date_to)


@app.route('/task4', methods=['POST', 'GET'])
def task4():
    if request.method == 'POST':
        latitude = request.form.get('latitudeValue')
        longitude = request.form.get('longitudeValue')
        date_from = request.form.get('dateFromValue')
        date_to = request.form.get('dateToValue')
        magnitude_from = request.form.get('magnitudeFromValue')
        magnitude_to = request.form.get('magnitudeToValue')
        distance = request.form.get('distanceValue')
        list_of_data = []
        sql = " SELECT * from (SELECT *,\
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
            ) * 60 * 1.1515 * 1.609344\
        )\
        as distance FROM eqi where (time between '"+str(date_from)+"' and '"+str(date_to)+"') and (mag between "+str(magnitude_from)+" and "+str(magnitude_to)+" )) WHERE DISTANCE<= "+distance+" ORDER BY MAG DESC "
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('task3.html', data=list_of_data, lat=latitude, long=longitude, magfrom=magnitude_from, magto=magnitude_to, distance=distance, datefrom=date_from, dateto=date_to)


@app.route('/task5', methods=['POST', 'GET'])
def task5():
    if request.method == 'POST':
        latitude_one = float(request.form.get('latitudeValueOne'))
        longitude_one = float(request.form.get('longitudeValueOne'))
        latitude_two = float(request.form.get('latitudeValueTwo'))
        longitude_two = float(request.form.get('longitudeValueTwo'))
        if latitude_one > latitude_two:
            latitude_one, latitude_two = latitude_two, latitude_one
            print('one')

        if longitude_one > longitude_two:
            longitude_one, longitude_two = longitude_two, longitude_one
            print('two')

        list_of_data = []
        sql = "(SELECT *\
        FROM latlong where (latitude between '"+str(latitude_one)+"' and '"+str(latitude_two)+"') and (longitude between "+str(longitude_one)+" and "+str(longitude_two)+" )) "
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('task5.html', data=list_of_data, latitude_one=latitude_one, longitude_one=longitude_one, latitude_two=latitude_two, longitude_two=longitude_two)

@app.route('/task6', methods=['POST', 'GET'])
def task6():
    if request.method == 'POST':
        latitude = float(request.form.get('latitudeValue'))
        longitude = float(request.form.get('longitudeValue'))

        latitude_one = latitude-4.5045045045
        longitude_one = longitude-4.5045045045
        latitude_two = latitude+4.5045045045
        longitude_two = longitude+4.5045045045
        if latitude_one > latitude_two:
            latitude_one, latitude_two = latitude_two, latitude_one
            print('one')

        if longitude_one > longitude_two:
            longitude_one, longitude_two = longitude_two, longitude_one
            print('two')

        list_of_data = []
        sql = "(SELECT *\
        FROM eqi where (latitude between '"+str(latitude_one)+"' and '"+str(latitude_two)+"') and (longitude between "+str(longitude_one)+" and "+str(longitude_two)+" )) ORDER BY MAG DESC"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_tuple(stmt)
        # print(result)
        while result:
            list_of_data.append(result)
            result = ibm_db.fetch_tuple(stmt)
        # print(list_of_data)
        return render_template('task2.html', data=list_of_data, latitude=latitude, longitude=longitude)


@app.route('/task7', methods=['POST', 'GET'])
def task7():
    if request.method == 'POST':
        start = int(request.form.get('range1Value'))
        end = int(request.form.get('range2Value'))
        print(start)
        print(end)
        list_of_data = []

        for i in range(start,end):
            list2=[]
            list2.append(str(i)+'-'+str(i+1))
            sql = "(SELECT count(*)\
            FROM eqi where (mag between '"+str(i)+"' and '"+str(i+1)+"'))"
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_tuple(stmt)
            list2.append(result[0])
            list_of_data.append(list2)
            start+=1
        print(list_of_data)
        
        return render_template('task7.html', data=list_of_data)


@app.route('/help')
def help():
    text_list = []
    # Python Version
    text_list.append({
        'label': 'Python Version',
        'value': str(sys.version)})
    # os.path.abspath(os.path.dirname(__file__))
    text_list.append({
        'label': 'os.path.abspath(os.path.dirname(__file__))',
        'value': str(os.path.abspath(os.path.dirname(__file__)))
    })
    # OS Current Working Directory
    text_list.append({
        'label': 'OS CWD',
        'value': str(os.getcwd())})
    # OS CWD Contents
    label = 'OS CWD Contents'
    value = ''
    text_list.append({
        'label': label,
        'value': value})
    return render_template('help.html', text_list=text_list, title='help')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return render_template('404.html', title='404')


@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return render_template('500.html', title='500')


if __name__ == '__main__':
    if cf_port is None:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)
