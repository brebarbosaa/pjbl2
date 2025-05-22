from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator

write = Blueprint("write", __name__, template_folder="views")

@write.route("/history_write")
def history_write():
    actuators = Actuator.get_actuators()
    return render_template("history_write.html", actuators=actuators, write=[])

@write.route("/get_write", methods=['POST'])
def get_write():
    actuator_id = request.form.get('id')
    start = request.form.get('start')
    end = request.form.get('end')

    if not actuator_id or not start or not end:
        return "Parâmetros inválidos", 400

    actuator = Actuator.query.get(actuator_id)
    if not actuator:
        return "Atuador não encontrado", 404

    write_data = Write.get_write(actuator.device_id, start, end)
    actuators = Actuator.get_actuators()

    return render_template("history_write.html", actuators=actuators, write=write_data)
