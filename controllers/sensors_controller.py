from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from decorators import admin_required
from models import db
from models.iot.devices import Device
from models.iot.sensors import Sensor

sensor_ = Blueprint('sensor_', __name__, template_folder='templates')

@sensor_.route('/sensors')
@login_required
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors=sensors)

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
    flash("Sensor adicionado com sucesso!", "success")
    return redirect(url_for("sensor_.sensors"))

# ✅ Página de edição
@sensor_.route('/edit_sensor/<int:id>', methods=['GET'])
@admin_required
def edit_sensor(id):
    sensor = Sensor.query.filter_by(device_id=id).first()

    if not sensor:
        flash("Sensor não encontrado.", "danger")
        return redirect(url_for("sensor_.sensors"))

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

    Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    flash("Sensor atualizado com sucesso!", "success")
    return redirect(url_for("sensor_.sensors"))

@sensor_.route('/remove_sensor')
@admin_required
def remove_sensor():
    sensors = Sensor.query.all()
    return render_template("remove_sensor.html", sensors=sensors)

@sensor_.route('/del_sensor/<int:id>', methods=['POST'])
@admin_required
def del_sensor(id):
    Sensor.delete_sensor(id)
    flash("Sensor deletado com sucesso!", "success")
    return redirect(url_for("sensor_.sensors"))
