from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from decorators import admin_required
from models.iot.actuators import Actuator

actuator_ = Blueprint('actuator_', __name__, template_folder='templates')

@actuator_.route('/actuators')
@login_required
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

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
    flash("Atuador adicionado com sucesso!", "success")
    return redirect(url_for("actuator_.actuators"))

@actuator_.route('/edit_actuator/<int:id>', methods=['GET'])
@admin_required
def edit_actuator(id):
    actuator = Actuator.query.filter_by(device_id=id).first()

    if not actuator:
        flash("Atuador não encontrado.", "danger")
        return redirect(url_for("actuator_.actuators"))

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

    Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    flash("Atuador atualizado com sucesso!", "success")
    return redirect(url_for("actuator_.actuators"))

@actuator_.route('/remove_actuator')
@admin_required
def remove_actuator():
    actuators = Actuator.query.all()
    return render_template("remove_actuator.html", actuators=actuators)

@actuator_.route('/del_actuator/<int:id>', methods=['POST'])
@admin_required
def del_actuator(id):
    Actuator.delete_actuator(id)
    flash("Atuador deletado com sucesso!", "success")
    return redirect(url_for("actuator_.actuators"))
