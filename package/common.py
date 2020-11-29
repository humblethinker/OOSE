from flask_restful import Resource, Api, request
from package.model import conn


class Common(Resource):
    def get(self):

        getPatientCount=conn.execute("SELECT COUNT(*) AS patient FROM patient WHERE bed_id>0").fetchone()
        getDoctorCount = conn.execute("SELECT COUNT(*) AS doctor FROM user").fetchone()
        getAppointmentCount = conn.execute("SELECT COUNT(*) AS appointment FROM appointment").fetchone()
        getBedCount = conn.execute("SELECT COUNT(*) AS bed FROM bed WHERE pat_id IS NULL").fetchone()
        getMedicineCount = conn.execute("SELECT COUNT(*) AS medicine FROM medicine").fetchone()
        getPatientCount.update(getDoctorCount)
        getPatientCount.update(getAppointmentCount)
        getPatientCount.update(getBedCount)
        getPatientCount.update(getMedicineCount)
        return getPatientCount