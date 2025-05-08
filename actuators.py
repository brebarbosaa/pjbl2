from flask import Blueprint, request, render_template

actuators = Blueprint("actuators", __name__, template_folder="templates")

# Lista de atuadores iniciais (exemplo de status 1 ou 0 para "ligado" ou "desligado")
@actuators.route('/dashboard')
def dashboard():
    atuadores = {
        'Servo Motor': 'Desligado',
        'LEDs': 'Ligados',
        'Cooler': 'Desligado',
    }
    return render_template('dashboard_atuadores.html', atuadores=atuadores)
@actuators.route('/register_actuator')
def register_actuator():
    return render_template('register_actuator.html')

@actuators.route('/add_actuator', methods=['POST'])
def add_actuator():
    global atuadores
    if request.method == 'POST':
        atuador = request.form['atuador']
        valor = request.form['valor']
    else:
        atuador = request.args.get('atuador', None)
        valor = request.args.get('valor', None)
    atuadores[atuador] = valor
    return render_template('actuators.html', devices=atuadores)

@actuators.route('/remove_actuator')
def remove_actuator():
    global atuadores
    return render_template('remove_actuator.html', devices=atuadores)

@actuators.route('/del_actuator', methods=['GET', 'POST'])
def del_actuator():
    global atuadores
    if request.method == 'POST':
        atuador = request.form['atuador']
    else:
        atuador = request.args.get('atuador', None)
    if atuador in atuadores:
        atuadores.pop(atuador)
    return render_template('actuators.html', devices=atuadores)

@actuators.route('/actuators')
def atuadores():
    global atuadores
    return render_template('actuators.html', devices=atuadores)
