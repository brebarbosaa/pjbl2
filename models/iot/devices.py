from models.db import db

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    sensor = db.relationship('Sensor', backref='device', lazy=True)
    actuator = db.relationship('Actuator', backref='device', lazy=True)