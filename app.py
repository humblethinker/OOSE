from flask import Flask, send_from_directory, render_template, jsonify, request, session, redirect, url_for
from flask_restful import Resource, Api
from package.patient import Patients, Patient
from package.doctor import Doctors, Doctor
from package.appointment import Appointments, Appointment
from package.bed import Beds, Bed
from package.medicine import Medicines, Medicine
from package.discharge import Discharge
from package.patient2 import Patient2
from package.common import Common
import sqlite3
from werkzeug.security import check_password_hash
import json
import datetime


with open('C:/Users/humbl/Downloads/OOSE/config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='', template_folder='static')
app.secret_key = "secret key"
api = Api(app)

api.add_resource(Patients, '/patient')
api.add_resource(Patient, '/patient/<int:id>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Doctor, '/doctor/<int:id>')
api.add_resource(Appointments, '/appointment')
api.add_resource(Appointment, '/appointment/<int:id>')
api.add_resource(Beds, '/bed')
api.add_resource(Bed, '/bed/<int:id>')
api.add_resource(Medicines, '/medicine')
api.add_resource(Medicine, '/medicine/<int:id>')
api.add_resource(Discharge, '/discharge/<int:id>')
api.add_resource(Patient2, '/patient2/<int:id>')

api.add_resource(Common, '/common')


def logins(email, pwd):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(config['database'], check_same_thread=False)
        conn.execute('pragma foreign_keys=ON')
        cursor = conn.cursor()

        sql = "SELECT user_id, password FROM user WHERE user_id=?"
        sql_where = (email,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()

        if row:
            if check_password_hash(row[1], pwd):
                return row[0]
            return None

    except Exception as e:
        print(e)

    finally:
    	if cursor and conn:
    		cursor.close()
    		conn.close()


# Routes

@app.route('/invoice/<id>')
def invoice(id):
	conn = sqlite3.connect(config['database'], check_same_thread=False)
	conn.execute('pragma foreign_keys=ON')
	cursor = conn.cursor()
	
	
	date1 = datetime.date.today()
	end_date = date1 + datetime.timedelta(days=2)

	row = conn.execute(
	    "SELECT pat_first_name, pat_last_name, charges, pat_ph_no FROM patient WHERE pat_id=?", (id,)).fetchone()
	days = conn.execute(
	    "SELECT julianday('now') - julianday(pat_date) FROM patient WHERE pat_id=?", (id,)).fetchone()
	cursor.close()
	conn.close()
	return render_template('invoice.html', pat_id=id, discharge_date = date1, due_date=end_date, pat_first_name=row[0], pat_last_name=row[1], pat_ph_no=row[3], charges=row[2], bed_charge=500*int(days[0]), total=500*int(days[0])+row[2])

@app.route('/invoice2/<id>')
def invoice2(id):
	conn = sqlite3.connect(config['database'], check_same_thread=False)
	conn.execute('pragma foreign_keys=ON')
	cursor = conn.cursor()
	
	
	date1 = datetime.date.today()
	end_date = date1 + datetime.timedelta(days=2)

	row = conn.execute(
	    "SELECT pat_first_name, pat_last_name, charges, pat_ph_no FROM patient WHERE pat_id=?", (id,)).fetchone()
	days = conn.execute(
	    "SELECT julianday('now') - julianday(pat_date) FROM patient WHERE pat_id=?", (id,)).fetchone()
	cursor.close()
	conn.close()
	return render_template('invoice2.html', pat_id=id, discharge_date = date1, due_date=end_date, pat_first_name=row[0], pat_last_name=row[1], pat_ph_no=row[3], charges=row[2], bed_charge=500*int(days[0]), total=500*int(days[0])+row[2])


@app.route('/login', methods=['POST'])
def login():
	_json = request.json
	# print(_json)
	_username = _json['username']
	_password = _json['password']
	
	if _username and _password:
		user = logins(_username, _password)
		
		if user != None:
			session['username'] = user
			return jsonify({'message' : 'User logged in successfully'})

	resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
	resp.status_code = 400
	return resp

@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', None)
	return jsonify({'message' : 'You successfully logged out'})

@app.route('/login/page')
def login_page():
    return render_template('login2.html')

@app.route('/card/<id>')
def card(id):
	return app.send_static_file('card2.html')

@app.route('/')
def home_page():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])
