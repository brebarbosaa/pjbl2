from flask import Blueprint, request, render_template
from decorators import admin_required
sensors = Blueprint("sensors", __name__, template_folder="templates")

# Inicializa a lista de sensores (simulando dados de sensores)
lista_sensor = {
        'Temperatura': '23.5 ºC',
        'Umidade': '60 %',
        'Movimento': 'Detectado',
        'Distância': '140'
    }
@sensors.route('/dashboard')
def dashboard():
    return render_template('dashboard_sensores.html', sensores=lista_sensor)

@sensors.route('/register_sensor')
@admin_required
def register_sensor():
    return render_template('register_sensor.html')

@sensors.route('/add_sensor', methods=['POST'])
@admin_required
def add_sensor():
    global lista_sensor
    if request.method == 'POST':
        sensor = request.form['sensor']
        valor = request.form['valor']
        try:
            valor = float(valor)  # Converte o valor para float para cálculos
        except ValueError:
            return "Erro: O valor do sensor deve ser um número!", 400
    else:
        sensor = request.args.get('sensor', None)
        valor = request.args.get('valor', None)
        try:
            valor = float(valor)
        except ValueError:
            return "Erro: O valor do sensor deve ser um número!", 400

    lista_sensor[sensor] = valor
    return render_template('sensors.html', devices=lista_sensor)

@sensors.route('/remove_sensor')
@admin_required
def remove_sensor():
    global lista_sensor
    return render_template('remove_sensor.html', devices=lista_sensor)

@sensors.route('/del_sensor', methods=['GET', 'POST'])
@admin_required
def del_sensor():
    global lista_sensor
    if request.method == 'POST':
        sensor = request.form['sensor']
    else:
        sensor = request.args.get('sensor', None)
    if sensor in lista_sensor:
        lista_sensor.pop(sensor)
    else:
        return f"Erro: O sensor '{sensor}' não encontrado!", 404
    return render_template('sensors.html', devices=lista_sensor)

@sensors.route('/sensors')
def sensores():
    global lista_sensor
    return render_template("sensors.html", devices=lista_sensor)