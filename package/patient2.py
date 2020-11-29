from flask_restful import Resource, Api, request
from package.model import conn




class Patient2(Resource):

    def put(self,id):

        patientInput = request.get_json(force=True)
        tests=patientInput['tests']
        charges = patientInput['charges']
        diagnosis = patientInput['diagnosis']
        conn.execute("UPDATE patient SET tests=?, diagnosis=?, charges=? WHERE pat_id=?",
                     (tests, diagnosis, charges, id))
        conn.commit()
        return patientInput