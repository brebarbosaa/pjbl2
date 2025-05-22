from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = 'actuator'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    device = db.relationship('Device', backref=db.backref('actuator', uselist=False))

    @staticmethod
    def save_actuator(name, brand, model, topic, unit, is_active):
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        db.session.add(device)
        db.session.commit()

        actuator = Actuator(device_id=device.id, unit=unit, topic=topic)
        db.session.add(actuator)
        db.session.commit()

    @staticmethod
    def get_actuators():
        return Actuator.query.join(Device).add_columns(
            Actuator.id,
            Device.id.label("device_id"),
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Actuator.topic,
            Actuator.unit
        ).all()

    @staticmethod
    def get_single_actuator(id):
        return Actuator.query.join(Device).add_columns(
            Actuator.id,
            Device.id.label("device_id"),
            Device.name,
            Device.brand,
            Device.model,
            Device.is_active,
            Actuator.topic,
            Actuator.unit
        ).filter(Device.id == id).first()

    @staticmethod
    def update_actuator(id, name, brand, model, topic, unit, is_active):
        device = Device.query.get(id)
        actuator = Actuator.query.filter_by(device_id=id).first()

        if device and actuator:
            device.name = name
            device.brand = brand
            device.model = model
            device.is_active = is_active
            actuator.topic = topic
            actuator.unit = unit
            db.session.commit()

        return Actuator.get_actuators()

    @staticmethod
    def delete_actuator(id):
        actuator = Actuator.query.filter_by(device_id=id).first()
        device = Device.query.get(id)

        if actuator:
            db.session.delete(actuator)
        if device:
            db.session.delete(device)
        db.session.commit()

        return Actuator.get_actuators()
