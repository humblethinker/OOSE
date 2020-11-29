from flask_restful import Resource, Api, request
from package.model import conn
from werkzeug.security import generate_password_hash
class Medicines(Resource):
    """This contain apis to carry out activity with all doctors"""

    def get(self):
        """Retrive list of all the doctor"""

        meds = conn.execute("SELECT * FROM medicine ORDER BY med_id DESC").fetchall()
        return meds



    def post(self):
        """Add the new doctor"""

        medInput = request.get_json(force=True)
        med_name=medInput['med_name']
        uses = medInput['uses']
        quant = medInput['quant']
        medInput['med_id']=conn.execute('''INSERT INTO medicine (med_name, uses, quant)
            VALUES(?,?,?)''', (med_name, uses, quant)).lastrowid
        conn.commit()
        return medInput

class Medicine(Resource):


    def get(self,id):

        med = conn.execute("SELECT * FROM medicine WHERE med_id=?",(id,)).fetchall()
        return med

    def delete(self, id):

        conn.execute("DELETE FROM medicine WHERE med_id=?", (id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):

        medInput = request.get_json(force=True)
        med_name=medInput['med_name']
        uses = medInput['uses']
        quant = medInput['quant']
        conn.execute(
            "UPDATE medicine SET med_name=?,uses=?,quant=? WHERE med_id=?",
            (med_name, uses, quant, id))
        conn.commit()
        return medInput