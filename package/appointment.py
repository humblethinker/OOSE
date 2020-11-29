from flask_restful import Resource, Api, request
from package.model import conn



class Appointments(Resource):

    def get(self):

        appointment = conn.execute("SELECT p.*,d.*,a.* from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN user d ON a.user_id = d.user_id ORDER BY appointment_date DESC").fetchall()
        return appointment

    def post(self):

        appointment = request.get_json(force=True)
        pat_id = appointment['pat_id']
        doc_id = appointment['user_id']
        appointment_date = appointment['appointment_date']
        appointment['app_id'] = conn.execute('''INSERT INTO appointment(pat_id,user_id,appointment_date)
            VALUES(?,?,?)''', (pat_id, doc_id,appointment_date)).lastrowid
        conn.commit()
        return appointment



class Appointment(Resource):

    def get(self,id):
        """retrive a singe appointment details by its id"""

        appointment = conn.execute("SELECT * FROM appointment WHERE app_id=?",(id,)).fetchall()
        return appointment


    def delete(self,id):

        conn.execute("DELETE FROM appointment WHERE app_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):

        appointment = request.get_json(force=True)
        pat_id = appointment['pat_id']
        doc_id = appointment['user_id']
        conn.execute("UPDATE appointment SET pat_id=?,user_id=? WHERE app_id=?",
                     (pat_id, doc_id, id))
        conn.commit()
        return appointment