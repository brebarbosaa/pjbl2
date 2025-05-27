from flask import Blueprint, request, render_template, flash, redirect, url_for
from decorators import admin_required
from models import db
from models.iot.devices import Device
from models.iot.sensors import Sensor

sensor_ = Blueprint('sensor_', __name__, template_folder='templates')

@sensor_.route('/register_sensor')
@admin_required
def register_sensor():
    return render_template('register_sensor.html')

@sensor_.route('/add_sensor', methods=['POST'])
@admin_required
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = request.form.get("is_active") == "on"

    Sensor.save_sensor(name, brand, model, topic, unit, is_active)
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors=sensors)

@sensor_.route('/sensors')
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors=sensors)

@sensor_.route('/edit_sensor')
@admin_required
def edit_sensor():
    id = request.args.get('id')
    sensor = Sensor.query.filter_by(id=id).first()
    return render_template("update_sensor.html", sensor=sensor)

@sensor_.route('/update_sensor', methods=['POST'])
@admin_required
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = request.form.get("is_active") == "on"

    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    return render_template("sensors.html", sensors=sensors)

@sensor_.route('/remove_sensor')
@admin_required
def remove_sensor():
    sensors = Sensor.query.all()
    return render_template("remove_sensor.html", sensors=sensors)

@sensor_.route('/del_sensor', methods=['GET', 'POST'])
@admin_required
def del_sensor():
    if request.method == 'POST':
        id = request.form.get('id')
    else:
        id = request.args.get('id')

    if id:
        Sensor.delete_sensor(id)
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors=sensors)
