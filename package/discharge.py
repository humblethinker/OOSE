from flask_restful import Resource, Api, request
from package.model import conn

class Discharge(Resource):


    def get(self,id):

        pay = conn.execute("SELECT * FROM payment WHERE payment_id=?",(id,)).fetchall()
        return pay

    def put(self,id):

        pay = conn.execute("SELECT * FROM patient WHERE pat_id=?",(id,)).fetchone()
        amount = pay['charges']
        conn.execute('''INSERT INTO payment(pat_id, amount)
            VALUES(?, ?)''', (id, amount))
        conn.execute("UPDATE bed SET pat_id=NULL WHERE pat_id=?",(id,))
        conn.execute("UPDATE patient SET bed_id=-1 discharge_date=(datetime('now','localtime')) WHERE pat_id=?",(id,))
        conn.commit()
        return "success"