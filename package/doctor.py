from flask_restful import Resource, Api, request
from package.model import conn
from werkzeug.security import generate_password_hash
class Doctors(Resource):
    """This contain apis to carry out activity with all doctors"""

    def get(self):
        """Retrive list of all the doctor"""

        doctors = conn.execute("SELECT * FROM user ORDER BY user_date DESC").fetchall()
        return doctors



    def post(self):
        """Add the new doctor"""

        doctorInput = request.get_json(force=True)
        doc_first_name=doctorInput['user_first_name']
        doc_last_name = doctorInput['user_last_name']
        age = doctorInput['age']
        sex = doctorInput['sex']
        designation = doctorInput['designation']
        doc_ph_no = doctorInput['user_ph_no']
        doc_address = doctorInput['user_address']
        password = generate_password_hash(doctorInput['password'])
        doctorInput['user_id']=conn.execute('''INSERT INTO user(user_first_name,user_last_name,age,sex,user_ph_no,user_address, password, designation)
            VALUES(?,?,?,?,?,?,?,?)''', (doc_first_name,doc_last_name,age,sex,doc_ph_no,doc_address,password, designation)).lastrowid
        conn.commit()
        return doctorInput

class Doctor(Resource):


    def get(self,id):

        doctor = conn.execute("SELECT * FROM user WHERE user_id=?",(id,)).fetchall()
        return doctor

    def delete(self, id):

        conn.execute("DELETE FROM user WHERE user_id=?", (id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):

        doctorInput = request.get_json(force=True)
        doc_first_name=doctorInput['user_first_name']
        doc_last_name = doctorInput['user_last_name']
        age = doctorInput['age']
        sex = doctorInput['sex']
        designation = doctorInput['designation']
        doc_ph_no = doctorInput['user_ph_no']
        doc_address = doctorInput['user_address']
        password = generate_password_hash(doctorInput['password'])
        conn.execute(
            "UPDATE user SET user_first_name=?,user_last_name=?,age=?,sex=?, designation=?, user_ph_no=?,user_address=?, password=? WHERE user_id=?",
            (doc_first_name, doc_last_name, age, sex, designation, doc_ph_no, doc_address,password, id))
        conn.commit()
        return doctorInput