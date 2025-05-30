from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

# models/iot/write.py
class Write(db.Model):
    __tablename__ = 'write'

    id = db.Column(db.Integer, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    value = db.Column(db.String(50), nullable=True)
    origin = db.Column(db.String(20), nullable=False, default="automatico")

    actuator = db.relationship("Actuator", backref="writes")

    @staticmethod
    def save_write(actuator, value, origin="automatico"):
        device = Device.query.get(actuator.device_id)
        if device and device.is_active:
            write = Write(
                write_datetime=datetime.utcnow(),
                actuators_id=actuator.id,
                value=str(value),
                origin=origin
            )
            db.session.add(write)
            db.session.commit()


    @staticmethod
    def get_write(device_id, start, end):
        try:
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end)
        except ValueError:
            return []

        actuator_ids = [a.id for a in Actuator.query.filter_by(device_id=device_id).all()]
        return Write.query.filter(
            Write.actuators_id.in_(actuator_ids),
            Write.write_datetime >= start_date,
            Write.write_datetime <= end_date
        ).all()
