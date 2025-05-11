from flask import Blueprint, request, render_template
from decorators import admin_required

actuators = Blueprint("actuators", __name__, template_folder="templates")

dicAtuadores = {
        'Servo Motor': 'Desligado',
        'LEDs': 'Ligados',
        'Cooler': 'Desligado',
}
# Lista de atuadores iniciais (exemplo de status 1 ou 0 para "ligado" ou "desligado")
@actuators.route('/dashboard')
def dashboard():
    return render_template('dashboard_atuadores.html', atuadores=dicAtuadores)

@actuators.route('/register_actuator')
@admin_required
def register_actuator():
    return render_template('register_actuator.html')

@actuators.route('/add_actuator', methods=['POST'])
@admin_required
def add_actuator():
    if request.method == 'POST':
        atuador = request.form['atuador']
        valor = request.form['valor']
    else:
        atuador = request.args.get('atuador', None)
        valor = request.args.get('valor', None)
    dicAtuadores[atuador] = valor
    return render_template('actuators.html', devices=dicAtuadores)

@actuators.route('/remove_actuator')
@admin_required
def remove_actuator():
    return render_template('remove_actuator.html', devices=dicAtuadores)

@actuators.route('/del_actuator', methods=['GET', 'POST'])
@admin_required
def del_actuator():
    if request.method == 'POST':
        atuador = request.form['atuador']
    else:
        atuador = request.args.get('atuador', None)
    if atuador in dicAtuadores:
        dicAtuadores.pop(atuador)
    return render_template('actuators.html', devices=dicAtuadores)

@actuators.route('/actuators')
def visualizar_atuadores():
    return render_template('actuators.html', devices=dicAtuadores)
