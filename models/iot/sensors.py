from models.db import db
from models.iot.devices import Device


class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    device = db.relationship('Device', back_populates='sensors')

    @staticmethod
    def save_sensor(name, brand, model, topic, unit, is_active):
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        db.session.add(device)
        db.session.commit()

        sensor = Sensor(device_id=device.id, unit=unit, topic=topic)
        db.session.add(sensor)
        db.session.commit()

    @staticmethod
    def get_sensors():
        return Sensor.query.join(Device).add_columns(
            Sensor.id,
            Device.id.label("device_id"),
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Sensor.topic,
            Sensor.unit
        ).all()

    @staticmethod
    def get_single_sensor(id):
        return Sensor.query.join(Device).add_columns(
            Sensor.id,
            Device.id.label("device_id"),
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Sensor.topic,
            Sensor.unit
        ).filter(Device.id == id).first()

    @staticmethod
    def update_sensor(id, name, brand, model, topic, unit, is_active):
        device = Device.query.get(id)
        sensor = Sensor.query.filter_by(device_id=id).first()

        if device and sensor:
            device.name = name
            device.brand = brand
            device.model = model
            device.is_active = is_active
            sensor.topic = topic
            sensor.unit = unit
            db.session.commit()

        return Sensor.get_sensors()

    @staticmethod
    def delete_sensor(id):
        device = Device.query.get(id)
        sensor = Sensor.query.filter_by(device_id=id).first()

        if sensor:
            db.session.delete(sensor)
        if device:
            db.session.delete(device)
        db.session.commit()

        return Sensor.get_sensors()
