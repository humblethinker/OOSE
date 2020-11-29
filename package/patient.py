from flask_restful import Resource, Api, request
from package.model import conn




class Patients(Resource):
    """It contain all the api carryign the activity with aand specific patient"""

    def get(self):
        """Api to retive all the patient from the database"""

        patients = conn.execute("SELECT * FROM patient WHERE bed_id>0 ORDER BY pat_date DESC").fetchall()
        return patients



    def post(self):
        """api to add the patient in the database"""

        patientInput = request.get_json(force=True)
        pat_first_name=patientInput['pat_first_name']
        pat_last_name = patientInput['pat_last_name']
        age = patientInput['age']
        sex = patientInput['sex']
        pat_ph_no = patientInput['pat_ph_no']
        pat_address = patientInput['pat_address']
        bed_id = patientInput['bed_id']
        patientInput['pat_id']=conn.execute('''INSERT INTO patient(pat_first_name, pat_last_name, age,sex,pat_ph_no, pat_address, bed_id)
            VALUES(?,?,?,?,?,?,?)''', (pat_first_name, pat_last_name, age,sex,pat_ph_no, pat_address, bed_id)).lastrowid
        conn.execute("UPDATE bed SET pat_id=? WHERE bed_id=?",
                     (patientInput['pat_id'], bed_id))
        conn.commit()
        return patientInput

class Patient(Resource):
    """It contains all apis doing activity with the single patient entity"""

    def get(self,id):
        """api to retrive details of the patient by it id"""

        patient = conn.execute("SELECT * FROM patient WHERE pat_id=?",(id,)).fetchall()
        if len(patient)==0:
            return "Invalid ID"
        return patient

    def delete(self,id):
        """api to delete the patiend by its id"""
        conn.execute("DELETE FROM patient WHERE pat_id=?",(id,))
        conn.execute("UPDATE bed SET pat_id=NULL WHERE pat_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the patient by it id"""
        old_bed=conn.execute("SELECT * FROM patient WHERE pat_id=?",
                     (id,)).fetchone()
        conn.execute("UPDATE bed SET pat_id=NULL WHERE bed_id=?",
                     (old_bed['bed_id'],))
        patientInput = request.get_json(force=True)
        pat_first_name=patientInput['pat_first_name']
        pat_last_name = patientInput['pat_last_name']
        age = patientInput['age']
        sex = patientInput['sex']
        pat_ph_no = patientInput['pat_ph_no']
        pat_address = patientInput['pat_address']
        bed_id = patientInput['bed_id']
        conn.execute("UPDATE bed SET pat_id=? WHERE bed_id=?",
                     (id, bed_id))
        conn.execute("UPDATE patient SET pat_first_name=?, pat_last_name=?, age=?, sex=?, pat_ph_no=?, pat_address=?, bed_id=? WHERE pat_id=?",
                     (pat_first_name, pat_last_name, age, sex, pat_ph_no, pat_address, bed_id, id))
        conn.commit()
        return patientInput