from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'read'

    id = db.Column(db.Integer, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    @staticmethod
    def save_read(sensor, value):
        device = Device.query.get(sensor.device_id)
        if device and device.is_active:
            read = Read(
                read_datetime=datetime.utcnow(),
                sensors_id=sensor.id,
                value=float(value)
            )
            db.session.add(read)
            db.session.commit()

    @staticmethod
    def get_read(device_id, start, end):
        try:
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end)
        except ValueError:
            return []

        sensor_ids = [s.id for s in Sensor.query.filter_by(device_id=device_id).all()]
        return Read.query.filter(
            Read.sensors_id.in_(sensor_ids),
            Read.read_datetime >= start_date,
            Read.read_datetime <= end_date
        ).all()

    @staticmethod
    def get_last_value(topic):
        sensor = Sensor.query.filter_by(topic=topic).first()
        if not sensor:
            return None
        return Read.query.filter_by(sensors_id=sensor.id).order_by(Read.read_datetime.desc()).first()
