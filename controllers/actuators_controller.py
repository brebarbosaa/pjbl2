from flask import Blueprint, request, render_template, flash, redirect, url_for
from decorators import admin_required
from models import db
from models.iot.actuators import Actuator
from models.iot.devices import Device

actuator_ = Blueprint('actuator_', __name__, template_folder='templates')

@actuator_.route('/register_actuator')
@admin_required
def register_actuator():
    return render_template('register_actuator.html')

@actuator_.route('/add_actuator', methods=['POST'])
@admin_required
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = request.form.get("is_active") == "on"

    Actuator.save_actuator(name, brand, model, topic, unit, is_active)
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

@actuator_.route('/actuators')
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

@actuator_.route('/edit_actuator/<int:id>', methods=['GET'])
@admin_required
def edit_actuator(id):
    actuator = Actuator.query.filter_by(device_id=id).first()

    if actuator is None or actuator.device is None:
        return "Atuador não encontrado", 404

    return render_template("update_actuator.html", actuator=actuator)

@actuator_.route('/update_actuator', methods=['POST'])
@admin_required
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = request.form.get("is_active") == "on"

    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    return render_template("actuators.html", actuators=actuators)


@actuator_.route('/remove_actuator')
@admin_required
def remove_actuator():
    actuators = Actuator.query.all()
    return render_template("remove_actuator.html", actuators=actuators)

@actuator_.route('/del_actuator', methods=['GET', 'POST'])
@admin_required
def del_actuator():
    if request.method == 'POST':
        id = request.form.get('id')
    else:
        id = request.args.get('id')

    if id:
        Actuator.delete_actuator(id)
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

