from flask import Blueprint, request, render_template
from decorators import admin_required
from models.iot.actuators import Actuator

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

@actuator_.route('/edit_actuator')
@admin_required
def edit_actuator():
    id = request.args.get('id')
    actuator = Actuator.query.filter_by(id=id).first()
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

@actuator_.route('/del_actuator')
@admin_required
def del_actuator():
    id = request.args.get('id')
    actuators = Actuator.delete_actuator(id)
    return render_template("actuators.html", actuators=actuators)
