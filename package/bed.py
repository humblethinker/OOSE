from flask_restful import Resource, Api, request
from package.model import conn

if list(conn.execute("SELECT COUNT(*) AS bed FROM bed").fetchone().values())[0] < 99:
    for i in range(1, 101):

        conn.execute('''INSERT INTO bed(pat_id) VALUES(NULL)''')
        conn.commit()


class Beds(Resource):
    def get(self):

        bed = conn.execute("SELECT * FROM bed ORDER BY bed_id DESC").fetchall()
        return bed


class Bed(Resource):

    def get(self, id):

        bed = conn.execute(
            "SELECT * FROM bed WHERE bed_id=?", (id,)).fetchall()
        return bed

    def put(self, id):

        bed = request.get_json(force=True)
        pat_id = appointment['pat_id']
        conn.execute("UPDATE bed SET pat_id=? WHERE bed_id=?",
                     (pat_id, id))
        conn.commit()
        return bed
