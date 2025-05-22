from flask import Blueprint, request, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor

read = Blueprint("read", __name__, template_folder="views")

@read.route("/history_read")
def history_read():
    sensors = Sensor.get_sensors()
    return render_template("history_read.html", sensors=sensors, read=[])

@read.route("/get_read", methods=['POST'])
def get_read():
    sensor_id = request.form.get('id')
    start = request.form.get('start')
    end = request.form.get('end')

    if not sensor_id or not start or not end:
        return "Parâmetros inválidos", 400

    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return "Sensor não encontrado", 404

    read_data = Read.get_read(sensor.device_id, start, end)
    sensors = Sensor.get_sensors()

    return render_template("history_read.html", sensors=sensors, read=read_data)
